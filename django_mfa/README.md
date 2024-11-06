Aplicación Django simple que implemente autenticación de múltiples factores (MFA) utilizando django-otp.

```python
# requirements.txt
Django==5.0.1
django-otp==1.3.0
qrcode==7.4.2

# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'accounts',  # nuestra app
]

MIDDLEWARE = [
    # ... otros middleware
    'django_otp.middleware.OTPMiddleware',
]

# accounts/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear dispositivo TOTP para el usuario
            device = TOTPDevice.objects.create(
                user=user,
                name='default',
                confirmed=True,
                key=random_hex()
            )
            return redirect('setup_mfa', device.id)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def setup_mfa(request, device_id):
    device = TOTPDevice.objects.get(id=device_id)
    return render(request, 'accounts/setup_mfa.html', {
        'device': device,
        'qr_url': device.config_url
    })

@login_required
def verify_token(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        device = TOTPDevice.objects.get(user=request.user)
        if device.verify_token(token):
            return redirect('home')
        else:
            return render(request, 'accounts/verify_token.html', {'error': 'Token inválido'})
    return render(request, 'accounts/verify_token.html')

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('setup-mfa/<int:device_id>/', views.setup_mfa, name='setup_mfa'),
    path('verify-token/', views.verify_token, name='verify_token'),
]

# templates/accounts/register.html
{% extends "base.html" %}
{% block content %}
<div class="container mt-5">
    <h2>Registro</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Registrar</button>
    </form>
</div>
{% endblock %}

# templates/accounts/setup_mfa.html
{% extends "base.html" %}
{% block content %}
<div class="container mt-5">
    <h2>Configurar MFA</h2>
    <p>Escanea el código QR con tu aplicación de autenticación:</p>
    <img src="{{ qr_url }}" alt="QR Code">
    <p>O ingresa esta clave manualmente: {{ device.key }}</p>
    <a href="{% url 'verify_token' %}" class="btn btn-primary">Continuar</a>
</div>
{% endblock %}

# templates/accounts/verify_token.html
{% extends "base.html" %}
{% block content %}
<div class="container mt-5">
    <h2>Verificar Token</h2>
    {% if error %}
    <div class="alert alert-danger">{{ error }}</div>
    {% endif %}
    <form method="post">
        {% csrf_token %}
        <div class="form-group">
            <label for="token">Ingresa el código de verificación:</label>
            <input type="text" name="token" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Verificar</button>
    </form>
</div>
{% endblock %}

```

Esta es una aplicación Django básica que implementa MFA usando TOTP (Time-based One-Time Password). Aquí están los componentes principales:

1. **Configuración**:
   - Usamos `django-otp` para manejar la autenticación de dos factores
   - Agregamos el middleware necesario de OTP

2. **Modelo de Usuario**:
   - Extendemos el modelo de usuario predeterminado de Django

3. **Vistas principales**:
   - `register`: Para crear nuevos usuarios
   - `setup_mfa`: Para configurar el dispositivo MFA
   - `verify_token`: Para verificar el código TOTP

4. **Templates**:
   - Formularios básicos para registro y verificación
   - Página para mostrar el código QR

Para usar esta aplicación:

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Realiza las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Flujo de uso:
   - El usuario se registra
   - Se genera un dispositivo TOTP
   - El usuario escanea el código QR con una app como Google Authenticator
   - El usuario verifica el token generado
