# 📝 Práctica: Consumo de APIs en Python con POO

## 🎯 Objetivo
Aprender a consumir **APIs públicas** en Python utilizando **Programación Orientada a Objetos (POO)**.  
Al finalizar, deberás ser capaz de:
- Encapsular la lógica de conexión en una clase.
- Realizar peticiones GET y POST.
- Manejar errores y respuestas en formato JSON.
- Mostrar resultados de forma clara.

---

## 📘 Parte 1: Implementación de la clase `APIClient`

Crea un archivo llamado `api_client.py` con la siguiente clase base:

```python
import requests

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def get(self, endpoint="", params=None):
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}", 
                params=params, 
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en GET: {e}")
            return None

    def post(self, endpoint="", data=None, json=None):
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}", 
                data=data, 
                json=json, 
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en POST: {e}")
            return None
```

---

## 📘 Parte 2: Ejercicio práctico

### Instrucciones
1. Crea un archivo `api_practica_poo.py`.
2. Importa tu clase `APIClient`.
3. Elige **dos APIs** de la siguiente lista:
   - **Agify API** → Predice edad según nombre.  
     URL: `https://api.agify.io?name=Pedro`
   - **JokeAPI** → Obtiene un chiste aleatorio.  
     URL: `https://official-joke-api.appspot.com/random_joke`
   - **Dog API** → Devuelve foto aleatoria de un perro.  
     URL: `https://dog.ceo/api/breeds/image/random`

4. Crea instancias de `APIClient` y realiza consultas.
5. Muestra la información de manera ordenada en pantalla.

---

## 📌 Ejemplo esperado de salida

```
>>> python api_practica_poo.py

Consulta a Agify:
Nombre: Pedro
Edad estimada: 52
Número de registros: 14000

Consulta a JokeAPI:
Setup: ¿Por qué la computadora fue al médico?
Punchline: Porque tenía un virus.

Consulta a DogAPI:
URL Imagen: https://images.dog.ceo/breeds/husky/n02110185_1469.jpg
```

---