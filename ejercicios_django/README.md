# Ejercicios de Django

## Ejercicio 1: Configuración inicial y "Hello World"

1. Instala Django usando pip: `pip install django`
2. Crea un nuevo proyecto Django: `django-admin startproject mi_proyecto`
3. Navega al directorio del proyecto: `cd mi_proyecto`
4. Crea una nueva aplicación: `python manage.py startapp mi_app`
5. En `mi_app/views.py`, crea una vista simple:

```python
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("¡Hola, mundo!")
```

6. En `mi_proyecto/urls.py`, agrega la URL para esta vista:

```python
from django.urls import path
from mi_app.views import hello_world

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
]
```

7. Ejecuta el servidor de desarrollo: `python manage.py runserver`
8. Visita `http://localhost:8000/hello/` en tu navegador

## Ejercicio 2: Modelos y migraciones

1. En `mi_app/models.py`, crea un modelo simple:

```python
from django.db import models

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    completada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

2. Crea las migraciones: `python manage.py makemigrations`
3. Aplica las migraciones: `python manage.py migrate`

## Ejercicio 3: Vistas basadas en clases y templates

1. Crea un directorio `templates` en tu aplicación y dentro de él un archivo `lista_tareas.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Lista de Tareas</title>
</head>
<body>
    <h1>Mis Tareas</h1>
    <ul>
    {% for tarea in tareas %}
        <li>{{ tarea.titulo }} - {% if tarea.completada %}Completada{% else %}Pendiente{% endif %}</li>
    {% empty %}
        <li>No hay tareas aún.</li>
    {% endfor %}
    </ul>
</body>
</html>
```

2. En `views.py`, crea una vista basada en clase:

```python
from django.views.generic import ListView
from .models import Tarea

class ListaTareasView(ListView):
    model = Tarea
    template_name = 'lista_tareas.html'
    context_object_name = 'tareas'
```

3. Actualiza `urls.py` para usar esta nueva vista:

```python
from django.urls import path
from mi_app.views import ListaTareasView

urlpatterns = [
    path('tareas/', ListaTareasView.as_view(), name='lista_tareas'),
]
```

## Ejercicio 4: Formularios y creación de objetos

1. Crea un archivo `forms.py` en tu aplicación:

```python
from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion']
```

2. Crea una nueva vista en `views.py`:

```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Tarea
from .forms import TareaForm

class CrearTareaView(CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'crear_tarea.html'
    success_url = reverse_lazy('lista_tareas')
```

3. Crea un template `crear_tarea.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Crear Tarea</title>
</head>
<body>
    <h1>Crear Nueva Tarea</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Crear Tarea</button>
    </form>
</body>
</html>
```

4. Agrega la URL para esta nueva vista en `urls.py`:

```python
path('tareas/crear/', CrearTareaView.as_view(), name='crear_tarea'),
```

## Ejercicio 5: Autenticación de usuarios

1. Crea una vista para el login en `views.py`:

```python
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('lista_tareas')
```

2. Crea un template `login.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Iniciar Sesión</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

3. Agrega la URL para el login en `urls.py`:

```python
path('login/', CustomLoginView.as_view(), name='login'),
```

4. Protege las vistas que requieren autenticación usando el decorador `@login_required` o heredando de `LoginRequiredMixin` para vistas basadas en clases.

Estos ejercicios te darán una buena base para trabajar con Django, cubriendo aspectos como modelos, vistas, templates, formularios y autenticación básica.
