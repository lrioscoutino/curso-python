# 🧑‍💻 Tarea Final: Proyecto Web con Django

## 🎯 Objetivo
Desarrollar una aplicación web completa utilizando el framework **Django**, aplicando el ciclo completo de desarrollo: configuración del entorno, estructura del proyecto, vistas, modelos, templates y despliegue local.

---

## 🧱 Parte 1: Preparación del entorno

### 1. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate       # En Linux o Mac
venv\Scripts\activate          # En Windows
```

### 2. Instalar Django
```bash
pip install django
```

### 3. Verificar la instalación
```bash
django-admin --version
```

---

## 🏗️ Parte 2: Crear el proyecto y la aplicación

### 1. Crear el proyecto
```bash
django-admin startproject mi_proyecto
cd mi_proyecto
```

### 2. Ejecutar el servidor por primera vez
```bash
python manage.py runserver
```

Abrir en el navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 3. Crear una aplicación
```bash
python manage.py startapp principal
```

### 4. Registrar la app en `settings.py`
```python
INSTALLED_APPS = [
    ...,
    'principal',
]
```

---

## 🧩 Parte 3: Crear una vista, URL y template

### 1. En `principal/views.py`
```python
from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html', {'titulo': 'Bienvenido a mi proyecto Django'})
```

### 2. Crear archivo `principal/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
]
```

### 3. Conectar las URLs en `mi_proyecto/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('principal.urls')),
]
```

### 4. Crear carpeta de templates
En `principal/`, crear una carpeta llamada `templates` y dentro el archivo `inicio.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{{ titulo }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css">
</head>
<body class="bg-gray-100 text-center p-8">
    <h1 class="text-3xl font-bold text-blue-600 mb-4">{{ titulo }}</h1>
    <p>Este es tu primer template en Django 🎉</p>
</body>
</html>
```

---

## 🗃️ Parte 4: Entregables

1. Repositorio en **GitHub** con:
   - Carpeta del proyecto completa.
   - Archivo `README.md` con:
     - Descripción del proyecto.
     - Pasos de instalación y ejecución.
   - Archivo `.gitignore` configurado para Django y entorno virtual.
2. Captura de pantalla del template funcionando en el navegador.
3. (Opcional) Implementar una segunda vista llamada **“Acerca de”** que muestre tu nombre y el propósito del proyecto.

---

## 🧾 Criterios de evaluación

| Criterio | Descripción | Ponderación |
|-----------|--------------|--------------|
| Configuración del entorno | Proyecto ejecuta correctamente en entorno virtual | 20% |
| Estructura y buenas prácticas | Organización del código y modularización | 20% |
| Implementación de vistas y templates | Correcta conexión entre vista, URL y template | 30% |
| Estilo y presentación | Uso básico de Tailwind o CSS propio | 10% |
| Documentación y entrega | README completo y repositorio funcional | 20% |

---

💡 **Nota:** Se valorará la claridad del código, la limpieza del repositorio y la documentación en el `README.md`.
