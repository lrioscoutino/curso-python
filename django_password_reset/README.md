# Tutorial: Recuperación de Contraseña en Django

## ¿Qué es el sistema de Password Reset de Django?

Django incluye **4 vistas built-in** en `django.contrib.auth.views` que manejan todo el flujo de recuperación de contraseña:

| Vista | Función |
|-------|---------|
| `PasswordResetView` | Formulario donde el usuario ingresa su email |
| `PasswordResetDoneView` | Página de confirmación: "Te enviamos un email" |
| `PasswordResetConfirmView` | Formulario para ingresar la nueva contraseña |
| `PasswordResetCompleteView` | Página final: "Tu contraseña fue cambiada" |

Estas vistas manejan internamente: generación de tokens seguros, envío de emails, validación del enlace y cambio de contraseña con hash.

## Flujo completo

```
Usuario olvida contraseña
        │
        ▼
┌─────────────────────┐
│ password_reset       │  ← Ingresa su email
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ password_reset_done  │  ← "Revisa tu correo"
└─────────┬───────────┘
          │
          ▼  (usuario abre el enlace del email)
┌─────────────────────┐
│ password_reset_      │  ← Ingresa nueva contraseña
│ confirm              │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ password_reset_      │  ← "¡Contraseña cambiada!"
│ complete             │
└─────────────────────┘
```

---

## Paso 1: Configurar el backend de email

Para desarrollo usaremos el **backend de consola**, que imprime los emails en la terminal en lugar de enviarlos realmente.

### `settings.py`

```python
# Backend de email para desarrollo (imprime en consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Opcional: configurar idioma español
LANGUAGE_CODE = 'es'
```

> **¿Qué hace `console.EmailBackend`?**
> En lugar de conectarse a un servidor SMTP, imprime el contenido del email directamente en la terminal donde ejecutas `runserver`. Perfecto para desarrollo y pruebas.

### Para producción (ejemplo con Gmail)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicacion'
DEFAULT_FROM_EMAIL = 'tu_email@gmail.com'
```

> **Nota de seguridad:** Nunca escribas contraseñas directamente en `settings.py`. Usa variables de entorno o un archivo `.env`.

---

## Paso 2: Configurar las URLs

### `urls.py` (proyecto principal)

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... tus otras urls ...

    # Paso 1: Formulario para ingresar email
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html'
        ),
        name='password_reset'
    ),

    # Paso 2: Confirmación de que el email fue enviado
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Paso 3: Formulario para nueva contraseña (enlace del email)
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Paso 4: Confirmación final
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
```

> **Importante:** El nombre de cada URL (`name=`) debe ser exactamente el mostrado arriba. Django los usa internamente para generar los enlaces del email y las redirecciones entre vistas.

### Anatomía de la URL de confirmación

```
password-reset-confirm/<uidb64>/<token>/
                        │        │
                        │        └─ Token único de un solo uso
                        └─ ID del usuario codificado en Base64
```

Django genera automáticamente estos valores y los incluye en el email.

---

## Paso 3: Crear los templates

Necesitamos **4 templates HTML** y **2 templates para el email**.

