# Tutorial: Perfil de Usuario en Django

## ¿Qué vamos a construir?

Un sistema donde cada usuario tiene un **perfil extendido** con campos adicionales (foto, biografía, fecha de nacimiento) que se crea automáticamente al registrarse.

| Concepto | Detalle |
|----------|---------|
| `OneToOneField` | Relación 1:1 entre `User` y `Profile` |
| `signals` (`post_save`) | Crear perfil automáticamente al crear usuario |
| `ImageField` | Subir foto de perfil |
| `ModelForm` | Formulario para editar el perfil |

## Flujo de la aplicación

```
Usuario se registra
       │
       ▼ (signal post_save)
┌──────────────────┐
│ Se crea Profile   │  ← automáticamente
│ vacío asociado    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Usuario edita     │  ← formulario con foto,
│ su perfil         │     bio, fecha de nacimiento
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Perfil visible    │  ← página pública o privada
│ actualizado       │
└──────────────────┘
```

---

## Paso 1: Configurar media files

Para manejar archivos subidos por el usuario (fotos), necesitamos configurar `MEDIA_ROOT` y `MEDIA_URL`.

### `settings.py`

```python
import os

# Al final del archivo
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### `urls.py` (proyecto principal)

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... tus urls ...
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> **¿Por qué solo en DEBUG?** En producción, los archivos estáticos y media los sirve el servidor web (Nginx, Apache), no Django.

---

## Paso 2: Crear el modelo Profile

### `accounts/models.py`

```python
from django.db import models
from django.conf import settings


def user_profile_path(instance, filename):
    """Guarda la foto en media/profile_pics/user_<id>/<filename>"""
    return f'profile_pics/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to=user_profile_path,
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biografía'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de nacimiento'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'
```

### Instalar Pillow (requerido para ImageField)

```bash
pip install Pillow
```

### Crear y aplicar migraciones

```bash
python3 manage.py makemigrations accounts
python3 manage.py migrate
```

### ¿Por qué `settings.AUTH_USER_MODEL`?

| Forma | Cuándo usar |
|-------|-------------|
| `from django.contrib.auth.models import User` | Solo si **nunca** vas a cambiar el modelo de usuario |
| `settings.AUTH_USER_MODEL` | **Siempre recomendado** — funciona con modelos de usuario personalizados |

---

## Paso 3: Crear la señal para auto-crear el perfil

### `accounts/signals.py`

```python
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un Profile automáticamente cuando se crea un User."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el Profile cuando se guarda el User."""
    instance.profile.save()
```

### `accounts/apps.py`

```python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # noqa: F401
```

> **¿Qué es `ready()`?** Django llama a este método cuando la aplicación está completamente cargada. Es el lugar correcto para conectar señales.

### ¿Cómo funciona la señal?

```
User.objects.create_user(...)
        │
        ▼ Django emite post_save con created=True
        │
        ▼
create_user_profile()
        │
        ▼
Profile.objects.create(user=instance)  ← perfil creado automáticamente
```

---

## Paso 4: Crear los formularios

### `accounts/forms.py`

```python
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """Formulario para editar campos del modelo User."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para editar campos del modelo Profile."""

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'bio': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Cuéntanos sobre ti...'}
            ),
        }
```

> **¿Por qué dos formularios?** Porque los datos están en dos modelos distintos (`User` y `Profile`). Ambos se muestran en una sola página y se procesan juntos en la vista.

---

## Paso 5: Crear la vista

### `accounts/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm


@login_required
def profile_view(request):
    """Muestra el perfil del usuario."""
    return render(request, 'accounts/profile.html')


