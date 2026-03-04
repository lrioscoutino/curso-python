# Tutorial: Registro de Usuarios con UserCreationForm en Django

> **Prerequisito**: Haber completado el tutorial de `django_login` (Login y Logout con LoginView y LogoutView).

## Teoria: Que es UserCreationForm?

Es un **formulario built-in** de Django que vive en `django.contrib.auth.forms`. Maneja todo lo necesario para crear un usuario nuevo:

| Caracteristica | Que hace? |
|---|---|
| Campos incluidos | `username`, `password1`, `password2` (confirmacion) |
| Validacion de contrasena | Minimo 8 caracteres, no puede ser solo numeros, no puede ser muy comun |
| Validacion de username | Verifica que no exista otro usuario con el mismo nombre |
| Creacion segura | Guarda la contrasena hasheada (nunca en texto plano) |

**Por que usarlo?** Porque reinventar la validacion de contrasenas y la creacion segura de usuarios es propenso a errores de seguridad. Django ya lo resuelve.

---

## Paso 1: Crear el formulario de registro

Crea el archivo `users/forms.py`. Aqui extendemos `UserCreationForm` para agregar el campo `email`:

```python
# users/forms.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

### Teoria - puntos clave:

1. **`UserCreationForm`** ya incluye `username`, `password1` y `password2`. No necesitas declararlos.

2. **`class Meta`** — Es la forma en que Django configura formularios basados en modelos (ModelForm). Le dice: "usa el modelo `User` y muestra estos campos".

3. **`fields`** — Lista los campos que quieres en el formulario, **en el orden que se mostraran**. `email` no viene por defecto en `UserCreationForm`, por eso lo agregamos aqui.

4. **`password1` y `password2`** — No son campos del modelo `User`. Son campos especiales del formulario que `UserCreationForm` usa para pedir y confirmar la contrasena. Al guardar, solo `password1` se hashea y almacena.

---

## Paso 2: Crear la vista de registro

```python
# users/views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")

def inicio(request):
    context = {
        "name": "Mario Garcia",
        "message": "Hello, world.",
        "age": 45,
        "example_list": [23, 5, 6, 7, 8, 9]
    }
    return render(request, "base.html", context=context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
```

### Teoria - puntos clave:

1. **`request.method == 'POST'`** — Distinguimos entre dos situaciones:
   - **GET**: El usuario llega a la pagina por primera vez → mostramos formulario vacio.
   - **POST**: El usuario envio el formulario → procesamos los datos.

2. **`RegisterForm(request.POST)`** — Crea el formulario con los datos que envio el usuario. Sin `request.POST`, el formulario estaria vacio.

3. **`form.is_valid()`** — Ejecuta TODAS las validaciones:
   - El username no esta repetido?
   - Las contrasenas coinciden?
   - La contrasena cumple las reglas de seguridad?
   - El email tiene formato valido?
   Si algo falla, los errores quedan en `form.errors` y se muestran en el template.

4. **`form.save()`** — Crea el usuario en la base de datos con la contrasena hasheada. Retorna el objeto `User` creado.

5. **`login(request, user)`** — Inicia sesion automaticamente despues del registro. Sin esta linea, el usuario se registra pero queda deslogueado (tendria que ir a `/login/` manualmente).

6. **`redirect('inicio')`** — Redirige a la pagina de inicio usando el nombre de la URL. Usa redireccion (no `render`) para evitar re-envio del formulario si el usuario recarga la pagina (patron POST/Redirect/GET).

### Flujo visual de la vista:

```
Usuario visita /register/
        |
        v
   Es POST?
   /       \
  NO        SI
  |          |
  v          v
form =     form = RegisterForm(request.POST)
RegisterForm()    |
  |               v
  |          form.is_valid()?
  |          /            \
  |        SI              NO
  |         |               |
  |         v               |
  |    form.save()          |
  |    login(user)          |
  |    redirect('inicio')   |
  |                         |
  v                         v
render('register.html', {'form': form})
(form vacio)          (form con errores)
```

---

## Paso 3: Agregar la URL de registro

```python
# config/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import index, inicio, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('inicio/', inicio, name='inicio'),

    # LOGIN y LOGOUT (del tutorial anterior)
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # REGISTRO (nuevo)
    path('register/', register, name='register'),
]
```

### Teoria:

- La URL de registro es una **vista de funcion (FBV)**, no una CBV como `LoginView`. Esto es porque `UserCreationForm` no tiene una vista built-in equivalente a `LoginView`. Necesitamos escribir la logica nosotros.
- Usamos `name='register'` para poder referenciarla en templates con `{% url 'register' %}`.

---

## Paso 4: Crear el template de registro

```html
<!-- templates/register.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registro</title>
</head>
<body>

<h2>Crear cuenta</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Registrarse</button>
</form>

<p>Ya tienes cuenta? <a href="{% url 'login' %}">Inicia sesion</a></p>

</body>
</html>
```

### Teoria - puntos clave:

1. **`{{ form.as_p }}`** — Renderiza los 4 campos (`username`, `email`, `password1`, `password2`) con sus labels, inputs, textos de ayuda y errores. Django genera automaticamente:
   - Las reglas de la contrasena como texto de ayuda
   - Mensajes de error si la validacion falla

2. **Enlace a login** — Buena practica de UX: si el usuario ya tiene cuenta, puede ir directo al login sin navegar manualmente.

3. **Los errores se muestran automaticamente** — Si `form.is_valid()` falla en la vista, `form.as_p` incluye los mensajes de error junto a cada campo.

---

## Paso 5: Agregar enlace de registro en login.html

Actualiza `login.html` para que los usuarios nuevos puedan ir al registro:

```html
<!-- templates/login.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>

