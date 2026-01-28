# Manual Práctico: Gestión de Proyectos Python con `uv`

Esta guía cubre desde la instalación básica hasta el manejo avanzado de dependencias y entornos, optimizado para el desarrollo moderno.

---

## 1. Instalación y Configuración Inicial
`uv` es un reemplazo extremadamente rápido para `pip`, `pip-tools` y `virtualenv`.

* **Instalación (Linux/Ubuntu):**
    ```bash
    curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
    ```
* **Inicializar un proyecto:**
    ```bash
    uv init mi-proyecto
    cd mi-proyecto
    ```

## 2. Gestión de Versiones de Python
`uv` puede gestionar instalaciones de Python de forma aislada sin depender del gestor de paquetes del sistema.

* **Instalar una versión:** `uv python install 3.12`
* **Fijar versión del proyecto:** `uv python pin 3.12` (crea el archivo `.python-version`)
* **Ver versiones instaladas:** `uv python list`

## 3. Entornos Virtuales Avanzados
A diferencia de otros gestores, `uv` utiliza "reflinks" para que la creación de entornos no ocupe espacio extra innecesario.

* **Crear entorno:** `uv venv`
* **Activar (Linux):** `source .venv/bin/activate`
* **Especificar versión al crear:** `uv venv --python 3.11`

## 4. Administración de Dependencias (Workflow con Lockfile)
`uv` introduce el archivo `uv.lock`, que garantiza que todos los desarrolladores tengan exactamente las mismas versiones.

* **Añadir paquetes:** `uv add django graphene-django`
* **Dependencias de desarrollo:** `uv add --dev pytest ruff`
* **Eliminar paquetes:** `uv remove django`
* **Sincronizar el entorno:** `uv sync` (instala lo que falta y borra lo que sobra según el lockfile)

## 5. Ejecución de Scripts y Aplicaciones
Puedes ejecutar comandos sin necesidad de activar manualmente el entorno virtual.

* **Ejecutar script:** `uv run python manage.py runserver`
* **Ejecutar con dependencias temporales:**
    ```bash
    uv run --with requests script.py
    ```

## 6. Uso de Herramientas Globales con `uvx`
`uvx` (equivalente a `npx` de Node.js) permite ejecutar herramientas en entornos efímeros.

* **Ejemplo con Ruff:** `uvx ruff check .`
* **Ejemplo con HTTPie:** `uvx httpie google.com`

## 7. Gestión de Scripts en un solo archivo
`uv` permite definir dependencias dentro de un solo archivo `.py` usando metadatos inline (PEP 723).

* **Ejemplo de cabecera en un script:**
    ```python
    # /// script
    # dependencies = ["requests"]
    # ///
    import requests
    print(requests.get("[https://google.com](https://google.com)").status_code)
    ```
* **Ejecución:** `uv run script.py` (uv instalará `requests` automáticamente en un entorno temporal).

---

### Resumen de comandos esenciales
| Comando | Propósito |
| :--- | :--- |
| `uv init` | Inicia un nuevo proyecto |
| `uv add` | Añade y sincroniza una librería |
| `uv sync` | Fuerza al entorno a coincidir con el lockfile |
| `uv run` | Ejecuta comandos en el contexto del proyecto |
| `uv lock` | Solo actualiza el archivo de bloqueo |
| `uv tree` | Visualiza el árbol de dependencias |
