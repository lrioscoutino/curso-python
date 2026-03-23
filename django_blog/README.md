# Tutorial: Blog con CRUD completo en Django

## ¿Qué vamos a construir?

Un blog funcional donde los usuarios pueden crear, leer, editar y eliminar posts. Usaremos **Class-Based Views (CBV)**, relaciones entre modelos y URLs amigables con slugs.

| Concepto | Detalle |
|----------|---------|
| `ListView`, `DetailView` | Vistas genéricas para listar y ver detalle |
| `CreateView`, `UpdateView`, `DeleteView` | CRUD completo con CBV |
| `ForeignKey` | Relación Post → Autor |
| `ManyToManyField` | Tags en los posts |
| `SlugField` | URLs amigables (`/blog/mi-primer-post/`) |
| Paginación | `paginate_by` en ListView |
| `LoginRequiredMixin` | Solo usuarios autenticados crean posts |
| `UserPassesTestMixin` | Solo el autor puede editar/eliminar |
| Template inheritance | `base.html` con bloques reutilizables |

## Flujo de la aplicación

```
Visitante                          Usuario autenticado
    │                                      │
    ▼                                      ▼
┌──────────────┐                 ┌──────────────────┐
│ Listado de   │                 │ Crear nuevo post  │
│ posts        │                 └────────┬─────────┘
└──────┬───────┘                          │
       │                                  ▼
       ▼                         ┌──────────────────┐
┌──────────────┐                 │ Editar post       │ ← solo el autor
│ Detalle del  │                 └────────┬─────────┘
│ post         │                          │
└──────────────┘                          ▼
                                 ┌──────────────────┐
                                 │ Eliminar post     │ ← confirmación
                                 └──────────────────┘
```

---

## Paso 1: Crear la app y configurarla

```bash
python3 manage.py startapp blog
```

### `settings.py`

```python
INSTALLED_APPS = [
    # ...
    'blog',
]
```

---

## Paso 2: Crear los modelos

### `blog/models.py`

```python
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    """Etiqueta para clasificar posts."""
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Entrada del blog."""

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        PUBLISHED = 'published', 'Publicado'

    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text='Se genera automáticamente del título'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Autor'
    )
    body = models.TextField(verbose_name='Contenido')
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name='Etiquetas'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
```

### Crear y aplicar migraciones

```bash
python3 manage.py makemigrations blog
python3 manage.py migrate
```

### Conceptos clave de los modelos

| Concepto | Explicación |
|----------|-------------|
| `ForeignKey` | Muchos posts pueden pertenecer a un autor. `on_delete=CASCADE` elimina los posts si se elimina el usuario |
| `ManyToManyField` | Un post puede tener muchas etiquetas, y una etiqueta puede estar en muchos posts |
| `SlugField` | Campo optimizado para URLs. Solo permite letras, números, guiones y guiones bajos |
| `slugify()` | Convierte "Mi Primer Post" → "mi-primer-post" |
| `TextChoices` | Enum de Django para opciones con tipo seguro. Reemplaza las tuplas clásicas de `choices` |
| `auto_now_add` | Guarda la fecha solo al crear el registro |
| `auto_now` | Actualiza la fecha cada vez que se guarda |
| `get_absolute_url()` | Convención de Django — retorna la URL canónica del objeto. Las CBV la usan automáticamente después de crear/editar |

### ¿Cómo funciona `ForeignKey`?

```
User (tabla auth_user)          Post (tabla blog_post)
┌────┬──────────┐              ┌────┬──────────┬───────────┐
│ id │ username │              │ id │ title    │ author_id │
├────┼──────────┤              ├────┼──────────┼───────────┤
│  1 │ luis     │◄─────────────│  1 │ Post A   │     1     │
│    │          │◄─────────────│  2 │ Post B   │     1     │
│  2 │ maria    │◄─────────────│  3 │ Post C   │     2     │
└────┴──────────┘              └────┴──────────┴───────────┘

# Acceso desde Python:
post.author              → User(username='luis')
user.posts.all()         → [Post A, Post B]  (gracias a related_name='posts')
```

### ¿Cómo funciona `ManyToManyField`?

