# Tutorial: Login y Logout con LoginView y LogoutView en Django

## Teoria: Que son LoginView y LogoutView?

Son **vistas basadas en clase (CBV)** que Django incluye en `django.contrib.auth.views`. Hacen todo el trabajo pesado por ti:

| Clase | Que hace? |
|---|---|
| `LoginView` | Muestra un formulario de login, valida credenciales, crea la sesion del usuario y lo redirige |
| `LogoutView` | Destruye la sesion del usuario y lo redirige |

**Por que usarlas?** Porque ya manejan internamente: validacion de credenciales, proteccion CSRF, mensajes de error, y manejo de sesiones. No necesitas escribir esa logica manualmente.

---

## Paso 1: Configurar settings.py

Django necesita saber **a donde redirigir** despues del login y logout. Agrega estas dos lineas al final de `settings.py`:

```python
# config/settings.py

LOGIN_REDIRECT_URL = 'inicio'   # A donde va despues de loguearse
LOGOUT_REDIRECT_URL = 'login'   # A donde va despues de cerrar sesion
```

**Teoria**: `LOGIN_REDIRECT_URL` acepta un **nombre de URL** (el `name` que defines en `path()`). Si no la configuras, Django redirige a `/accounts/profile/` por defecto, que no existe y da error 404.

---

## Paso 2: Configurar las URLs

Reemplazar la vista `login` manual por `LoginView` y agregar `LogoutView`:

```python
# config/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import index, inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('inicio/', inicio, name='inicio'),

    # LOGIN: usa LoginView con tu template personalizado
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    # LOGOUT: usa LogoutView (no necesita template)
    path('logout/', LogoutView.as_view(), name='logout'),
]
```

### Teoria - puntos clave:

- `LoginView.as_view(template_name='login.html')` le dice a Django: "usa MI template, no el default".
- Por defecto `LoginView` busca el template en `registration/login.html`. Con `template_name` lo sobreescribes.
- `LogoutView` no necesita template, solo destruye la sesion y redirige a `LOGOUT_REDIRECT_URL`.
- Ya **no necesitas** la funcion `login` en `views.py` porque `LoginView` la reemplaza.

---

## Paso 3: El Template login.html

`LoginView` inyecta automaticamente una variable llamada `form` en el contexto del template. Este `form` es una instancia de `AuthenticationForm` que tiene los campos `username` y `password`.

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

    {# Mostrar errores de autenticacion #}
    {% if form.errors %}
        <p style="color: red;">Usuario o contrasena incorrectos.</p>
    {% endif %}

    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Entrar</button>
    </form>
{% endif %}

</body>
</html>
```

### Teoria - puntos clave del template:

1. **`method="post"`** — El formulario DEBE ser POST. Un GET no envia credenciales de forma segura.

2. **`{% csrf_token %}`** — Obligatorio. Django rechaza cualquier POST sin este token (proteccion contra ataques CSRF).

3. **`{{ form.as_p }}`** — Renderiza los campos del formulario envueltos en `<p>`. Django genera los `<input>` con los `name` correctos (`username`, `password`), labels, y validaciones. Alternativas: `form.as_div`, `form.as_table`, o renderizar campo por campo.

4. **`form.errors`** — Si el login falla (credenciales incorrectas), `LoginView` re-renderiza el template con los errores en `form.errors`.

---

## Paso 4: Actualizar base.html con enlace de logout

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Titulo de la pagina</title>
</head>
<body>
<h1>Hola Mundo</h1>
{{ name }}
{{ age }}
{{ message }}

{% for item in example_list %}
    {{ item }}<br>
{% endfor %}

{% if request.user.is_authenticated %}
    <p>Usuario: {{ request.user.username }}</p>
    <a href="{% url 'logout' %}">Cerrar sesion</a>
{% else %}
    <a href="{% url 'login' %}">Iniciar sesion</a>
{% endif %}
</body>
</html>
```

---

## Paso 5: Limpiar views.py

Ya no necesitas la funcion `login` porque `LoginView` la reemplaza:

```python
# users/views.py

from django.http import HttpResponse
from django.shortcuts import render

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
```

---

## Paso 6: Crear un superusuario para probar

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
```

---

## Paso 7: Probar

```bash
python3 manage.py runserver
```

1. Ir a `http://127.0.0.1:8000/login/` — Veras el formulario
2. Ingresar las credenciales del superusuario — Te redirige a `/inicio/`
3. Ir a `http://127.0.0.1:8000/inicio/` — Veras "Usuario: tu_nombre" y el enlace "Cerrar sesion"
4. Click en "Cerrar sesion" — Te redirige de vuelta a `/login/`

---

## Flujo completo (lo que pasa internamente)

```
Usuario visita /login/
        |
        v
   +-------------+
   |  LoginView   |---- GET ----> Renderiza login.html con form vacio
   +-------------+
        |
      POST (usuario envia credenciales)
        |
        v
   Credenciales validas?
    /            \
  SI              NO
   |               |
   v               v
auth.login()    Re-renderiza login.html
(crea sesion)   con form.errors
   |
   v
Redirect a LOGIN_REDIRECT_URL ('inicio')

------------------------------------

Usuario hace click en "Cerrar sesion"
        |
        v
   +--------------+
   |  LogoutView   |--> auth.logout() (destruye sesion)
   +--------------+          |
                             v
                    Redirect a LOGOUT_REDIRECT_URL ('login')
```

---

## Extra: Renderizar campos individualmente

Si quieres mas control sobre el HTML en vez de `{{ form.as_p }}`:

```html
<form method="post">
    {% csrf_token %}

    <div>
        <label for="{{ form.username.id_for_label }}">Usuario:</label>
        {{ form.username }}
        {% for error in form.username.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>

    <div>
        <label for="{{ form.password.id_for_label }}">Contrasena:</label>
        {{ form.password }}
        {% for error in form.password.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>

    {% if form.non_field_errors %}
        {% for error in form.non_field_errors %}
            <p style="color: red;">{{ error }}</p>
        {% endfor %}
    {% endif %}

    <button type="submit">Entrar</button>
</form>
```

**`non_field_errors`** son errores que no pertenecen a un campo especifico (como "credenciales incorrectas").

---

## Resumen de archivos modificados

| Archivo | Accion |
|---|---|
| `config/settings.py` | Agregar `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL` |
| `config/urls.py` | Reemplazar vista `login` por `LoginView`, agregar `LogoutView` |
| `templates/login.html` | Agregar `method="post"`, `{% csrf_token %}`, `{{ form.as_p }}` |
| `templates/base.html` | Agregar enlace de logout con `{% url 'logout' %}` |
| `users/views.py` | Eliminar la funcion `login` (ya no se necesita) |
