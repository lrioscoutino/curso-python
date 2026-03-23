# Tutorial: Permisos y Roles en Django

## ¿Qué es el sistema de permisos de Django?

Django incluye un sistema de permisos completo que controla **quién puede hacer qué** en tu aplicación.

| Componente | Descripción |
|------------|-------------|
| **Permission** | Permiso individual (ej: "puede crear artículo") |
| **Group** | Conjunto de permisos asignados a un rol (ej: "Editor") |
| **User.is_staff** | Puede acceder al admin |
| **User.is_superuser** | Tiene **todos** los permisos automáticamente |

## Permisos automáticos

Django crea **4 permisos por cada modelo** automáticamente:

```
app_label.add_modelo      ← Crear
app_label.view_modelo     ← Ver
app_label.change_modelo   ← Modificar
app_label.delete_modelo   ← Eliminar
```

Por ejemplo, para un modelo `Article` en la app `blog`:

```
blog.add_article
blog.view_article
blog.change_article
blog.delete_article
```

---

## Paso 1: Crear una app de ejemplo

Vamos a crear una app `blog` con un modelo `Article` para practicar permisos.

### `blog/models.py`

```python
from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Autor'
    )
    published = models.BooleanField(default=False, verbose_name='Publicado')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        # Permisos personalizados (además de los 4 automáticos)
        permissions = [
            ('publish_article', 'Puede publicar artículos'),
            ('feature_article', 'Puede destacar artículos'),
        ]

    def __str__(self):
        return self.title
```

```bash
python3 manage.py makemigrations blog
python3 manage.py migrate
```

### Permisos resultantes para Article

| Permiso | Origen |
|---------|--------|
| `blog.add_article` | Automático |
| `blog.view_article` | Automático |
| `blog.change_article` | Automático |
| `blog.delete_article` | Automático |
| `blog.publish_article` | **Personalizado** |
| `blog.feature_article` | **Personalizado** |

---

## Paso 2: Crear Grupos (roles)

### Opción A: Desde el Admin

1. Ve a `/admin/auth/group/`
2. Crea los grupos y asígnales permisos con el selector

### Opción B: Con un comando de gestión (recomendado)

### `blog/management/commands/setup_groups.py`

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Article


class Command(BaseCommand):
    help = 'Crea los grupos y permisos iniciales'

    def handle(self, *args, **options):
        ct = ContentType.objects.get_for_model(Article)

        # --- Grupo: Lector ---
        lector, created = Group.objects.get_or_create(name='Lector')
        lector.permissions.set([
            Permission.objects.get(codename='view_article', content_type=ct),
        ])
        self.stdout.write(f'Grupo "Lector": {"creado" if created else "actualizado"}')

        # --- Grupo: Escritor ---
        escritor, created = Group.objects.get_or_create(name='Escritor')
        escritor.permissions.set([
            Permission.objects.get(codename='view_article', content_type=ct),
            Permission.objects.get(codename='add_article', content_type=ct),
            Permission.objects.get(codename='change_article', content_type=ct),
        ])
        self.stdout.write(f'Grupo "Escritor": {"creado" if created else "actualizado"}')

        # --- Grupo: Editor ---
        editor, created = Group.objects.get_or_create(name='Editor')
        editor.permissions.set([
            Permission.objects.get(codename='view_article', content_type=ct),
            Permission.objects.get(codename='add_article', content_type=ct),
            Permission.objects.get(codename='change_article', content_type=ct),
            Permission.objects.get(codename='delete_article', content_type=ct),
            Permission.objects.get(codename='publish_article', content_type=ct),
            Permission.objects.get(codename='feature_article', content_type=ct),
        ])
        self.stdout.write(f'Grupo "Editor": {"creado" if created else "actualizado"}')

        self.stdout.write(self.style.SUCCESS('Grupos configurados correctamente.'))
```

```bash
python3 manage.py setup_groups
```

### Jerarquía de roles resultante

```
Editor (todos los permisos)
  │
  ├── Escritor (ver + crear + editar)
  │     │
  │     └── Lector (solo ver)
  │
  └── Publicar y Destacar (permisos exclusivos del Editor)
```

---

## Paso 3: Asignar usuarios a grupos

### Desde el shell

```python
python3 manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# Obtener usuario y grupo
user = User.objects.get(username='juan')
escritor = Group.objects.get(name='Escritor')

# Asignar usuario al grupo
user.groups.add(escritor)

