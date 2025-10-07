# Práctica: Instalación y Creación de un Proyecto FastAPI con pyenv

Esta guía te mostrará cómo instalar FastAPI y configurar un proyecto básico desde cero utilizando `pyenv` para la gestión de entornos virtuales.

---

### **Paso 1: Preparar el Entorno del Proyecto**

Primero, necesitas crear un directorio para tu proyecto y luego configurar un entorno virtual específico para él.

1.  **Abre tu terminal.**

2.  **Crea y navega al directorio del proyecto:**
    ```bash
    mkdir practica_fastapi
    cd practica_fastapi
    ```

3.  **Crea un entorno virtual con `pyenv`:**
    Usaremos una versión reciente de Python. Reemplaza `3.11.6` con cualquier versión que tengas instalada a través de `pyenv`. Puedes ver tus versiones instaladas con `pyenv versions`.

    ```bash
    # Sintaxis: pyenv virtualenv <version_python> <nombre_del_entorno>
    pyenv virtualenv 3.11.6 fastapi-practica
    ```

4.  **Asigna el entorno virtual a tu directorio:**
    Este comando crea un archivo `.python-version` en tu directorio actual, que le indica a `pyenv` que active automáticamente el entorno `fastapi-practica` cuando estés en esta carpeta.

    ```bash
    # Sintaxis: pyenv local <nombre_del_entorno>
    pyenv local fastapi-practica
    ```
    Ahora, tu terminal debería mostrar el nombre del entorno activado.

---

### **Paso 2: Instalar Dependencias**

Con el entorno activado, instala FastAPI y Uvicorn, el servidor ASGI que ejecutará tu aplicación.

```bash
# Instala fastapi y uvicorn con sus dependencias estándar para mejor rendimiento
pip install fastapi "uvicorn[standard]"
```

---

### **Paso 3: Crear la Aplicación "Hola Mundo"**

Crea un archivo llamado `main.py` y añade el siguiente código.

1.  **Crea el archivo:**
    ```bash
    touch main.py
    ```

2.  **Añade el código a `main.py`:**
    ```python
    from fastapi import FastAPI

    # Crea una instancia de la aplicación FastAPI
    app = FastAPI()


    # Define un "path operation decorator" en la ruta raíz ("/")
    @app.get("/")
    def read_root():
        """
        Este endpoint devuelve un saludo simple.
        """
        return {"Hello": "World"}

    ```

---

### **Paso 4: Ejecutar el Servidor de Desarrollo**

Ahora, inicia el servidor Uvicorn para que tu API esté activa.

```bash
# uvicorn main:app --reload
#
# - main: Se refiere al archivo main.py
# - app: Es el objeto FastAPI creado dentro de main.py (app = FastAPI())
# - --reload: Hace que el servidor se reinicie automáticamente cada vez que cambies el código.
#
uvicorn main:app --reload
```

El servidor estará corriendo y escuchando en `http://127.0.0.1:8000`.

---

### **Paso 5: Verificar la Aplicación**

1.  **Visita la API:**
    Abre tu navegador y ve a `http://127.0.0.1:8000`. Deberías ver la respuesta JSON:
    ```json
    {"Hello":"World"}
    ```

2.  **Explora la Documentación Interactiva:**
    FastAPI genera automáticamente documentación interactiva para tu API. Ve a `http://127.0.0.1:8000/docs`.
    Desde aquí, puedes ver tus endpoints y probarlos directamente desde el navegador.

---

¡Felicidades! Has configurado e iniciado con éxito un proyecto FastAPI utilizando `pyenv`.


---
---

## **Siguientes Pasos: Proyecto Avanzado - API de Agregación Asíncrona**

Ahora que tienes las bases, construiremos un proyecto más complejo que integra varios tópicos avanzados de Python y FastAPI.

**Objetivo:** Crear una API que obtiene datos del clima y noticias de APIs externas de forma concurrente, los guarda en una base de datos y notifica a los clientes conectados por WebSocket en tiempo real.

**Tópicos a cubrir:**
*   Programación asíncrona (`asyncio`, `httpx`)
*   Tareas en segundo plano (`BackgroundTasks`)
*   WebSockets para comunicación en tiempo real
*   ORM Asíncrono con SQLAlchemy

### **Paso 1: Instalar Dependencias Adicionales**

