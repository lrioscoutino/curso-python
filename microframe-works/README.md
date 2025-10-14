
# Práctica: Creando una Aplicación Simple con Flask y FastAPI

Este documento sirve como una guía práctica y teórica para construir una pequeña aplicación de prueba utilizando dos de los frameworks web más populares de Python: Flask y FastAPI.

## Introducción

Tanto Flask como FastAPI son excelentes opciones para desarrollar APIs y servicios web en Python. Sin embargo, operan bajo principios diferentes y son adecuados para distintos tipos de tareas.

- **Flask**: Es un microframework WSGI (Web Server Gateway Interface). Es conocido por su simplicidad, flexibilidad y un núcleo minimalista que es fácil de extender. Es una opción sólida para una amplia variedad de aplicaciones web, desde sitios pequeños hasta APIs complejas.
- **FastAPI**: Es un framework web moderno y de alto rendimiento basado en ASGI (Asynchronous Server Gateway Interface). Utiliza anotaciones de tipo de Python (type hints) para validar, serializar y deserializar datos, además de generar automáticamente documentación interactiva para tu API.

A continuación, crearemos la misma aplicación "Hola Mundo" en ambos frameworks para comparar sus enfoacciones.

---

## Parte 1: Construyendo con Flask

### 1.1. Fundamentos Teóricos de Flask

Flask se basa en el estándar WSGI, que es una interfaz síncrona entre los servidores web y las aplicaciones de Python. Esto significa que, por defecto, maneja las peticiones de manera secuencial. Aunque se pueden integrar soluciones para asincronía, no es su característica principal. Su filosofía es mantener un núcleo simple y dejar que el desarrollador elija las herramientas y extensiones que necesita.

### 1.2. Pasos Técnicos

#### a. Configurar el Entorno

Primero, crea un entorno virtual para aislar las dependencias de nuestro proyecto.

```bash
# Crea un directorio para el proyecto
mkdir practica_flask
cd practica_flask

# Crea y activa un entorno virtual
python3 -m venv venv
source venv/bin/activate
```

#### b. Instalar Flask

Instala Flask utilizando `pip`.

```bash
pip install Flask
```

#### c. Crear la Aplicación

Crea un archivo llamado `app.py` y agrega el siguiente código:

```python
from flask import Flask, jsonify

# Inicializa la aplicación de Flask
app = Flask(__name__)

# Define una ruta en la URL raíz ("/")
@app.route('/')
def hola_mundo():
    """
    Esta función se ejecuta cuando alguien accede a la URL raíz.
    """
    return jsonify(mensaje="Hola Mundo desde Flask!")

# Permite ejecutar la aplicación directamente con 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)
```

#### d. Ejecutar la Aplicación

Inicia el servidor de desarrollo de Flask.

```bash
flask run
```

O, si incluiste el bloque `if __name__ == '__main__':`:

```bash
python app.py
```

Ahora puedes visitar `http://127.0.0.1:5000` en tu navegador o con una herramienta como `curl` y verás la respuesta en formato JSON.

---

## Parte 2: Construyendo con FastAPI

### 2.1. Fundamentos Teóricos de FastAPI

FastAPI está construido sobre Starlette (para el núcleo web) and Pydantic (para la validación de datos). Se basa en el estándar ASGI, lo que le permite manejar operaciones de manera asíncrona de forma nativa. Esto lo hace ideal para aplicaciones que requieren alta concurrencia y operaciones de I/O intensivas, como interactuar con bases de datos o APIs externas.

Una de sus características más destacadas es la **generación automática de documentación**. Al usar type hints, FastAPI crea una interfaz de usuario con Swagger UI y ReDoc para que puedas probar tu API directamente desde el navegador.

### 2.2. Pasos Técnicos

#### a. Configurar el Entorno

Si sigues desde la práctica de Flask, puedes usar el mismo entorno o crear uno nuevo.

```bash
# (Si es necesario) Crea un directorio y un entorno virtual
mkdir practica_fastapi
cd practica_fastapi
python3 -m venv venv
source venv/bin/activate
```

#### b. Instalar FastAPI y Uvicorn

FastAPI requiere un servidor ASGI como `uvicorn` para ejecutarse.

```bash
pip install fastapi "uvicorn[standard]"
```

#### c. Crear la Aplicación

Crea un archivo llamado `main.py` con el siguiente código:

```python
from fastapi import FastAPI

# Inicializa la aplicación de FastAPI
app = FastAPI()

# Define una ruta en la URL raíz ("/")
@app.get('/')
def hola_mundo():
    """
    Esta función se ejecuta cuando alguien accede a la URL raíz con un método GET.
    """
    return {"mensaje": "Hola Mundo desde FastAPI!"}
```

#### d. Ejecutar la Aplicación

Usa `uvicorn` para iniciar el servidor.

```bash
uvicorn main:app --reload
```

- `main`: Es el nombre del archivo (`main.py`).
- `app`: Es el objeto `FastAPI` creado dentro del archivo.
- `--reload`: Hace que el servidor se reinicie automáticamente cada vez que cambies el código.

Ahora, visita `http://127.0.0.1:8000`. Además, puedes explorar la documentación interactiva en `http://127.0.0.1:8000/docs`.

---

## Comparación y Conclusión

| Característica      | Flask                                       | FastAPI                                           |
|---------------------|---------------------------------------------|---------------------------------------------------|
| **Interfaz**        | WSGI (Síncrono por defecto)                 | ASGI (Asíncrono por naturaleza)                   |
| **Rendimiento**     | Bueno para la mayoría de los casos de uso.  | Muy alto, ideal para alta concurrencia.           |
| **Validación**      | Manual o mediante extensiones (ej. Marshmallow). | Integrada y automática con Pydantic.              |
| **Documentación**   | Requiere extensiones (ej. Flasgger).        | Automática (Swagger UI y ReDoc).                  |
| **Curva de Aprendizaje** | Muy baja, ideal para principiantes.         | Baja, pero requiere entender `async/await`.       |

### ¿Cuándo elegir cuál?

- **Usa Flask si:**
  - Estás construyendo una aplicación web tradicional o un monolito.
  - Prefieres la máxima flexibilidad y un control total sobre los componentes que usas.
  - La asincronía no es una prioridad clave.

- **Usa FastAPI si:**
  - Estás construyendo una API que necesita alto rendimiento y escalabilidad.
  - Quieres validación de datos y documentación automática desde el principio.
  - Tu aplicación se beneficiará del ecosistema asíncrono de Python.

Ambos frameworks son herramientas poderosas en el arsenal de un desarrollador de Python. La elección correcta depende de los requisitos específicos de tu proyecto.
