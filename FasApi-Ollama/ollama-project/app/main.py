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