### 3.1 Formulario de solicitud — `registration/password_reset.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperar Contraseña</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="email"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
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
        .error { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <h2>Recuperar Contraseña</h2>
    <p>Ingresa tu dirección de correo electrónico y te enviaremos un enlace para restablecer tu contraseña.</p>

    <form method="post">
        {% csrf_token %}

        {% if form.errors %}
            <div class="error">
                <p>Por favor corrige los errores a continuación.</p>
            </div>
        {% endif %}

        <div class="form-group">
            <label for="{{ form.email.id_for_label }}">Correo electrónico:</label>
            {{ form.email }}
        </div>

        <button type="submit">Enviar enlace de recuperación</button>
    </form>

    <p><a href="{% url 'login' %}">Volver al inicio de sesión</a></p>
</body>
</html>
```

### 3.2 Email enviado — `registration/password_reset_done.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Enviado</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        .info-box {
            background-color: #e8f5e9;
            border: 1px solid #4CAF50;
            border-radius: 4px;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h2>Revisa tu correo</h2>

    <div class="info-box">
        <p>Te hemos enviado instrucciones para restablecer tu contraseña al correo electrónico proporcionado.</p>
        <p>Si no recibes el correo en unos minutos, verifica que ingresaste la dirección correcta y revisa tu carpeta de spam.</p>
    </div>

    <p><a href="{% url 'login' %}">Volver al inicio de sesión</a></p>
</body>
</html>
```

> **Nota de seguridad:** Esta página se muestra siempre, sin importar si el email existe o no en el sistema. Esto evita que un atacante pueda descubrir qué emails están registrados.

### 3.3 Nueva contraseña — `registration/password_reset_confirm.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nueva Contraseña</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
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
        .error { color: red; font-size: 14px; }
        .help-text { color: #666; font-size: 13px; margin-top: 5px; }
        .invalid-link {
            background-color: #ffebee;
            border: 1px solid #f44336;
            border-radius: 4px;
            padding: 20px;
        }
    </style>
</head>
<body>
    {% if validlink %}
        <h2>Establece tu nueva contraseña</h2>

        <form method="post">
            {% csrf_token %}

            {% if form.errors %}
                <div class="error">
                    <p>Por favor corrige los errores a continuación.</p>
                    {{ form.errors }}
                </div>
            {% endif %}

            <div class="form-group">
                <label for="{{ form.new_password1.id_for_label }}">Nueva contraseña:</label>
                {{ form.new_password1 }}
                <div class="help-text">{{ form.new_password1.help_text }}</div>
            </div>

            <div class="form-group">
                <label for="{{ form.new_password2.id_for_label }}">Confirmar contraseña:</label>
                {{ form.new_password2 }}
            </div>

            <button type="submit">Cambiar contraseña</button>
        </form>
    {% else %}
        <div class="invalid-link">
            <h2>Enlace inválido</h2>
            <p>Este enlace de recuperación ya fue usado o ha expirado.</p>
            <p><a href="{% url 'password_reset' %}">Solicitar un nuevo enlace</a></p>
        </div>
    {% endif %}
</body>
</html>
```

> **¿Qué es `validlink`?**
> Django pasa esta variable al template. Es `True` si la combinación de `uidb64` y `token` es válida y no ha sido usada. Si el enlace ya expiró o fue usado, es `False`.

### 3.4 Contraseña cambiada — `registration/password_reset_complete.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contraseña Cambiada</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
        }
        .success-box {
            background-color: #e8f5e9;
            border: 1px solid #4CAF50;
            border-radius: 4px;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="success-box">
        <h2>Contraseña restablecida</h2>
        <p>Tu contraseña ha sido cambiada exitosamente. Ya puedes iniciar sesión con tu nueva contraseña.</p>
    </div>

    <p><a href="{% url 'login' %}">Iniciar sesión</a></p>
</body>
</html>
```

---

## Paso 4: Templates del email

### 4.1 Asunto del email — `registration/password_reset_subject.txt`

```
Recuperación de contraseña - {{ site_name }}
```

> **Importante:** Este archivo debe tener una sola línea, sin saltos de línea al final.

### 4.2 Cuerpo del email — `registration/password_reset_email.html`

```
Hola,

Recibimos una solicitud para restablecer la contraseña de tu cuenta asociada al correo {{ email }}.

Para restablecer tu contraseña, haz clic en el siguiente enlace:

{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}

Si no solicitaste este cambio, puedes ignorar este mensaje. Tu contraseña no será modificada.

Saludos,
{{ site_name }}
```

### Variables disponibles en el template del email

| Variable | Descripción |
|----------|-------------|
| `{{ email }}` | Correo electrónico del usuario |
| `{{ domain }}` | Dominio del sitio (ej: `localhost:8000`) |
| `{{ site_name }}` | Nombre del sitio |
| `{{ protocol }}` | `http` o `https` |
| `{{ uid }}` | ID del usuario codificado en Base64 |
| `{{ token }}` | Token de un solo uso |

---

## Paso 5: Agregar enlace en el template de login

En tu template de login existente, agrega un enlace para que el usuario pueda recuperar su contraseña:

```html
<!-- Dentro de tu template de login -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Iniciar sesión</button>
</form>

<p><a href="{% url 'password_reset' %}">¿Olvidaste tu contraseña?</a></p>
<p>¿No tienes cuenta? <a href="{% url 'register' %}">Regístrate aquí</a></p>
```

---

## Paso 6: Probar el flujo completo

### 1. Ejecuta el servidor

```bash
python3 manage.py runserver
```

### 2. Visita la página de recuperación

Abre tu navegador en: `http://127.0.0.1:8000/password-reset/`

### 3. Ingresa un email registrado

Escribe el email de un usuario existente y haz clic en "Enviar enlace de recuperación".

### 4. Revisa la terminal

Como usamos `console.EmailBackend`, verás algo así en la terminal:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: =?utf-8?q?Recuperaci=C3=B3n_de_contrase=C3=B1a_-_localhost?=
From: webmaster@localhost
To: usuario@ejemplo.com
Date: Mon, 09 Mar 2026 12:00:00 -0000

Hola,

Recibimos una solicitud para restablecer la contraseña...

http://127.0.0.1:8000/password-reset-confirm/MQ/abc123-token/
```

### 5. Copia el enlace y ábrelo en el navegador

El enlace te llevará al formulario para establecer la nueva contraseña.

### 6. Verifica que funcione

- Intenta con contraseñas que no coinciden → debe mostrar error
- Intenta con una contraseña débil (ej: `123`) → debe mostrar error de validación
- Ingresa una contraseña válida → debe redirigir a la página de éxito

---

## Extras opcionales

### Personalizar la duración del token

Por defecto, el enlace de recuperación expira en **3 días** (259200 segundos). Puedes cambiarlo en `settings.py`:

```python
# El token expira en 1 hora (3600 segundos)
PASSWORD_RESET_TIMEOUT = 3600
```

### Renderizar campos individualmente con CSS personalizado

```html
<div class="form-group">
    <label for="{{ form.email.id_for_label }}">Correo electrónico:</label>
    <input
        type="email"
        name="{{ form.email.html_name }}"
        id="{{ form.email.id_for_label }}"
        class="form-control"
        placeholder="tu@email.com"
        required
    >
    {% if form.email.errors %}
        <div class="error">{{ form.email.errors }}</div>
    {% endif %}
</div>
```

### Login automático después de cambiar contraseña

```python
# En urls.py
path(
    'password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        post_reset_login=True,  # Login automático al cambiar contraseña
    ),
    name='password_reset_confirm'
),
```

---

## Estructura final de archivos

```
tu_proyecto/
├── templates/
│   └── registration/
│       ├── password_reset.html           ← Formulario: ingresar email
│       ├── password_reset_done.html      ← Mensaje: "revisa tu correo"
│       ├── password_reset_confirm.html   ← Formulario: nueva contraseña
│       ├── password_reset_complete.html  ← Mensaje: "contraseña cambiada"
│       ├── password_reset_email.html     ← Cuerpo del email enviado
│       └── password_reset_subject.txt    ← Asunto del email
├── settings.py                           ← EMAIL_BACKEND configurado
└── urls.py                               ← 4 rutas de password reset
```

---

## Resumen

| Concepto | Detalle |
|----------|---------|
| Vistas usadas | `PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, `PasswordResetCompleteView` |
| Templates necesarios | 4 HTML + 1 email body + 1 email subject |
| Backend de email (dev) | `django.core.mail.backends.console.EmailBackend` |
| Seguridad del token | Un solo uso, expira en 3 días (configurable) |
| Seguridad del flujo | No revela si un email existe en el sistema |
| Configuración | `PASSWORD_RESET_TIMEOUT` para duración del token |