@login_required
def profile_edit_view(request):
    """Permite editar el perfil del usuario."""
    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,  # Necesario para ImageField
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
```

### Puntos clave de la vista

| Detalle | Explicación |
|---------|-------------|
| `@login_required` | Solo usuarios autenticados pueden ver/editar su perfil |
| `request.FILES` | **Obligatorio** cuando el formulario tiene archivos (fotos) |
| `instance=request.user` | Pre-llena el formulario con los datos actuales |
| `instance=request.user.profile` | Accede al perfil vía la relación `OneToOneField` |

---

## Paso 6: Configurar las URLs

### `accounts/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]
```

### `urls.py` (proyecto principal)

```python
urlpatterns = [
    # ... otras urls ...
    path('', include('accounts.urls')),
]
```

---

## Paso 7: Crear los templates

### 7.1 Ver perfil — `accounts/profile.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Perfil</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .profile-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 30px;
        }
        .avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #ddd;
        }
        .avatar-placeholder {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background-color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            color: #999;
        }
        .info { margin-top: 20px; }
        .info p { margin: 8px 0; }
        .label { font-weight: bold; color: #555; }
        .actions { margin-top: 20px; }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .btn:hover { background-color: #45a049; }
        .messages { margin-bottom: 20px; }
        .message-success {
            background-color: #e8f5e9;
            border: 1px solid #4CAF50;
            padding: 10px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    {% if messages %}
        <div class="messages">
            {% for message in messages %}
                <div class="message-{{ message.tags }}">{{ message }}</div>
            {% endfor %}
        </div>
    {% endif %}

    <div class="profile-card">
        <h2>Mi Perfil</h2>

        {% if user.profile.avatar %}
            <img src="{{ user.profile.avatar.url }}" alt="Avatar" class="avatar">
        {% else %}
            <div class="avatar-placeholder">{{ user.username|first|upper }}</div>
        {% endif %}

        <div class="info">
            <p><span class="label">Usuario:</span> {{ user.username }}</p>
            <p><span class="label">Nombre:</span> {{ user.get_full_name|default:"No especificado" }}</p>
            <p><span class="label">Email:</span> {{ user.email|default:"No especificado" }}</p>
            <p><span class="label">Biografía:</span> {{ user.profile.bio|default:"Sin biografía" }}</p>
            <p><span class="label">Fecha de nacimiento:</span>
                {% if user.profile.birth_date %}
                    {{ user.profile.birth_date }}
                {% else %}
                    No especificada
                {% endif %}
            </p>
            <p><span class="label">Miembro desde:</span> {{ user.date_joined|date:"d M Y" }}</p>
        </div>

        <div class="actions">
            <a href="{% url 'profile_edit' %}" class="btn">Editar perfil</a>
        </div>
    </div>
</body>
</html>
```

### 7.2 Editar perfil — `accounts/profile_edit.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Perfil</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"],
        input[type="email"],
        input[type="date"],
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .current-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 10px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background-color: #45a049; }
        .btn-cancel {
            display: inline-block;
            padding: 12px 24px;
            color: #555;
            text-decoration: none;
            margin-left: 10px;
        }
        .error { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <h2>Editar Perfil</h2>

    <!-- enctype="multipart/form-data" es OBLIGATORIO para subir archivos -->
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}

        <h3>Datos de usuario</h3>

        {% for field in user_form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}:</label>
                {{ field }}
                {% if field.errors %}
                    <div class="error">{{ field.errors }}</div>
                {% endif %}
            </div>
        {% endfor %}

        <h3>Datos de perfil</h3>

        {% if user.profile.avatar %}
            <p>Foto actual:</p>
            <img src="{{ user.profile.avatar.url }}" alt="Avatar actual" class="current-avatar">
        {% endif %}

        {% for field in profile_form %}
            <div class="form-group">
                <label for="{{ field.id_for_label }}">{{ field.label }}:</label>
                {{ field }}
                {% if field.help_text %}
                    <small>{{ field.help_text }}</small>
                {% endif %}
                {% if field.errors %}
                    <div class="error">{{ field.errors }}</div>
                {% endif %}
            </div>
        {% endfor %}

        <button type="submit">Guardar cambios</button>
        <a href="{% url 'profile' %}" class="btn-cancel">Cancelar</a>
    </form>
</body>
</html>
```

> **Punto clave:** `enctype="multipart/form-data"` es **obligatorio** en el `<form>` cuando se suben archivos. Sin esto, `request.FILES` estará vacío y la foto no se guardará.

---

## Paso 8: Registrar en el Admin

### `accounts/admin.py`

```python
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']
    search_fields = ['user__username', 'user__email']
```

---

## Paso 9: Probar

### 1. Crear un superusuario (si no tienes uno)

```bash
python3 manage.py createsuperuser
```

### 2. Ejecutar el servidor

```bash
python3 manage.py runserver
```

### 3. Verificar creación automática

Registra un nuevo usuario y confirma que en el admin (`/admin/`) aparece su perfil creado automáticamente.

### 4. Editar perfil

Visita `/profile/edit/`, sube una foto, escribe una biografía y guarda.

### 5. Verificar la foto

La foto debería guardarse en `media/profile_pics/user_<id>/` y mostrarse en `/profile/`.

---

## Crear perfiles para usuarios existentes

Si ya tienes usuarios sin perfil, crea un comando de gestión:

### `accounts/management/commands/create_profiles.py`

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile


class Command(BaseCommand):
    help = 'Crea perfiles para usuarios que no tienen uno'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(profile__isnull=True)
        count = 0
        for user in users_without_profile:
            Profile.objects.create(user=user)
            count += 1
        self.stdout.write(
            self.style.SUCCESS(f'Se crearon {count} perfiles.')
        )
```

```bash
python3 manage.py create_profiles
```

---

## Estructura final de archivos

```
accounts/
├── management/
│   └── commands/
│       └── create_profiles.py   ← comando para usuarios existentes
├── migrations/
├── templates/
│   └── accounts/
│       ├── profile.html         ← ver perfil
│       └── profile_edit.html    ← editar perfil
├── __init__.py
├── admin.py                     ← registro en admin
├── apps.py                      ← importa signals en ready()
├── forms.py                     ← UserUpdateForm + ProfileUpdateForm
├── models.py                    ← modelo Profile
├── signals.py                   ← auto-crear perfil
├── urls.py                      ← rutas profile/ y profile/edit/
└── views.py                     ← vistas de perfil
media/
└── profile_pics/                ← fotos subidas (gitignore esto)
```

---

## Resumen

| Concepto | Detalle |
|----------|---------|
| Modelo | `Profile` con `OneToOneField` a `User` |
| Señal | `post_save` crea el perfil automáticamente |
| Formularios | `UserUpdateForm` + `ProfileUpdateForm` juntos |
| Archivos | `ImageField` + `enctype="multipart/form-data"` + `request.FILES` |
| Seguridad | `@login_required` en todas las vistas |
| Upload path | `media/profile_pics/user_<id>/` |
| Comando | `create_profiles` para usuarios existentes sin perfil |
