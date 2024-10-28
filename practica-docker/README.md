# Práctica de Docker: Nivel Principiante

## Objetivos de Aprendizaje
- Entender los conceptos básicos de Docker
- Aprender comandos esenciales de Docker
- Crear tu primer contenedor
- Trabajar con imágenes Docker
- Crear un Dockerfile simple

## Parte 1: Primeros Pasos con Docker

### 1.1 Verificar la Instalación
```bash
# Verificar la versión de Docker
docker --version

# Verificar que Docker está funcionando correctamente
docker run hello-world
```

### 1.2 Comandos Básicos
Practica estos comandos esenciales:
```bash
# Listar imágenes
docker images

# Listar contenedores en ejecución
docker ps

# Listar todos los contenedores (incluso los detenidos)
docker ps -a

# Eliminar un contenedor
docker rm [ID_CONTENEDOR]

# Eliminar una imagen
docker rmi [NOMBRE_IMAGEN]
```

## Parte 2: Tu Primera Aplicación en Docker

### 2.1 Crear una Aplicación Web Simple
Crea un nuevo directorio para el proyecto:
```bash
mkdir mi-primera-app-docker
cd mi-primera-app-docker
```

Crea un archivo `index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Mi Primera App Docker</title>
</head>
<body>
    <h1>¡Hola desde Docker!</h1>
    <p>Esta es mi primera aplicación usando Docker.</p>
</body>
</html>
```

### 2.2 Crear tu Primer Dockerfile
Crea un archivo llamado `Dockerfile`:
```dockerfile
# Usar nginx como imagen base
FROM nginx:alpine

# Copiar el archivo index.html al directorio de nginx
COPY index.html /usr/share/nginx/html/
```

### 2.3 Construir y Ejecutar
```bash
# Construir la imagen
docker build -t mi-primera-web .

# Ejecutar el contenedor
docker run -d -p 8080:80 mi-primera-web

# Verificar que el contenedor está corriendo
docker ps
```

Visita http://localhost:8080 en tu navegador para ver tu aplicación.

## Parte 3: Trabajando con Contenedores

### 3.1 Operaciones Básicas
Practica estos comandos:
```bash
# Detener un contenedor
docker stop [ID_CONTENEDOR]

# Iniciar un contenedor detenido
docker start [ID_CONTENEDOR]

# Ver los logs de un contenedor
docker logs [ID_CONTENEDOR]

# Entrar a un contenedor en ejecución
docker exec -it [ID_CONTENEDOR] /bin/sh
```

### 3.2 Ejercicio Práctico con Base de Datos
```bash
# Ejecutar un contenedor de MongoDB
docker run -d --name mi-mongodb -p 27017:27017 mongo

# Ver los logs de MongoDB
docker logs mi-mongodb

# Conectarse al contenedor de MongoDB
docker exec -it mi-mongodb mongosh
```

## Parte 4: Creando una Aplicación Multi-Container

### 4.1 Aplicación Python con Redis
Crea un archivo `app.py`:
```python
from flask import Flask
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    contador = redis_client.incr('visitas')
    return f'¡Esta página ha sido visitada {contador} veces!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Crea un archivo `requirements.txt`:
```
flask
redis
```

Crea un nuevo `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
COPY app.py .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### 4.2 Docker Compose
Crea un archivo `docker-compose.yml`:
```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis
  redis:
    image: redis:alpine
```

Para ejecutar:
```bash
docker-compose up -d
```

## Ejercicios Prácticos

1. **Ejercicio de Imágenes**
   - Descarga la imagen de Ubuntu
   - Lista todas las imágenes
   - Elimina la imagen de Ubuntu

2. **Ejercicio de Contenedores**
   - Crea un contenedor de Nginx
   - Modifica su página de inicio
   - Crea una nueva imagen a partir del contenedor modificado

3. **Ejercicio de Volúmenes**
   - Crea un volumen
   - Monta el volumen en un contenedor
   - Verifica la persistencia de datos

## Evaluación
Para completar esta práctica, deberás:
1. Crear y ejecutar todos los ejemplos mostrados
2. Completar los ejercicios prácticos
3. Documentar los comandos utilizados y sus resultados
4. Explicar cualquier error encontrado y cómo lo solucionaste

## Referencias y Recursos Adicionales
- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Cheat Sheet](https://www.docker.com/sites/default/files/d8/2019-09/docker-cheat-sheet.pdf)
