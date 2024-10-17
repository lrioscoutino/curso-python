
# Docker y Docker Compose implementado en Django

Docker es una plataforma que permite crear, ejecutar y gestionar aplicaciones en **contenedores**. Un contenedor incluye todo el entorno necesario para que una aplicación funcione de manera consistente, independientemente del sistema operativo o la infraestructura donde se ejecute. Esto es especialmente útil para el desarrollo de aplicaciones en Django, ya que permite estandarizar el entorno de desarrollo, pruebas y producción.

**Docker Compose** es una herramienta que permite definir y ejecutar aplicaciones multicontenedor. Para una aplicación Django, puedes definir los servicios necesarios, como la base de datos, el servidor web, Redis, etc., en un solo archivo, facilitando la gestión y configuración.

## 1. Instalación de Docker y Docker Compose

Primero, asegúrate de tener Docker y Docker Compose instalados en tu máquina. Puedes seguir la [documentación oficial de Docker](https://docs.docker.com/get-docker/) para instalarlo.

## 2. Crear un proyecto Django

Si aún no tienes un proyecto Django, puedes crear uno ejecutando los siguientes comandos:

```bash
django-admin startproject myproject
cd myproject
```

## 3. Estructura del proyecto

Supongamos que ya tienes un proyecto Django básico. La estructura de tu proyecto será algo así:

```
myproject/
│
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── Dockerfile
└── docker-compose.yml
```

## 4. Crear un Dockerfile

El archivo \`Dockerfile\` define la imagen de Docker para nuestra aplicación Django. Aquí te muestro un ejemplo de cómo configurarlo:

```Dockerfile
# Usar la imagen oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos y luego instalarlos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto a la carpeta de trabajo
COPY . /app/

# Exponer el puerto 8000 para el servidor Django
EXPOSE 8000

# Comando para ejecutar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 5. Crear un archivo \`requirements.txt\`

El archivo \`requirements.txt\` debe contener las dependencias necesarias para el proyecto, como Django y otras bibliotecas que estés utilizando. Por ejemplo:

```
Django==4.2
djangorestframework==3.14
```

## 6. Crear el archivo \`docker-compose.yml\`

Docker Compose nos permitirá levantar el entorno de Django y cualquier otro servicio que necesitemos (como una base de datos) con un solo comando. A continuación, un ejemplo de cómo configurarlo:

```yaml
version: '3'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://myuser:mypassword@db:5432/mydatabase

volumes:
  postgres_data:
```

## 7. Configurar la base de datos en \`settings.py\`

Debes asegurarte de que tu proyecto Django está configurado para usar PostgreSQL en lugar de la base de datos por defecto (SQLite). En el archivo \`settings.py\`, configura la base de datos de la siguiente manera:

```python
import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
```

Asegúrate de tener instalado \`dj-database-url\` en tu archivo \`requirements.txt\`:

```
dj-database-url==0.5.0
```

## 8. Levantar los contenedores

Una vez que tengas configurados el \`Dockerfile\` y \`docker-compose.yml\`, puedes levantar los contenedores con el siguiente comando:

```bash
docker-compose up
```

Esto creará los contenedores, iniciará la base de datos y la aplicación Django, y podrás acceder a tu aplicación en \`http://localhost:8000\`.

## 9. Ejecutar migraciones

Como estamos usando PostgreSQL en contenedores, debemos ejecutar las migraciones para preparar la base de datos. En una nueva terminal, ejecuta el siguiente comando:

```bash
docker-compose run web python manage.py migrate
```

## 10. Administra los contenedores

Algunos comandos útiles para manejar los contenedores con Docker Compose son:

- **Iniciar los contenedores**: \`docker-compose up\`
- **Detener los contenedores**: \`docker-compose down\`
- **Reconstruir los contenedores (si haces cambios en el Dockerfile)**: \`docker-compose up --build\`
- **Ver los logs de los contenedores**: \`docker-compose logs\`
  
## Conclusión

Docker y Docker Compose facilitan la creación de un entorno reproducible para un proyecto Django, lo que garantiza que funcione de la misma manera en diferentes máquinas y entornos. Con esta configuración, podrás tener un entorno de desarrollo consistente, y también será más fácil implementar tu aplicación en producción.
