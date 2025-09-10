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