# Verificar permisos
user.has_perm('blog.add_article')     # True (por grupo Escritor)
user.has_perm('blog.delete_article')  # False (no tiene ese permiso)
user.has_perm('blog.publish_article') # False

# Ver todos los permisos del usuario
user.get_all_permissions()
```

### Desde el Admin

1. Ve a `/admin/auth/user/`
2. Selecciona un usuario
3. En la sección "Grupos", asigna el grupo deseado

---

## Paso 4: Proteger vistas con Function-Based Views (FBV)

### `blog/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Article
from .forms import ArticleForm


# --- Solo requiere login ---
@login_required
def article_list(request):
    """Cualquier usuario autenticado puede ver la lista."""
    articles = Article.objects.filter(published=True)
    return render(request, 'blog/article_list.html', {'articles': articles})


# --- Requiere permiso específico ---
@permission_required('blog.add_article', raise_exception=True)
def article_create(request):
    """Solo usuarios con permiso 'add_article' pueden crear."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Artículo creado.')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


# --- Requiere login + permiso (combinados) ---
@login_required
@permission_required('blog.delete_article', raise_exception=True)
def article_delete(request, pk):
    """Solo usuarios con permiso 'delete_article' pueden eliminar."""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artículo eliminado.')
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})


# --- Permiso personalizado ---
@permission_required('blog.publish_article', raise_exception=True)
def article_publish(request, pk):
    """Solo Editores pueden publicar artículos."""
    article = get_object_or_404(Article, pk=pk)
    article.published = True
    article.save()
    messages.success(request, f'"{article.title}" ha sido publicado.')
    return redirect('article_list')
```

### Comparación de decoradores

| Decorador | Qué verifica | Si falla... |
|-----------|-------------|-------------|
| `@login_required` | ¿Está autenticado? | Redirige a `LOGIN_URL` |
| `@permission_required('perm')` | ¿Tiene el permiso? | Redirige a `LOGIN_URL` |
| `@permission_required('perm', raise_exception=True)` | ¿Tiene el permiso? | Responde **403 Forbidden** |

> **`raise_exception=True`** es importante: sin esto, un usuario autenticado sin permisos sería redirigido al login (confuso). Con esta opción, recibe un error 403 claro.

---

## Paso 5: Proteger vistas con Class-Based Views (CBV)

### `blog/views.py` (alternativa con CBV)

```python
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Article
from .forms import ArticleForm


class ArticleListView(LoginRequiredMixin, ListView):
    """Cualquier usuario autenticado puede ver la lista."""
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(published=True)


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    """Solo usuarios con permiso 'add_article' pueden crear."""
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    permission_required = 'blog.add_article'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    """Solo usuarios con permiso 'delete_article' pueden eliminar."""
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    permission_required = 'blog.delete_article'
    success_url = reverse_lazy('article_list')
```

### Comparación FBV vs CBV

| Aspecto | FBV (decoradores) | CBV (mixins) |
|---------|-------------------|--------------|
| Sintaxis | `@permission_required('perm')` | `permission_required = 'perm'` |
| Múltiples permisos | Apilar decoradores | `permission_required = ['perm1', 'perm2']` |
| Login + permiso | `@login_required` + `@permission_required` | `LoginRequiredMixin` + `PermissionRequiredMixin` |
| Orden | Decorador inferior se ejecuta primero | Mixin izquierdo tiene prioridad |

> **Orden de mixins:** Siempre pon `LoginRequiredMixin` o `PermissionRequiredMixin` **antes** de la vista base (ej: `ListView`). Los mixins se leen de izquierda a derecha.

---

## Paso 6: Verificar permisos en templates

### En cualquier template

```html
<!-- Verificar si el usuario está autenticado -->
{% if user.is_authenticated %}
    <p>Bienvenido, {{ user.username }}</p>
{% endif %}

<!-- Verificar un permiso específico -->
{% if perms.blog.add_article %}
    <a href="{% url 'article_create' %}">Nuevo artículo</a>
{% endif %}

{% if perms.blog.delete_article %}
    <a href="{% url 'article_delete' article.pk %}">Eliminar</a>
{% endif %}

{% if perms.blog.publish_article %}
    <a href="{% url 'article_publish' article.pk %}">Publicar</a>
{% endif %}

<!-- Verificar si pertenece a un grupo -->
<!-- Nota: no existe un tag built-in, pero puedes crear uno -->
```

### Ejemplo completo: lista de artículos

```html
<h2>Artículos</h2>

{% if perms.blog.add_article %}
    <a href="{% url 'article_create' %}" class="btn">Nuevo artículo</a>
{% endif %}

<table>
    <thead>
        <tr>
            <th>Título</th>
            <th>Autor</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        {% for article in articles %}
        <tr>
            <td>{{ article.title }}</td>
            <td>{{ article.author.username }}</td>
            <td>
                {% if perms.blog.change_article %}
                    <a href="{% url 'article_edit' article.pk %}">Editar</a>
                {% endif %}

                {% if perms.blog.delete_article %}
                    <a href="{% url 'article_delete' article.pk %}">Eliminar</a>
                {% endif %}

                {% if perms.blog.publish_article and not article.published %}
                    <a href="{% url 'article_publish' article.pk %}">Publicar</a>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

> **¿Cómo funciona `perms`?** Django inyecta automáticamente la variable `perms` en todos los templates (vía `django.contrib.auth.context_processors.auth`). No necesitas pasar nada extra desde la vista.

---

## Paso 7: Crear una página 403 personalizada

Cuando un usuario no tiene permisos y usas `raise_exception=True`, Django muestra una página 403. Personalízala:

### `templates/403.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso Denegado</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 100px auto;
            padding: 20px;
            text-align: center;
        }
        .error-code {
            font-size: 72px;
            font-weight: bold;
            color: #f44336;
            margin: 0;
        }
        .error-message {
            font-size: 20px;
            color: #555;
        }
        a {
            color: #4CAF50;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <p class="error-code">403</p>
    <p class="error-message">No tienes permiso para acceder a esta página.</p>
    <p><a href="/">Volver al inicio</a></p>
</body>
</html>
```

---

## Paso 8: Configurar URLs

### `blog/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/new/', views.article_create, name='article_create'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('articles/<int:pk>/publish/', views.article_publish, name='article_publish'),
]
```

---

## Paso 9: Formulario del artículo

### `blog/forms.py`

```python
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8}),
        }
```

---

## Paso 10: Probar

### 1. Configura grupos y permisos

```bash
python3 manage.py setup_groups
```

### 2. Crea usuarios de prueba

```bash
python3 manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# Crear usuarios
lector = User.objects.create_user('lector1', 'lector@test.com', 'pass1234')
escritor = User.objects.create_user('escritor1', 'escritor@test.com', 'pass1234')
editor = User.objects.create_user('editor1', 'editor@test.com', 'pass1234')

# Asignar grupos
lector.groups.add(Group.objects.get(name='Lector'))
escritor.groups.add(Group.objects.get(name='Escritor'))
editor.groups.add(Group.objects.get(name='Editor'))
```

### 3. Prueba cada rol

| Acción | Lector | Escritor | Editor |
|--------|--------|----------|--------|
| Ver artículos | Si | Si | Si |
| Crear artículo | **403** | Si | Si |
| Editar artículo | **403** | Si | Si |
| Eliminar artículo | **403** | **403** | Si |
| Publicar artículo | **403** | **403** | Si |

---

## Estructura final de archivos

```
blog/
├── management/
│   └── commands/
│       └── setup_groups.py       ← crear grupos y permisos
├── migrations/
├── templates/
│   └── blog/
│       ├── article_list.html     ← lista con botones según permisos
│       ├── article_form.html     ← crear/editar artículo
│       └── article_confirm_delete.html
├── __init__.py
├── admin.py
├── forms.py                      ← ArticleForm
├── models.py                     ← Article con permisos personalizados
├── urls.py
└── views.py                      ← vistas protegidas
templates/
└── 403.html                      ← página de acceso denegado
```

---

## Resumen

| Concepto | Detalle |
|----------|---------|
| Permisos automáticos | `add`, `view`, `change`, `delete` por cada modelo |
| Permisos personalizados | Definidos en `Meta.permissions` del modelo |
| Grupos | Conjuntos de permisos = roles (Lector, Escritor, Editor) |
| FBV | `@login_required`, `@permission_required` |
| CBV | `LoginRequiredMixin`, `PermissionRequiredMixin` |
| Templates | `{% if perms.app.codename %}` para mostrar/ocultar elementos |
| 403 | `raise_exception=True` + template `403.html` personalizado |
| Setup | Comando `setup_groups` para configuración reproducible |