```
Post                    blog_post_tags (tabla intermedia)         Tag
┌────┬────────┐        ┌─────────┬────────┐                ┌────┬──────────┐
│ id │ title  │        │ post_id │ tag_id │                │ id │ name     │
├────┼────────┤        ├─────────┼────────┤                ├────┼──────────┤
│  1 │ Post A │◄───────│    1    │   1    │───────────────►│  1 │ Python   │
│    │        │◄───────│    1    │   2    │───────────────►│  2 │ Django   │
│  2 │ Post B │◄───────│    2    │   2    │───────────────►│    │          │
└────┴────────┘        └─────────┴────────┘                └────┴──────────┘

# Post A tiene tags: Python, Django
# Post B tiene tags: Django

post.tags.all()          → [Python, Django]
tag.posts.all()          → [Post A]  (gracias a related_name='posts')
```

> Django crea automáticamente la tabla intermedia `blog_post_tags`. No necesitas definirla manualmente.

---

## Paso 3: Crear los formularios

### `blog/forms.py`

```python
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Título del post'}
            ),
            'body': forms.Textarea(
                attrs={
                    'rows': 10,
                    'placeholder': 'Escribe tu contenido aquí...'
                }
            ),
            'tags': forms.CheckboxSelectMultiple(),
        }
```

### ¿Por qué no incluimos `author` ni `slug` en el formulario?

| Campo | Razón |
|-------|-------|
| `author` | Se asigna automáticamente en la vista (`request.user`) — el usuario no debe elegir quién es el autor |
| `slug` | Se genera automáticamente del título en `save()` |

### Widget `CheckboxSelectMultiple`

En lugar de un `<select multiple>` (difícil de usar), las etiquetas se muestran como checkboxes:

```
☑ Python
☑ Django
☐ JavaScript
☐ DevOps
```

---

## Paso 4: Crear las vistas (Class-Based Views)

### `blog/views.py`

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    """Lista todos los posts publicados con paginación."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related('author').prefetch_related('tags')


class PostDetailView(DetailView):
    """Muestra el detalle de un post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Si el usuario es el autor, puede ver borradores
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                models.Q(status=Post.Status.PUBLISHED) |
                models.Q(author=self.request.user)
            )
        return Post.objects.filter(status=Post.Status.PUBLISHED)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Crea un nuevo post. Requiere autenticación."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edita un post existente. Solo el autor puede editar."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Elimina un post. Pide confirmación. Solo el autor puede eliminar."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

### Agregar import faltante

Nota: En `PostDetailView.get_queryset` usamos `models.Q`. Agrega el import al inicio:

```python
from django.db import models
```

### ¿Qué son las Class-Based Views (CBV)?

Django ofrece dos formas de escribir vistas:

```python
# Function-Based View (FBV) — lo que usaste en tutoriales anteriores
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# Class-Based View (CBV) — menos código, más reutilizable
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
```

| FBV | CBV |
|-----|-----|
| Explícitas, fáciles de leer | Menos código para patrones comunes |
| Más control manual | Reutilizables vía herencia y mixins |
| Buenas para lógica única/especial | Ideales para CRUD estándar |

### ¿Cómo funcionan los Mixins?

Los mixins añaden comportamiento a las vistas sin duplicar código:

```
LoginRequiredMixin          UserPassesTestMixin          UpdateView
       │                           │                         │
       ▼                           ▼                         ▼
  "¿Está logueado?"     "¿Pasa el test_func()?"      "Lógica de edición"
       │                           │                         │
       └───────────────┬───────────┘─────────────────────────┘
                       ▼
              PostUpdateView
              (tiene las 3 cosas)
```

> **Orden importante:** Los mixins van **antes** de la vista base. Python los lee de izquierda a derecha.
> `LoginRequiredMixin, UserPassesTestMixin, UpdateView` — correcto
> `UpdateView, LoginRequiredMixin` — **incorrecto**, el mixin no se aplicaría

### Tabla de vistas y sus atributos

| Vista | Hereda de | Qué hace | Atributo clave |
|-------|-----------|----------|----------------|
| `PostListView` | `ListView` | Lista paginada | `paginate_by`, `get_queryset()` |
| `PostDetailView` | `DetailView` | Detalle de un objeto | `slug_field` (por defecto `'slug'`) |
| `PostCreateView` | `CreateView` | Formulario + crear | `form_valid()` para asignar autor |
| `PostUpdateView` | `UpdateView` | Formulario + editar | `test_func()` para verificar autor |
| `PostDeleteView` | `DeleteView` | Confirmación + eliminar | `success_url` con `reverse_lazy` |