{% if request.user.is_authenticated %}
    <p>Bienvenido, {{ request.user.username }}</p>
    <a href="{% url 'logout' %}">Cerrar sesion</a>
{% else %}
    <h2>Iniciar sesion</h2>

    {% if form.errors %}
        <p style="color: red;">Usuario o contrasena incorrectos.</p>
    {% endif %}

    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Entrar</button>
    </form>

    <p>No tienes cuenta? <a href="{% url 'register' %}">Registrate aqui</a></p>
{% endif %}

</body>
</html>
```

---

## Paso 6: Probar

```bash
python3 manage.py migrate
python3 manage.py runserver
```

1. Ir a `http://127.0.0.1:8000/register/` — Veras el formulario con 4 campos
2. Dejar campos vacios y enviar — Veras errores de validacion
3. Poner contrasenas que no coincidan — Veras "The two password fields didn't match"
4. Poner una contrasena debil como "1234" — Veras los errores de seguridad
5. Llenar todo correctamente — Se crea el usuario, inicia sesion y redirige a `/inicio/`
6. Ir a `http://127.0.0.1:8000/inicio/` — Veras "Usuario: tu_nombre_nuevo"

---

## Flujo completo: Registro + Login + Logout

```
Usuario nuevo visita /register/
        |
        v
   +-----------------+
   |  register view   |---- GET ----> Renderiza register.html con form vacio
   +-----------------+
        |
      POST (usuario envia datos)
        |
        v
   Datos validos?
    /            \
  SI              NO
   |               |
   v               v
form.save()     Re-renderiza register.html
(crea user)     con form.errors
   |
   v
login(user)     <-- Inicia sesion automaticamente
   |
   v
Redirect a 'inicio'
   |
   v
Usuario usa la app normalmente
   |
   v
Click en "Cerrar sesion"
   |
   v
   +--------------+
   |  LogoutView   |--> Destruye sesion
   +--------------+
        |
        v
   Redirect a 'login'
   |
   v
   Ya tiene cuenta -> Login
   No tiene cuenta -> Click en "Registrate aqui" -> /register/
```

---

## Extra: Renderizar campos individualmente

Si quieres mas control visual sobre el formulario:

```html
<form method="post">
    {% csrf_token %}

    <div>
        <label for="{{ form.username.id_for_label }}">Usuario:</label>
        {{ form.username }}
        <small>{{ form.username.help_text }}</small>
        {% for error in form.username.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        <label for="{{ form.email.id_for_label }}">Email:</label>
        {{ form.email }}
        {% for error in form.email.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        <label for="{{ form.password1.id_for_label }}">Contrasena:</label>
        {{ form.password1 }}
        <small>{{ form.password1.help_text }}</small>
        {% for error in form.password1.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        <label for="{{ form.password2.id_for_label }}">Confirmar contrasena:</label>
        {{ form.password2 }}
        {% for error in form.password2.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>

    <button type="submit">Registrarse</button>
</form>
```

### Teoria:

- **`help_text`** — Texto de ayuda que Django genera para cada campo. En `password1` muestra las reglas de seguridad.
- **`id_for_label`** — Genera el `id` correcto para el atributo `for` del `<label>`, conectando label con input (importante para accesibilidad).
- **Renderizar individualmente** te permite agregar clases CSS, wrappers `<div>`, iconos, o cualquier HTML custom alrededor de cada campo.

---

## Extra: Personalizar mensajes de error en espanol

Por defecto los errores estan en ingles. Para cambiar a espanol, agrega en `settings.py`:

```python
# config/settings.py

LANGUAGE_CODE = 'es'
```

Esto cambia **todos** los mensajes built-in de Django a espanol, incluyendo:
- "Este campo es obligatorio"
- "Las contrasenas no coinciden"
- "Ya existe un usuario con ese nombre"

---

## Extra: Validar que el email sea obligatorio

Por defecto el campo `email` en `User` es **opcional**. Si quieres hacerlo obligatorio:

```python
# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

### Teoria:

- Al declarar `email = forms.EmailField(required=True)` **fuera** de `Meta`, sobreescribes el campo que Django genera automaticamente.
- `EmailField` valida que el texto tenga formato de email (algo@algo.algo).
- `required=True` hace que Django rechace el formulario si el campo esta vacio.

---

## Resumen de archivos modificados/creados

| Archivo | Accion |
|---|---|
| `users/forms.py` | **Crear** — Define `RegisterForm` basado en `UserCreationForm` |
| `users/views.py` | **Modificar** — Agregar funcion `register` con logica de registro y login automatico |
| `config/urls.py` | **Modificar** — Agregar `path('register/', ...)` |
| `templates/register.html` | **Crear** — Formulario de registro con enlace a login |
| `templates/login.html` | **Modificar** — Agregar enlace "Registrate aqui" |

---

## Comparacion: LoginView vs vista register

| Aspecto | Login | Registro |
|---|---|---|
| Tipo de vista | CBV built-in (`LoginView`) | FBV custom (funcion `register`) |
| Formulario | `AuthenticationForm` (automatico) | `RegisterForm` (custom, basado en `UserCreationForm`) |
| Logica | Django la maneja toda | Tu la escribes en la vista |
| Por que? | Login es estandar, no hay nada que personalizar | Registro varia entre proyectos (campos extra, validaciones, etc.) |