Necesitaremos `httpx` para hacer peticiones HTTP asíncronas y `SQLAlchemy` con un driver `async`.

```bash
pip install httpx sqlalchemy "aiosqlite"
```

### **Paso 2: Estructura del Proyecto**

Crea los siguientes archivos dentro de tu directorio `practica_fastapi`:

```
. (practica_fastapi)
├── main.py
├── api_clients.py
├── database.py
├── models.py
└── websocket_manager.py
```

### **Paso 3: Configurar la Base de Datos (`database.py` y `models.py`)**

1.  **En `database.py`, configura la conexión asíncrona a la base de datos:**

    ```python
    # database.py
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker, declarative_base

    DATABASE_URL = "sqlite+aiosqlite:///./database.db"

    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    Base = declarative_base()
    ```

2.  **En `models.py`, define la tabla para guardar los datos:**

    ```python
    # models.py
    from sqlalchemy import Column, Integer, String, Float
    from .database import Base

    class Report(Base):
        __tablename__ = "reports"

        id = Column(Integer, primary_key=True, index=True)
        source = Column(String, index=True)
        data = Column(String)
    ```

### **Paso 4: Crear Clientes de API Asíncronos (`api_clients.py`)**

Aquí simularemos la obtención de datos de dos fuentes externas de forma concurrente.

```python
# api_clients.py
import asyncio
import httpx
import random

async def get_weather_data():
    """Simula la obtención de datos del clima."""
    await asyncio.sleep(random.uniform(0.5, 1.5)) # Simula latencia de red
    temp = round(random.uniform(-10, 30), 2)
    return {"source": "weather", "data": f"{temp}°C"}

async def get_news_data():
    """Simula la obtención de noticias."""
    await asyncio.sleep(random.uniform(0.5, 1.5)) # Simula latencia de red
    headlines = ["Python 4.0 Anunciado", "FastAPI domina el desarrollo web", "Uvicorn más rápido que nunca"]
    return {"source": "news", "data": random.choice(headlines)}

async def fetch_all_data():
    """Ejecuta todos los clientes de API de forma concurrente."""
    results = await asyncio.gather(
        get_weather_data(),
        get_news_data()
    )
    return results
```

### **Paso 5: Gestionar WebSockets (`websocket_manager.py`)**

Este módulo se encargará de mantener y notificar a los clientes conectados.

```python
# websocket_manager.py
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
```

### **Paso 6: Unir Todo en `main.py`**

Modifica tu `main.py` para orquestar todos los componentes.

```python
# main.py
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlalchemy.future import select

from database import Base, engine, async_session
from models import Report
from api_clients import fetch_all_data
from websocket_manager import manager

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Crear tablas en la base de datos
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Iniciar la tarea de fondo para actualizar datos
    asyncio.create_task(update_data_periodically())

async def update_data_periodically():
    while True:
        print("Actualizando datos...")
        new_data = await fetch_all_data()
        
        async with async_session() as session:
            # Borrar datos viejos
            await session.execute(Report.__table__.delete())
            # Insertar datos nuevos
            for item in new_data:
                report = Report(source=item['source'], data=item['data'])
                session.add(report)
            await session.commit()

        # Notificar a clientes WebSocket
        await manager.broadcast(json.dumps(new_data))
        
        await asyncio.sleep(15) # Esperar 15 segundos

@app.get("/api/dashboard")
async def get_dashboard_data():
    async with async_session() as session:
        result = await session.execute(select(Report))
        reports = result.scalars().all()
        return reports

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Mantener la conexión viva
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### **Paso 7: Probar la Aplicación Completa**

1.  **Ejecuta el servidor:** `uvicorn main:app --reload`
2.  **Abre el cliente WebSocket:** Usa una herramienta como `websocat` o un cliente de navegador para conectarte a `ws://127.0.0.1:8000/ws/updates`.
3.  **Observa los logs:** Verás el mensaje "Actualizando datos..." cada 15 segundos en tu terminal.
4.  **Recibe actualizaciones:** Tu cliente WebSocket recibirá un mensaje JSON con los nuevos datos cada 15 segundos.
5.  **Consulta la API:** Mientras todo corre, visita `http://127.0.0.1:8000/api/dashboard` para ver los datos más recientes almacenados en la base de datos.