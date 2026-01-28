# Guia Practica: UV con Django

Manual practico para usar **uv** como gestor de proyectos Python con Django.

---

## 1. Instalacion de UV

### Linux / macOS

```bash
# Usando curl (recomendado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Usando wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Alternativas

```bash
# macOS con Homebrew
brew install uv

# Windows con WinGet
winget install --id=astral-sh.uv -e

# Con pipx
pipx install uv
```

### Verificar instalacion

```bash
uv --version
```

---

## 2. Gestion de Versiones de Python

### Instalar versiones de Python

```bash
# Instalar una version especifica
uv python install 3.12

# Instalar version con patch exacto
uv python install 3.12.3

# Instalar segun restricciones
uv python install '>=3.10,<3.13'
```

### Listar versiones disponibles

```bash
# Ver versiones instaladas y disponibles
uv python list

# Filtrar por version
uv python list 3.12

# Ver todas las versiones disponibles
uv python list --all-versions
```

### Encontrar ejecutable de Python

```bash
uv python find '>=3.11'
```

---

## 3. Crear un Proyecto Django

### Inicializar proyecto con uv

```bash
# Crear directorio del proyecto
uv init mi-proyecto-django
cd mi-proyecto-django

# O inicializar en directorio existente
mkdir mi-proyecto-django
cd mi-proyecto-django
uv init
```

### Estructura generada por uv

```
mi-proyecto-django/
├── .gitignore
├── .python-version      # Version de Python del proyecto
├── main.py              # Archivo principal (lo eliminaremos)
├── pyproject.toml       # Configuracion del proyecto
└── README.md
```

### Agregar Django como dependencia

```bash
# Agregar Django
uv add django

# Agregar version especifica
uv add 'django>=5.0,<6.0'

# Agregar Django con extras comunes
uv add django djangorestframework django-cors-headers
```

### Archivos creados automaticamente

Despues de agregar dependencias, uv crea:

- **`.venv/`**: Entorno virtual aislado
- **`uv.lock`**: Lockfile con versiones exactas (incluir en git)

---

## 4. Configurar Proyecto Django

### Crear proyecto Django

```bash
# Eliminar main.py generado por uv
rm main.py

# Crear proyecto Django (el punto al final es importante)
uv run django-admin startproject config .
```

### Estructura resultante

```
mi-proyecto-django/
├── .gitignore
├── .python-version
├── .venv/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
```

### Crear una aplicacion Django

```bash
uv run python manage.py startapp mi_app
```

---

## 5. Ejecutar Comandos Django

### Usando `uv run`

```bash
# Ejecutar servidor de desarrollo
uv run python manage.py runserver

# Ejecutar en puerto especifico
uv run python manage.py runserver 0.0.0.0:8000

# Crear migraciones
uv run python manage.py makemigrations

# Aplicar migraciones
uv run python manage.py migrate

# Crear superusuario
uv run python manage.py createsuperuser

# Abrir shell de Django
uv run python manage.py shell

# Recolectar archivos estaticos
uv run python manage.py collectstatic
```

### Alternativa: Activar entorno virtual

```bash
# Sincronizar dependencias
uv sync

# Activar entorno (Linux/macOS)
source .venv/bin/activate

# Activar entorno (Windows)
.venv\Scripts\activate

# Ahora puedes usar comandos directamente
python manage.py runserver
```

---

## 6. Gestion de Dependencias

### Agregar dependencias

```bash
# Dependencia de produccion
uv add psycopg2-binary
uv add gunicorn
uv add python-decouple

# Dependencia de desarrollo
uv add --dev pytest pytest-django
uv add --dev black isort flake8
uv add --dev django-debug-toolbar

# Desde requirements.txt existente
uv add -r requirements.txt
```

### Eliminar dependencias

```bash
uv remove django-debug-toolbar

# Eliminar dependencia de desarrollo
uv remove --dev pytest
```

### Actualizar dependencias

```bash
# Actualizar paquete especifico
uv lock --upgrade-package django

# Actualizar todas las dependencias
uv lock --upgrade
```

### Sincronizar entorno

```bash
# Instalar/actualizar segun lockfile
uv sync

# Sincronizar incluyendo dependencias de desarrollo
uv sync --dev
```

---

## 7. Grupos de Dependencias

### Crear grupos personalizados

```bash
# Grupo para testing
uv add --group test pytest pytest-django pytest-cov

# Grupo para linting
uv add --group lint ruff mypy

