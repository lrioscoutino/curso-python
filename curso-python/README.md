### Tarea: **Consumo de APIs en Python**

**Objetivo:** Aprender a consumir APIs en Python, utilizar datos de fuentes externas, procesarlos y presentarlos de manera adecuada.

---

### Introducción:

Una **API (Interfaz de Programación de Aplicaciones)** es un conjunto de reglas que permiten que un software interactúe con otro software. Las APIs web permiten que los programas se comuniquen a través de Internet y accedan a servicios o datos de manera eficiente.

En el consumo de APIs, Python ofrece varias herramientas, siendo una de las más populares el módulo `requests`, que simplifica el proceso de hacer solicitudes HTTP (GET, POST, PUT, DELETE, etc.) y trabajar con los datos que estas devuelven, generalmente en formato JSON.

---

### Ejercicio Práctico:

Vas a consumir una API pública de clima para obtener el pronóstico del tiempo en una ciudad específica. Utilizaremos la API de [OpenWeatherMap](https://openweathermap.org/api) para este ejemplo.

#### Requisitos:
1. Crear un script que consuma la API de OpenWeatherMap usando el módulo `requests`.
2. El usuario deberá ingresar el nombre de una ciudad, y el script mostrará:
   - La temperatura actual.
   - La descripción del clima (ej. “clear sky”).
   - La humedad.
3. En caso de error (por ejemplo, si el nombre de la ciudad no existe), manejar adecuadamente las excepciones y errores HTTP.

#### Paso 1: Instalación de la biblioteca `requests`
Si aún no tienes instalada la biblioteca `requests`, puedes instalarla usando `pip`:

```bash
pip install requests
```

#### Paso 2: Crear una cuenta en OpenWeatherMap
Necesitas crear una cuenta en [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) para obtener una **API Key**, que es necesaria para hacer solicitudes a su API.

#### Paso 3: Implementación del Código

Crea un script Python que siga la estructura que se presenta a continuación:

```python
import requests
import json

def obtener_clima(ciudad, api_key):
    # URL base de la API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"
    
    try:
        # Hacer la solicitud a la API
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Verificar si hubo algún error en la solicitud
        datos = respuesta.json()  # Convertir los datos a formato JSON

        # Extraer y mostrar los datos relevantes
        temperatura = datos['main']['temp']
        descripcion_clima = datos['weather'][0]['description']
        humedad = datos['main']['humidity']
        
        print(f"Clima en {ciudad.capitalize()}:")
        print(f"Temperatura: {temperatura}°C")
        print(f"Descripción: {descripcion_clima}")
        print(f"Humedad: {humedad}%")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except Exception as err:
        print(f"Error: {err}")

# Obtener la ciudad del usuario
ciudad = input("Ingresa el nombre de una ciudad: ")

# Aquí deberías ingresar tu API key de OpenWeatherMap
api_key = "tu_api_key_aqui"

# Llamar a la función para obtener el clima
obtener_clima(ciudad, api_key)
```

#### Explicación del Código:
1. **API URL**: La URL de la API incluye el nombre de la ciudad y tu API key. La opción `units=metric` se usa para obtener los resultados en grados Celsius.
2. **Manejo de errores**: Usamos `requests.exceptions.HTTPError` para manejar posibles errores HTTP, y `try-except` para manejar excepciones generales.
3. **Salida de datos**: El script extrae y muestra la temperatura, la descripción del clima y la humedad de la respuesta de la API.

#### Paso 4: Prueba

1. **Corre el script** y prueba ingresando nombres de varias ciudades, como "London", "Paris", "New York", o cualquier otra.
2. Verifica el manejo de errores ingresando un nombre de ciudad incorrecto, como "Xyz123".

---

### Tarea:

1. **Modificación**: Modifica el script para que también muestre la **velocidad del viento** y el **país** al que pertenece la ciudad.
2. **Repetir solicitudes**: Permite que el usuario ingrese varias ciudades en una misma ejecución del programa. Esto se puede hacer añadiendo un ciclo que solo se detenga cuando el usuario desee salir.
3. **Presentación**: Formatea la salida para que sea más clara y legible, por ejemplo:

```
Clima en Londres, UK:
-------------------------------------
Temperatura: 15°C
Descripción: cielo claro
Humedad: 50%
Velocidad del viento: 5.1 m/s
```

---

### Instrucciones de Entrega:
1. Implementa el código solicitado y guárdalo en un archivo `.py`.
2. Sube tu código a un repositorio de GitHub o envíalo comprimido en un archivo `.zip` agergando video o screenshots de pantalla.
3. Fecha de entrega: **21/Octubre/2024**.
4. Criterios de evaluación:
   - Correctitud del resultado.
   - Manejo adecuado de excepciones y errores.
   - Claridad y legibilidad del código.

---

### Recursos Sugeridos:
- [Documentación oficial de requests](https://docs.python-requests.org/en/master/)
- [API de OpenWeatherMap](https://openweathermap.org/current)
- [Manejo de errores en requests](https://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions)

---

Esta tarea te permitirá familiarizarte con el uso de APIs en Python, y te dará experiencia en el procesamiento de datos provenientes de servicios externos.