### ¿Por qué `reverse_lazy` y no `reverse`?

```python
# reverse() se ejecuta al importar el módulo
# En ese momento las URLs pueden no estar cargadas → error

# reverse_lazy() se ejecuta solo cuando se necesita el valor
# Seguro para atributos de clase
success_url = reverse_lazy('post_list')  # ← correcto en atributos de clase
```

### ¿Qué son `select_related` y `prefetch_related`?

```python
# SIN optimización — 1 query por post para obtener el autor (problema N+1)
Post.objects.all()
# SELECT * FROM blog_post
# SELECT * FROM auth_user WHERE id = 1  ← por cada post
# SELECT * FROM auth_user WHERE id = 2
# ...

# CON select_related — 1 sola query con JOIN (para ForeignKey)
Post.objects.select_related('author')
# SELECT * FROM blog_post INNER JOIN auth_user ON ...

# CON prefetch_related — 2 queries (para ManyToMany)
Post.objects.prefetch_related('tags')
# SELECT * FROM blog_post
# SELECT * FROM blog_tag INNER JOIN blog_post_tags ON ... WHERE post_id IN (1, 2, 3)
```

| Método | Tipo de relación | Estrategia |
|--------|------------------|------------|
| `select_related` | `ForeignKey`, `OneToOneField` | SQL JOIN en una sola query |
| `prefetch_related` | `ManyToManyField`, relaciones inversas | Query separada + unión en Python |

---

## Paso 5: Configurar las URLs

### `blog/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.PostListView.as_view(),
        name='post_list'
    ),
    path(
        'post/<slug:slug>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'post/new/',
        views.PostCreateView.as_view(),
        name='post_create'
    ),
    path(
        'post/<slug:slug>/edit/',
        views.PostUpdateView.as_view(),
        name='post_update'
    ),
    path(
        'post/<slug:slug>/delete/',
        views.PostDeleteView.as_view(),
        name='post_delete'
    ),
]
```

### `urls.py` (proyecto principal)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    # ... otras urls ...
]
```

### ¿Qué es `<slug:slug>`?

```
URL: /blog/post/mi-primer-post/
                 ^^^^^^^^^^^^^^
                 └── capturado por <slug:slug>

<slug:slug>
  │     │
  │     └── nombre del argumento pasado a la vista (coincide con Post.slug)
  └── tipo de convertidor (solo acepta letras, números, guiones y _)
```

> **Cuidado con el orden:** `post/new/` debe ir **antes** de `post/<slug:slug>/`. Si no, Django intentaría buscar un post con slug="new".

---

## Paso 6: Crear los templates

