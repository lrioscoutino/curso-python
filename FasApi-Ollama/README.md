# Estructura del proyecto
# /ollama-fastapi-project
# ├── app
# │   ├── __init__.py
# │   ├── main.py
# │   ├── ollama_client.py
# │   └── templates
# │       ├── index.html
# │       └── response.html
# ├── requirements.txt
# └── README.md

# app/__init__.py
# Archivo vacío para convertir la carpeta en un paquete de Python

# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from . import ollama_client

app = FastAPI(title="Ollama DeepSeek API")

# Configuración de plantillas
templates = Jinja2Templates(directory="app/templates")

# Opcional: Agregar archivos estáticos
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página principal con formulario para consultar a DeepSeek"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, prompt: str = Form(...), temperature: float = Form(0.7), max_tokens: int = Form(1024)):
    """Procesa el formulario y envía la consulta a Ollama DeepSeek"""
    try:
        response = await ollama_client.generate_response(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "prompt": prompt,
                "response": response,
                "success": True
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "response.html",
            {
                "request": request,
                "prompt": prompt,
                "response": f"Error al procesar la solicitud: {str(e)}",
                "success": False
            }
        )

# app/ollama_client.py
import httpx
import json
import asyncio
from typing import Dict, Any, Optional

# URL de la API Ollama local
OLLAMA_API_URL = "http://localhost:11434/api/generate"

async def generate_response(
    prompt: str, 
    model: str = "deepseek", 
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> str:
    """
    Envía una solicitud a la API de Ollama y recibe la respuesta del modelo DeepSeek.
    
    Args:
        prompt: El texto de entrada para el modelo
        model: El nombre del modelo a utilizar
        temperature: Control de aleatoriedad (0.0 - 1.0)
        max_tokens: Número máximo de tokens a generar
    
    Returns:
        str: La respuesta del modelo
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False  # Para recibir la respuesta completa, no en streaming
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            data = response.json()
            return data.get("response", "")
    except httpx.HTTPError as e:
        raise Exception(f"Error HTTP al comunicarse con Ollama: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Error al decodificar la respuesta de Ollama")
    except Exception as e:
        raise Exception(f"Error inesperado: {str(e)}")

# app/templates/index.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama DeepSeek - Consulta</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        textarea, input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        textarea {
            min-height: 150px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .parameters {
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }
        .parameters .form-group {
            flex: 1;
        }
    </style>
</head>
<body>
    <h1>Consulta al modelo DeepSeek</h1>
    
    <form action="/generate" method="post">
        <div class="form-group">
            <label for="prompt">Prompt:</label>
            <textarea id="prompt" name="prompt" required placeholder="Escribe tu prompt aquí..."></textarea>
        </div>
        
        <div class="parameters">
            <div class="form-group">
                <label for="temperature">Temperatura:</label>
                <input type="number" id="temperature" name="temperature" min="0" max="1" step="0.1" value="0.7">
            </div>
            
            <div class="form-group">
                <label for="max_tokens">Tokens máximos:</label>
                <input type="number" id="max_tokens" name="max_tokens" min="1" max="4096" value="1024">
            </div>
        </div>
        
        <div class="form-group">
            <button type="submit">Generar respuesta</button>
        </div>
    </form>
</body>
</html>

# app/templates/response.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepSeek - Respuesta</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1, h2 {
            color: #333;
        }
        .prompt, .response {
            margin-bottom: 30px;
        }
        .prompt h2, .response h2 {
            padding-bottom: 5px;
            border-bottom: 1px solid #eee;
        }
        pre {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        .success {
            color: #2e7d32;
        }
        .error {
            color: #c62828;
        }
        .actions {
            margin-top: 30px;
        }
        .actions a {
            display: inline-block;
            background-color: #2196F3;
            color: white;
            padding: 10px 15px;
            text-decoration: none;
            border-radius: 4px;
        }
        .actions a:hover {
            background-color: #0b7dda;
        }
    </style>
</head>
<body>
    <h1>Respuesta del modelo DeepSeek</h1>
    
    <div class="prompt">
        <h2>Tu prompt:</h2>
        <pre>{{ prompt }}</pre>
    </div>
    
    <div class="response">
        <h2>Respuesta{% if not success %} <span class="error">(Error)</span>{% endif %}:</h2>
        <pre {% if not success %}class="error"{% endif %}>{{ response }}</pre>
    </div>
    
    <div class="actions">
        <a href="/">Realizar otra consulta</a>
    </div>
</body>
</html>

# requirements.txt
fastapi==0.105.0
uvicorn==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
httpx==0.25.1

# README.md
# Proyecto FastAPI para consumir Ollama DeepSeek

Este proyecto proporciona una interfaz web simple para interactuar con el modelo DeepSeek de Ollama a través de FastAPI.

## Requisitos

- Python 3.7+
- Ollama instalado y ejecutándose en tu máquina
- El modelo DeepSeek descargado en Ollama

## Instalación

1. Clona este repositorio:
```
git clone https://github.com/yourusername/ollama-fastapi-project.git
cd ollama-fastapi-project
```

2. Crea un entorno virtual e instala las dependencias:
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Asegúrate de tener Ollama instalado y el modelo DeepSeek disponible:
```
ollama pull deepseek
```

## Ejecución

1. Inicia Ollama en tu máquina (si no está ejecutándose ya):
```
ollama serve
```

2. En otra terminal, inicia la aplicación FastAPI:
```
uvicorn app.main:app --reload
```

3. Abre tu navegador y ve a http://localhost:8000

## Uso

1. Introduce tu prompt en el formulario
2. Ajusta la temperatura y el número máximo de tokens según tus necesidades
3. Haz clic en "Generar respuesta"
4. Verás la respuesta del modelo en la página siguiente

## Personalización

- Puedes cambiar el modelo predeterminado modificando el parámetro `model` en `ollama_client.py`
- Añade más parámetros al formulario según sea necesario
- Personaliza los estilos CSS en los archivos HTML