# Grupo para documentacion
uv add --group docs sphinx sphinx-rtd-theme
```

### Ejemplo de pyproject.toml

```toml
[project]
name = "mi-proyecto-django"
version = "0.1.0"
description = "Proyecto Django con uv"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "django>=5.0",
    "djangorestframework>=3.14",
    "python-decouple>=3.8",
    "psycopg2-binary>=2.9",
]

[dependency-groups]
dev = [
    "django-debug-toolbar>=4.2",
    "ipython>=8.0",
]
test = [
    "pytest>=8.0",
    "pytest-django>=4.8",
    "pytest-cov>=4.1",
]
lint = [
    "ruff>=0.1",
    "mypy>=1.8",
]
```

---

## 8. Scripts en pyproject.toml

### Definir scripts personalizados

Agrega scripts al `pyproject.toml`:

```toml
[project.scripts]
dev = "manage:main"

[tool.uv.scripts]
serve = "python manage.py runserver"
migrate = "python manage.py migrate"
makemigrations = "python manage.py makemigrations"
shell = "python manage.py shell"
test = "pytest"
lint = "ruff check ."
format = "ruff format ."
```

---

## 9. Configuracion Avanzada

### Archivo .python-version

```
3.12
```

### Variables de entorno con .env

Crea archivo `.env`:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

Usa `python-decouple` en settings.py:

```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

### Configurar indice de paquetes alternativo

En `pyproject.toml`:

```toml
[tool.uv]
index-url = "https://pypi.org/simple"
extra-index-url = ["https://download.pytorch.org/whl/cpu"]
```

---

## 10. Flujo de Trabajo Recomendado

### Nuevo proyecto desde cero

```bash
# 1. Crear e inicializar proyecto
uv init mi-proyecto
cd mi-proyecto

# 2. Especificar version de Python
uv python pin 3.12

# 3. Agregar Django y dependencias
uv add django djangorestframework python-decouple

# 4. Agregar dependencias de desarrollo
uv add --dev pytest-django django-debug-toolbar

# 5. Crear proyecto Django
rm main.py
uv run django-admin startproject config .

# 6. Verificar que funciona
uv run python manage.py runserver
```

### Clonar proyecto existente

```bash
# 1. Clonar repositorio
git clone https://github.com/usuario/proyecto.git
cd proyecto

# 2. Sincronizar dependencias
uv sync

# 3. Aplicar migraciones
uv run python manage.py migrate

# 4. Ejecutar servidor
uv run python manage.py runserver
```

---

## 11. Comandos UV mas Usados

| Comando | Descripcion |
|---------|-------------|
| `uv init` | Inicializar nuevo proyecto |
| `uv add <paquete>` | Agregar dependencia |
| `uv add --dev <paquete>` | Agregar dependencia de desarrollo |
| `uv remove <paquete>` | Eliminar dependencia |
| `uv sync` | Sincronizar entorno con lockfile |
| `uv lock` | Actualizar lockfile |
| `uv lock --upgrade` | Actualizar todas las dependencias |
| `uv run <comando>` | Ejecutar comando en entorno |
| `uv python install` | Instalar version de Python |
| `uv python list` | Listar versiones de Python |
| `uv build` | Construir paquete distribuible |
| `uv --version` | Ver version de uv |

---

## 12. Estructura Final del Proyecto

```
mi-proyecto-django/
├── .gitignore
├── .python-version
├── .venv/                    # Entorno virtual (no incluir en git)
├── .env                      # Variables de entorno (no incluir en git)
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── mi_app/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── static/
├── templates/
├── manage.py
├── pyproject.toml            # Configuracion del proyecto
├── uv.lock                   # Lockfile (incluir en git)
└── README.md
```

---

## 13. Tips y Buenas Practicas

1. **Siempre incluir `uv.lock` en git**: Garantiza reproducibilidad entre entornos

2. **No incluir `.venv/` en git**: Cada desarrollador debe sincronizar su propio entorno

3. **Usar `uv run` en lugar de activar entorno**: Es mas explicito y evita errores

4. **Separar dependencias por grupos**: Facilita instalaciones en diferentes entornos

5. **Especificar version de Python**: Usa `.python-version` para consistencia

6. **Actualizar regularmente**: Ejecuta `uv lock --upgrade` periodicamente

7. **Revisar lockfile antes de commit**: Verifica que no haya cambios inesperados

---

## Referencias

- [Documentacion oficial de UV](https://docs.astral.sh/uv/)
- [Guia de proyectos UV](https://docs.astral.sh/uv/guides/projects/)
- [Gestion de dependencias](https://docs.astral.sh/uv/concepts/projects/dependencies/)
- [Documentacion de Django](https://docs.djangoproject.com/)