### 6.0 Template base — `blog/base.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blog{% endblock %}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            background-color: #fafafa;
        }
        nav {
            background-color: #2c3e50;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        nav a { color: #ecf0f1; text-decoration: none; margin-right: 15px; }
        nav a:hover { color: #3498db; }
        .nav-brand { font-size: 20px; font-weight: bold; }
        .container {
            max-width: 800px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 14px;
            cursor: pointer;
            border: none;
        }
        .btn-primary { background-color: #3498db; color: white; }
        .btn-primary:hover { background-color: #2980b9; }
        .btn-danger { background-color: #e74c3c; color: white; }
        .btn-danger:hover { background-color: #c0392b; }
        .btn-secondary { background-color: #95a5a6; color: white; }
        .btn-secondary:hover { background-color: #7f8c8d; }
        .messages { margin-bottom: 20px; }
        .message-success {
            background-color: #e8f5e9;
            border: 1px solid #4CAF50;
            padding: 10px 15px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .message-error {
            background-color: #ffebee;
            border: 1px solid #e74c3c;
            padding: 10px 15px;
            border-radius: 4px;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav>
        <div>
            <a href="{% url 'post_list' %}" class="nav-brand">Blog</a>
        </div>
        <div>
            {% if user.is_authenticated %}
                <a href="{% url 'post_create' %}">Nuevo Post</a>
                <a href="#">{{ user.username }}</a>
            {% else %}
                <a href="{% url 'login' %}">Iniciar sesión</a>
            {% endif %}
        </div>
    </nav>

    <div class="container">
        {% if messages %}
            <div class="messages">
                {% for message in messages %}
                    <div class="message-{{ message.tags }}">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}

        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### ¿Cómo funciona la herencia de templates?

```
base.html (define la estructura y bloques)
    │
    ├── {% block title %}Blog{% endblock %}        ← valor por defecto
    ├── {% block extra_css %}{% endblock %}         ← vacío por defecto
    └── {% block content %}{% endblock %}           ← vacío por defecto

post_list.html (extiende base.html y llena los bloques)
    │
    ├── {% block title %}Posts{% endblock %}        ← reemplaza "Blog" por "Posts"
    └── {% block content %}                         ← llena el contenido
            <h1>Lista de posts...</h1>
        {% endblock %}
```

> **Regla:** `{% extends "blog/base.html" %}` debe ser la **primera línea** del template hijo. Todo contenido debe ir dentro de un `{% block %}`.

---

### 6.1 Lista de posts — `blog/post_list.html`

```html
{% extends "blog/base.html" %}

{% block title %}Posts{% endblock %}

{% block extra_css %}
<style>
    .post-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .post-card h2 { margin-bottom: 10px; }
    .post-card h2 a { color: #2c3e50; text-decoration: none; }
    .post-card h2 a:hover { color: #3498db; }
    .post-meta {
        color: #7f8c8d;
        font-size: 14px;
        margin-bottom: 15px;
    }
    .post-excerpt {
        color: #555;
        margin-bottom: 15px;
    }
    .tag {
        display: inline-block;
        background-color: #ecf0f1;
        color: #2c3e50;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 5px;
    }
    .pagination {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 30px;
    }
    .pagination a, .pagination span {
        padding: 8px 16px;
        border: 1px solid #ddd;
        border-radius: 4px;
        text-decoration: none;
        color: #333;
    }
    .pagination .current {
        background-color: #3498db;
        color: white;
        border-color: #3498db;
    }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #999;
    }
</style>
{% endblock %}

{% block content %}
    <h1>Posts</h1>

    {% if posts %}
        {% for post in posts %}
            <article class="post-card">
                <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
                <div class="post-meta">
                    Por {{ post.author.get_full_name|default:post.author.username }}
                    &middot; {{ post.created_at|date:"d M Y" }}
                </div>
                <p class="post-excerpt">{{ post.body|truncatewords:30 }}</p>
                {% if post.tags.all %}
                    <div>
                        {% for tag in post.tags.all %}
                            <span class="tag">{{ tag.name }}</span>
                        {% endfor %}
                    </div>
                {% endif %}
            </article>
        {% endfor %}

        <!-- Paginación -->
        {% if is_paginated %}
            <div class="pagination">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}">&laquo; Anterior</a>
                {% endif %}

                {% for num in page_obj.paginator.page_range %}
                    {% if page_obj.number == num %}
                        <span class="current">{{ num }}</span>
                    {% elif num > page_obj.number|add:"-3" and num < page_obj.number|add:"3" %}
                        <a href="?page={{ num }}">{{ num }}</a>
                    {% endif %}
                {% endfor %}

                {% if page_obj.has_next %}
                    <a href="?page={{ page_obj.next_page_number }}">Siguiente &raquo;</a>
                {% endif %}
            </div>
        {% endif %}
    {% else %}
        <div class="empty-state">
            <h2>No hay posts publicados</h2>
            <p>Sé el primero en escribir algo.</p>
            {% if user.is_authenticated %}
                <a href="{% url 'post_create' %}" class="btn btn-primary" style="margin-top: 15px;">
                    Crear post
                </a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

### Variables de paginación que provee `ListView`

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `posts` | `QuerySet` | Los objetos de la página actual (definido por `context_object_name`) |
| `page_obj` | `Page` | Objeto de la página actual |
| `page_obj.number` | `int` | Número de página actual |
| `page_obj.has_previous` | `bool` | ¿Hay página anterior? |
| `page_obj.has_next` | `bool` | ¿Hay página siguiente? |
| `page_obj.paginator.page_range` | `range` | Rango de todas las páginas |
| `is_paginated` | `bool` | `True` si hay más de una página |

---

### 6.2 Detalle del post — `blog/post_detail.html`

```html
{% extends "blog/base.html" %}

{% block title %}{{ post.title }}{% endblock %}

{% block extra_css %}
<style>
    .post-header { margin-bottom: 30px; }
    .post-header h1 { font-size: 32px; margin-bottom: 10px; }
    .post-meta { color: #7f8c8d; font-size: 14px; }
    .post-body {
        font-size: 18px;
        line-height: 1.8;
        margin-bottom: 30px;
        white-space: pre-wrap;
    }
    .post-tags { margin-bottom: 30px; }
    .tag {
        display: inline-block;
        background-color: #ecf0f1;
        color: #2c3e50;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 5px;
    }
    .post-actions {
        border-top: 1px solid #eee;
        padding-top: 20px;
        display: flex;
        gap: 10px;
    }
    .draft-badge {
        display: inline-block;
        background-color: #f39c12;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        margin-left: 10px;
        vertical-align: middle;
    }
</style>
{% endblock %}

{% block content %}
    <article>
        <div class="post-header">
            <h1>
                {{ post.title }}
                {% if post.status == 'draft' %}
                    <span class="draft-badge">Borrador</span>
                {% endif %}
            </h1>
            <div class="post-meta">
                Por {{ post.author.get_full_name|default:post.author.username }}
                &middot; {{ post.created_at|date:"d M Y, H:i" }}
                {% if post.updated_at != post.created_at %}
                    &middot; Editado {{ post.updated_at|date:"d M Y, H:i" }}
                {% endif %}
            </div>
        </div>

        <div class="post-body">{{ post.body }}</div>

        {% if post.tags.all %}
            <div class="post-tags">
                {% for tag in post.tags.all %}
                    <span class="tag">{{ tag.name }}</span>
                {% endfor %}
            </div>
        {% endif %}

        {% if user == post.author %}
            <div class="post-actions">
                <a href="{% url 'post_update' post.slug %}" class="btn btn-primary">Editar</a>
                <a href="{% url 'post_delete' post.slug %}" class="btn btn-danger">Eliminar</a>
            </div>
        {% endif %}
    </article>

    <div style="margin-top: 30px;">
        <a href="{% url 'post_list' %}">&larr; Volver a la lista</a>
    </div>
{% endblock %}
```

---

### 6.3 Formulario de crear/editar — `blog/post_form.html`

```html
{% extends "blog/base.html" %}

{% block title %}
    {% if object %}Editar: {{ object.title }}{% else %}Nuevo Post{% endif %}
{% endblock %}

{% block extra_css %}
<style>
    .form-group { margin-bottom: 20px; }
    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
        color: #2c3e50;
    }
    .form-group input[type="text"],
    .form-group textarea,
    .form-group select {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 16px;
        font-family: inherit;
    }
    .form-group textarea { resize: vertical; }
    .form-group .helptext { font-size: 12px; color: #999; margin-top: 4px; }
    .form-group .error { color: #e74c3c; font-size: 14px; }
    .form-group ul { list-style: none; padding: 0; }
    .form-group ul li { margin-bottom: 5px; }
    .form-actions { display: flex; gap: 10px; margin-top: 20px; }
</style>
{% endblock %}

{% block content %}
    <h1>{% if object %}Editar Post{% else %}Nuevo Post{% endif %}</h1>

    <form method="post">
        {% csrf_token %}

        {% for field in form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}:</label>
                {{ field }}
                {% if field.help_text %}
                    <div class="helptext">{{ field.help_text }}</div>
                {% endif %}
                {% if field.errors %}
                    {% for error in field.errors %}
                        <div class="error">{{ error }}</div>
                    {% endfor %}
                {% endif %}
            </div>
        {% endfor %}

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">
                {% if object %}Guardar cambios{% else %}Publicar{% endif %}
            </button>
            <a href="{% url 'post_list' %}" class="btn btn-secondary">Cancelar</a>
        </div>
    </form>
{% endblock %}
```

### ¿Cómo sabe el template si es crear o editar?

Las CBV pasan automáticamente la variable `object`:

| Situación | `object` | Resultado |
|-----------|----------|-----------|
| `CreateView` | `None` | "Nuevo Post" |
| `UpdateView` | El post existente | "Editar: Mi Post" |

> **Reutilización:** Un solo template sirve para crear y editar. Django se encarga de diferenciar el comportamiento.

---

### 6.4 Confirmar eliminación — `blog/post_confirm_delete.html`

```html
{% extends "blog/base.html" %}

{% block title %}Eliminar: {{ post.title }}{% endblock %}

{% block extra_css %}
<style>
    .delete-card {
        background: white;
        border: 2px solid #e74c3c;
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        margin-top: 40px;
    }
    .delete-card h2 { color: #e74c3c; margin-bottom: 15px; }
    .delete-card p { margin-bottom: 25px; color: #555; }
    .delete-actions { display: flex; justify-content: center; gap: 15px; }
</style>
{% endblock %}

{% block content %}
    <div class="delete-card">
        <h2>¿Eliminar este post?</h2>
        <p>Estás a punto de eliminar "<strong>{{ post.title }}</strong>". Esta acción no se puede deshacer.</p>

        <form method="post">
            {% csrf_token %}
            <div class="delete-actions">
                <button type="submit" class="btn btn-danger">Sí, eliminar</button>
                <a href="{{ post.get_absolute_url }}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
{% endblock %}
```

> **¿Por qué la confirmación?** `DeleteView` muestra esta página con GET. Solo al enviar el formulario (POST) se elimina el objeto. Esto previene eliminaciones accidentales.

---

## Paso 7: Registrar en el Admin

### `blog/admin.py`

```python
from django.contrib import admin
from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'tags']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
```

### Atributos útiles del ModelAdmin

| Atributo | Qué hace |
|----------|----------|
| `list_display` | Columnas visibles en la lista |
| `list_filter` | Filtros en la barra lateral |
| `search_fields` | Campos incluidos en la búsqueda |
| `prepopulated_fields` | Auto-llena el slug mientras escribes el título |
| `date_hierarchy` | Navegación por fecha arriba de la lista |

---

## Paso 8: Estructura final de archivos

```
blog/
├── templates/
│   └── blog/
│       ├── base.html                 ← template padre
│       ├── post_list.html            ← listado con paginación
│       ├── post_detail.html          ← detalle del post
│       ├── post_form.html            ← crear y editar (compartido)
│       └── post_confirm_delete.html  ← confirmación de eliminar
├── __init__.py
├── admin.py                          ← registro de Post y Tag
├── apps.py
├── forms.py                          ← PostForm
├── models.py                         ← Post y Tag
├── urls.py                           ← rutas del blog
└── views.py                          ← CBVs (List, Detail, Create, Update, Delete)
```

---

## Paso 9: Probar

### 1. Crear migraciones y migrar

```bash
python3 manage.py makemigrations blog
python3 manage.py migrate
```

### 2. Crear etiquetas desde el admin

Visita `/admin/` y crea algunas etiquetas: Python, Django, Tutorial, etc.

### 3. Crear un post

Visita `/blog/post/new/`, llena el formulario y publica.

### 4. Verificar la lista

Visita `/blog/` y confirma que tu post aparece.

### 5. Verificar permisos

- Cierra sesión e intenta acceder a `/blog/post/new/` → debe redirigir al login.
- Con otro usuario, intenta editar un post ajeno → debe mostrar 403 Forbidden.

### 6. Probar paginación

Crea más de 5 posts publicados y verifica que aparecen los controles de paginación.

---

## Resumen

| Concepto | Detalle |
|----------|---------|
| **Modelos** | `Post` con `ForeignKey` a User + `ManyToManyField` a `Tag` |
| **CBV** | `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` |
| **Slugs** | URLs amigables generadas automáticamente del título |
| **Paginación** | `paginate_by = 5` en ListView |
| **Permisos** | `LoginRequiredMixin` + `UserPassesTestMixin` (solo el autor edita/elimina) |
| **Optimización** | `select_related` y `prefetch_related` para evitar N+1 queries |
| **Templates** | Herencia con `base.html` + bloques reutilizables |
| **Admin** | `prepopulated_fields` para auto-generar slugs |
