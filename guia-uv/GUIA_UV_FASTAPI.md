# Guía Práctica: UV con FastAPI

Manual práctico para comenzar a usar **uv** como gestor de paquetes y proyectos Python con FastAPI.

## Tabla de Contenidos

1. [¿Qué es UV?](#qué-es-uv)
2. [Instalación](#instalación)
3. [Crear un Proyecto FastAPI](#crear-un-proyecto-fastapi)
4. [Gestión de Dependencias](#gestión-de-dependencias)
5. [Ejecutar la Aplicación](#ejecutar-la-aplicación)
6. [Scripts con Dependencias Inline](#scripts-con-dependencias-inline)
7. [Comandos Útiles](#comandos-útiles)
8. [Estructura del Proyecto](#estructura-del-proyecto)

---

## ¿Qué es UV?

**uv** es un gestor de paquetes y proyectos Python extremadamente rápido, desarrollado por Astral (creadores de Ruff). Reemplaza herramientas como pip, pip-tools, pipx, poetry, pyenv y virtualenv en un solo binario.

### Ventajas principales:

- **Velocidad**: 10-100x más rápido que pip
- **Todo en uno**: Gestiona Python, dependencias, entornos virtuales y proyectos
- **Compatible**: Usa `pyproject.toml` estándar (PEP 621)
- **Lockfiles**: Genera `uv.lock` para builds reproducibles

---

## Instalación

### Linux / macOS

```bash
# Instalador oficial (recomendado)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternativa con wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

### macOS con Homebrew

```bash
brew install uv
```

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Con pip/pipx (cualquier sistema)

```bash
# Con pipx (recomendado)
pipx install uv

# Con pip
pip install uv
```

### Verificar instalación

```bash
uv --version
```

---

## Crear un Proyecto FastAPI

### Paso 1: Inicializar el proyecto

```bash
# Crear nuevo proyecto
uv init mi-api-fastapi
cd mi-api-fastapi

# O inicializar en directorio existente
mkdir mi-api-fastapi && cd mi-api-fastapi
uv init
```

Esto genera la siguiente estructura:

```
mi-api-fastapi/
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

### Paso 2: Agregar FastAPI y Uvicorn

```bash
# Agregar FastAPI
uv add fastapi

# Agregar uvicorn (servidor ASGI)
uv add uvicorn[standard]

# O agregar ambos en un solo comando
uv add fastapi "uvicorn[standard]"
```

### Paso 3: Crear la aplicación

Reemplaza el contenido de `main.py`:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Mi API con UV",
    description="API creada con FastAPI y gestionada con UV",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"mensaje": "Hola desde FastAPI con UV"}


@app.get("/items/{item_id}")
def leer_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

## Gestión de Dependencias

### Agregar dependencias

```bash
# Agregar paquete
uv add requests

# Agregar con versión específica
uv add "requests==2.31.0"

# Agregar con rango de versiones
uv add "requests>=2.28,<3.0"

# Agregar dependencia de desarrollo
uv add --dev pytest pytest-asyncio httpx

# Agregar desde requirements.txt existente
uv add -r requirements.txt

# Agregar desde repositorio Git
uv add git+https://github.com/usuario/repo
```

### Eliminar dependencias

```bash
uv remove requests
```

### Actualizar dependencias

```bash
# Actualizar paquete específico
uv lock --upgrade-package fastapi

# Actualizar todas las dependencias
uv lock --upgrade
```

### Sincronizar entorno

```bash
# Instala/actualiza dependencias según uv.lock
uv sync

# Sincronizar incluyendo dependencias de desarrollo
uv sync --dev
```

---

## Ejecutar la Aplicación

### Método 1: Con `uv run` (recomendado)

```bash
# Ejecutar servidor de desarrollo
uv run uvicorn main:app --reload

# Con puerto específico
uv run uvicorn main:app --reload --port 8080

# Con host accesible externamente
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Método 2: Activando el entorno virtual

```bash
# Sincronizar dependencias
uv sync

# Activar entorno virtual
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Ejecutar
uvicorn main:app --reload

# Desactivar cuando termines
deactivate
```

### Acceder a la API

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

---

## Scripts con Dependencias Inline

UV soporta scripts independientes con dependencias declaradas (PEP 723).

### Crear script con dependencias

```bash
# Inicializar script
uv init --script servidor_rapido.py --python 3.12

# Agregar dependencias al script
uv add --script servidor_rapido.py fastapi "uvicorn[standard]"
```

### Ejemplo de script inline

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn[standard]",
# ]
# ///

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"mensaje": "Script independiente con UV"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Ejecutar script inline

```bash
# Ejecutar directamente (UV instala dependencias automáticamente)
uv run servidor_rapido.py

# O hacerlo ejecutable
chmod +x servidor_rapido.py
./servidor_rapido.py
```

---

## Comandos Útiles

### Gestión de proyecto

| Comando | Descripción |
|---------|-------------|
| `uv init` | Inicializar nuevo proyecto |
| `uv add <paquete>` | Agregar dependencia |
| `uv remove <paquete>` | Eliminar dependencia |
| `uv sync` | Sincronizar entorno con lockfile |
| `uv lock` | Actualizar lockfile |
| `uv run <comando>` | Ejecutar comando en el entorno |
| `uv build` | Construir distribuciones (wheel/sdist) |

### Gestión de Python

| Comando | Descripción |
|---------|-------------|
| `uv python list` | Listar versiones de Python disponibles |
| `uv python install 3.12` | Instalar Python 3.12 |
| `uv python pin 3.12` | Fijar versión de Python del proyecto |

### Herramientas globales

| Comando | Descripción |
|---------|-------------|
| `uv tool install ruff` | Instalar herramienta global |
| `uv tool run black .` | Ejecutar herramienta sin instalar |
| `uvx ruff check .` | Atajo para `uv tool run` |

---

## Estructura del Proyecto

### Proyecto FastAPI completo

```
mi-api-fastapi/
├── .venv/                  # Entorno virtual (auto-generado)
├── .gitignore
├── .python-version         # Versión de Python
├── pyproject.toml          # Configuración del proyecto
├── uv.lock                 # Lockfile (auto-generado)
├── README.md
├── main.py                 # Punto de entrada
├── app/
│   ├── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── items.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py
│   └── schemas/
│       ├── __init__.py
│       └── item.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

### pyproject.toml ejemplo

```toml
[project]
name = "mi-api-fastapi"
version = "0.1.0"
description = "API REST con FastAPI gestionada con UV"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
]
```

---

## Flujo de Trabajo Típico

```bash
# 1. Crear proyecto
uv init mi-api && cd mi-api

# 2. Agregar dependencias
uv add fastapi "uvicorn[standard]"
uv add --dev pytest httpx

# 3. Desarrollar (editar main.py)

# 4. Ejecutar en desarrollo
uv run uvicorn main:app --reload

# 5. Ejecutar tests
uv run pytest

# 6. Construir para producción
uv build
```

---

## Recursos Adicionales

- [Documentación oficial de UV](https://docs.astral.sh/uv/)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Repositorio de UV en GitHub](https://github.com/astral-sh/uv)

---

*Guía creada basada en la documentación oficial de UV (docs.astral.sh/uv)*
