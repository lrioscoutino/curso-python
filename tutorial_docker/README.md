# Tutorial de Docker: De la Teoria a la Practica

## Guia completa para estudiantes universitarios

> **Requisitos previos**: Linux (Ubuntu), terminal basica, conocimientos basicos de redes.
> **Docker version**: 29.x+ con Docker Compose v5+

---

## Tabla de Contenidos

1. [Fundamentos teoricos](#1-fundamentos-teoricos)
2. [Instalacion y primeros pasos](#2-instalacion-y-primeros-pasos)
3. [Imagenes de Docker](#3-imagenes-de-docker)
4. [Contenedores](#4-contenedores)
5. [Dockerfile - Construir imagenes propias](#5-dockerfile---construir-imagenes-propias)
6. [Volumenes y persistencia de datos](#6-volumenes-y-persistencia-de-datos)
7. [Redes en Docker](#7-redes-en-docker)
8. [Docker Compose - Aplicaciones multi-contenedor](#8-docker-compose---aplicaciones-multi-contenedor)
9. [Ejercicios practicos resueltos](#9-ejercicios-practicos-resueltos)
10. [Ejercicios propuestos](#10-ejercicios-propuestos)

---

## 1. Fundamentos Teoricos

### 1.1 El problema que resuelve Docker

En el desarrollo de software tradicional existe un problema clasico:

```
"En mi maquina funciona" -> En el servidor no funciona
```

Esto ocurre porque cada maquina tiene diferentes:
- Versiones de lenguajes (Python 3.8 vs 3.12)
- Librerias del sistema operativo
- Variables de entorno
- Configuraciones

**Docker resuelve esto empaquetando la aplicacion junto con TODO lo que necesita**
para ejecutarse en una unidad llamada **contenedor**.

### 1.2 Contenedores vs Maquinas Virtuales

```
 MAQUINA VIRTUAL                    CONTENEDOR DOCKER
+-------------------+              +-------------------+
| App A  | App B    |              | App A  | App B    |
+--------+----------+              +--------+----------+
| Bins/  | Bins/    |              | Bins/  | Bins/    |
| Libs   | Libs     |              | Libs   | Libs     |
+--------+----------+              +--------+----------+
| Guest  | Guest    |              |   Docker Engine    |
| OS     | OS       |              +--------------------+
+--------+----------+              |   Sistema Operativo|
|     Hypervisor     |              |   Host (Linux)     |
+--------------------+              +--------------------+
|  Sistema Operativo |              |     Hardware       |
|  Host              |              +--------------------+
+--------------------+
|     Hardware       |
+--------------------+
```

| Caracteristica | Maquina Virtual | Contenedor |
|---|---|---|
| Tamano | GBs (incluye SO completo) | MBs (solo app + dependencias) |
| Arranque | Minutos | Segundos |
| Aislamiento | Completo (hardware virtual) | A nivel de proceso (namespaces) |
| Rendimiento | Overhead del hypervisor | Casi nativo |
| SO invitado | Necesita uno completo | Comparte kernel del host |
| Densidad | ~10 VMs por servidor | ~100+ contenedores por servidor |

### 1.3 Arquitectura de Docker

```
+-------------------------------------------------------------+
|                     Docker CLI (docker)                      |
|            Comandos: run, build, pull, push, ...             |
+------------------------------+------------------------------+
                               |
                          REST API
                               |
+------------------------------v------------------------------+
|                     Docker Daemon (dockerd)                  |
|                                                              |
|  +------------------+  +-------------+  +-----------------+  |
|  | Gestion de       |  | Gestion de  |  | Gestion de      |  |
|  | Contenedores     |  | Imagenes    |  | Redes/Volumenes |  |
|  +------------------+  +-------------+  +-----------------+  |
|                                                              |
+------------------------------+------------------------------+
                               |
              +----------------+----------------+
              |                |                |
        +-----------+   +-----------+   +-----------+
        | containerd|   | Imagenes  |   | Redes     |
        | (runtime) |   | (layers)  |   | (bridge)  |
        +-----------+   +-----------+   +-----------+
```

**Componentes clave:**

- **Docker CLI**: la herramienta de linea de comandos que usamos.
- **Docker Daemon** (`dockerd`): servicio que gestiona todo en segundo plano.
- **Imagenes**: plantillas de solo lectura con el SO base + app + dependencias.
- **Contenedores**: instancias en ejecucion de una imagen.
- **Registros**: repositorios de imagenes (Docker Hub, GitHub Container Registry).

### 1.4 Tecnologias del kernel que usa Docker

Docker no es magia; usa funcionalidades del kernel de Linux:

| Tecnologia | Que hace | Ejemplo |
|---|---|---|
| **Namespaces** | Aisla recursos entre contenedores | PID, Network, Mount, User |
| **cgroups** | Limita recursos (CPU, RAM) | "Este contenedor max 512MB RAM" |
| **Union FS** | Sistema de archivos por capas | OverlayFS - capas de imagen |
| **chroot** | Cambia el directorio raiz | Cada contenedor ve su propio `/` |

```
Namespaces - Aislamiento:
+--Container A--+  +--Container B--+
| PID 1: nginx  |  | PID 1: python |   <- Cada uno tiene su PID 1
| Net: 172.17.2 |  | Net: 172.17.3 |   <- Red independiente
| Mount: /app-a |  | Mount: /app-b |   <- Filesystem propio
+---------------+  +---------------+
        |                  |
+-------v------------------v--------+
|         Kernel de Linux            |   <- Comparten el mismo kernel
+------------------------------------+
```

### 1.5 Ciclo de vida de un contenedor

```
   Imagen               Contenedor             Contenedor
  (plantilla)           (creado)               (en ejecucion)
  +--------+    run     +--------+   start    +--------+
  | nginx  | --------> | stopped | --------> | running |
  | :latest|           |         |           |         |
  +--------+           +--------+           +--------+
                           ^                     |
                           |      stop           |
                           +---------------------+
                           |
                           |      rm
                           +---------> [eliminado]
```

Estados posibles:
- **Created**: contenedor creado pero no iniciado.
- **Running**: proceso principal en ejecucion.
- **Paused**: proceso congelado (SIGSTOP).
- **Stopped**: proceso termino (exit code 0 o error).
- **Removed**: contenedor eliminado del sistema.

---

## 2. Instalacion y Primeros Pasos

### 2.1 Instalacion en Ubuntu

```bash
# Actualizar paquetes
sudo apt update

# Instalar dependencias
sudo apt install -y ca-certificates curl gnupg

# Agregar clave GPG oficial de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Agregar el repositorio
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine + Compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER
# IMPORTANTE: Cerrar sesion y volver a entrar para que aplique
```

### 2.2 Verificar la instalacion

```bash
# Version de Docker
docker --version
# Docker version 29.2.1, build a5c7197

# Version de Compose
docker compose version
# Docker Compose version v5.0.2

# Informacion del sistema
docker info

# Prueba: ejecutar el contenedor de prueba
docker run hello-world
```

### 2.3 Entender el comando `docker run hello-world`

```
$ docker run hello-world

1. Docker busca la imagen "hello-world" localmente
   -> No la encuentra

2. La descarga de Docker Hub (pull)
   -> Descarga las capas de la imagen

3. Crea un contenedor a partir de la imagen
   -> Asigna namespaces, cgroups, filesystem

4. Ejecuta el proceso principal del contenedor
   -> Imprime el mensaje de bienvenida

5. El proceso termina -> el contenedor se detiene
```

---

## 3. Imagenes de Docker

### 3.1 Teoria: Que es una imagen

Una imagen es una **plantilla de solo lectura** compuesta por **capas** (layers):

```
+----------------------------------+
| Capa 4: COPY app.py /app/       |  <- Tu codigo
+----------------------------------+
| Capa 3: RUN pip install flask    |  <- Dependencias
+----------------------------------+
| Capa 2: RUN apt-get install python| <- Paquetes del SO
+----------------------------------+
| Capa 1: Ubuntu 22.04 base       |  <- Imagen base
+----------------------------------+
```

Cada capa es **inmutable** y se **reutiliza** entre imagenes. Si 10 contenedores
usan Ubuntu 22.04, la capa base se almacena UNA sola vez.

### 3.2 Comandos basicos de imagenes

```bash
# Buscar imagenes en Docker Hub
docker search nginx

# Descargar una imagen
docker pull nginx              # Descarga la ultima version (:latest)
docker pull nginx:1.25         # Version especifica
docker pull python:3.12-slim   # Variante slim (mas pequena)

# Listar imagenes locales
docker images
# REPOSITORY   TAG          IMAGE ID       SIZE
# nginx        latest       a8758716bb6a   187MB
# python       3.12-slim    f5d1b490b6a0   125MB

# Ver las capas de una imagen
docker history nginx

# Eliminar una imagen
docker rmi nginx:1.25

# Eliminar imagenes sin usar
docker image prune
```

### 3.3 Tags y versiones

```
nombre_imagen:tag

Ejemplos:
  python:3.12          -> Python 3.12 sobre Debian
  python:3.12-slim     -> Python 3.12 version reducida (~125MB vs ~900MB)
  python:3.12-alpine   -> Python 3.12 sobre Alpine Linux (~50MB)
  node:20-bookworm     -> Node 20 sobre Debian Bookworm
  ubuntu:22.04         -> Ubuntu 22.04 LTS
  nginx:latest         -> Ultima version estable de Nginx

Regla: NUNCA usar :latest en produccion.
       Siempre especificar la version exacta.
```

---

## 4. Contenedores

### 4.1 Crear y ejecutar contenedores

```bash
# Ejecutar un contenedor en primer plano
docker run nginx
# (bloquea la terminal, Ctrl+C para detener)

# Ejecutar en segundo plano (detached)
docker run -d nginx
# Retorna el ID del contenedor: a1b2c3d4e5f6...

# Ejecutar con nombre personalizado
docker run -d --name mi-nginx nginx

# Ejecutar y mapear puertos
# -p puerto_host:puerto_contenedor
docker run -d -p 8080:80 --name web nginx
# Ahora accesible en http://localhost:8080

# Ejecutar con terminal interactiva
docker run -it ubuntu bash
# Abre un shell dentro del contenedor
# "exit" para salir
```

### 4.2 Flags importantes de `docker run`

| Flag | Descripcion | Ejemplo |
|---|---|---|
| `-d` | Segundo plano (detached) | `docker run -d nginx` |
| `-it` | Terminal interactiva | `docker run -it ubuntu bash` |
| `-p` | Mapear puertos | `-p 8080:80` |
| `-v` | Montar volumen | `-v /host/dir:/container/dir` |
| `--name` | Nombre del contenedor | `--name mi-app` |
| `-e` | Variable de entorno | `-e DB_HOST=localhost` |
| `--rm` | Eliminar al detenerse | `docker run --rm nginx` |
| `--network` | Conectar a red | `--network mi-red` |
| `-m` | Limite de memoria | `-m 512m` |
| `--cpus` | Limite de CPUs | `--cpus 1.5` |

### 4.3 Gestionar contenedores

```bash
# Listar contenedores activos
docker ps

# Listar TODOS (incluye detenidos)
docker ps -a

# Ver logs de un contenedor
docker logs mi-nginx
docker logs -f mi-nginx          # Seguir en tiempo real (como tail -f)

# Ejecutar un comando dentro de un contenedor activo
docker exec -it mi-nginx bash    # Abrir shell
docker exec mi-nginx ls /etc     # Ejecutar un comando

# Detener un contenedor (SIGTERM, luego SIGKILL)
docker stop mi-nginx

# Iniciar un contenedor detenido
docker start mi-nginx

# Reiniciar
docker restart mi-nginx

# Eliminar un contenedor detenido
docker rm mi-nginx

# Forzar eliminacion (incluso si esta corriendo)
docker rm -f mi-nginx

# Ver uso de recursos en tiempo real
docker stats

# Inspeccionar configuracion completa
docker inspect mi-nginx
```

### 4.4 Limitar recursos (cgroups en accion)

```bash
# Limitar memoria a 256MB y 1 CPU
docker run -d --name limitado \
  -m 256m \
  --cpus 1.0 \
  nginx

# Verificar los limites
docker stats limitado --no-stream
# NAME       CPU %   MEM USAGE / LIMIT   MEM %
# limitado   0.00%   5.2MiB / 256MiB     2.03%
```

---

## 5. Dockerfile - Construir Imagenes Propias

### 5.1 Teoria: Que es un Dockerfile

Un **Dockerfile** es un archivo de texto con instrucciones paso a paso
para construir una imagen. Cada instruccion crea una **capa**.

### 5.2 Instrucciones del Dockerfile

| Instruccion | Proposito | Ejemplo |
|---|---|---|
| `FROM` | Imagen base (obligatoria, primera linea) | `FROM python:3.12-slim` |
| `WORKDIR` | Directorio de trabajo dentro del contenedor | `WORKDIR /app` |
| `COPY` | Copiar archivos del host al contenedor | `COPY . /app` |
| `ADD` | Como COPY pero soporta URLs y descompresion | `ADD app.tar.gz /app` |
| `RUN` | Ejecutar comando durante la construccion | `RUN pip install flask` |
| `ENV` | Definir variable de entorno | `ENV PORT=8000` |
| `EXPOSE` | Documentar el puerto que usa la app | `EXPOSE 8000` |
| `CMD` | Comando por defecto al iniciar contenedor | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Comando principal (no se sobreescribe facil) | `ENTRYPOINT ["python"]` |
| `VOLUME` | Declarar punto de montaje para datos | `VOLUME /data` |
| `ARG` | Variable solo durante build | `ARG VERSION=1.0` |
| `USER` | Usuario que ejecuta los comandos | `USER appuser` |

### 5.3 Ejemplo basico: App Python con Flask

**Estructura del proyecto:**

```
mi-app-flask/
├── Dockerfile
├── requirements.txt
└── app.py
```

**app.py:**

```python
from flask import Flask, jsonify
import platform
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "mensaje": "Hola desde Docker!",
        "hostname": platform.node(),
        "plataforma": platform.platform(),
        "python": platform.python_version(),
        "pid": os.getpid()
    })

@app.route("/salud")
def health():
    return jsonify({"estado": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

**requirements.txt:**

```
flask==3.1.1
```

**Dockerfile:**

```dockerfile
# 1. Imagen base: Python slim (pequena, ~125MB)
FROM python:3.12-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar SOLO requirements primero (optimiza cache de capas)
COPY requirements.txt .

# 4. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del codigo
COPY . .

# 6. Variable de entorno
ENV PORT=5000

# 7. Documentar el puerto
EXPOSE 5000

# 8. Comando para ejecutar la aplicacion
CMD ["python", "app.py"]
```

**Construir y ejecutar:**

```bash
# Construir la imagen
docker build -t mi-flask-app:1.0 .
# -t = tag (nombre:version)
# .  = contexto de build (directorio actual)

# Ejecutar
docker run -d -p 5000:5000 --name flask-app mi-flask-app:1.0

# Probar
curl http://localhost:5000
# {"hostname":"a1b2c3d4","mensaje":"Hola desde Docker!",...}

# Ver logs
docker logs flask-app
```

### 5.4 Optimizacion del Dockerfile: Multi-stage Build

Los **multi-stage builds** permiten compilar en una imagen grande y copiar
solo el resultado a una imagen pequena:

```dockerfile
# === ETAPA 1: Compilacion ===
FROM python:3.12 AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# === ETAPA 2: Produccion (imagen final) ===
FROM python:3.12-slim

WORKDIR /app

# Copiar SOLO las dependencias instaladas (no pip, no compiladores)
COPY --from=builder /install /usr/local

COPY . .

# Crear usuario no-root (seguridad)
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
```

Esto reduce el tamano de la imagen final significativamente.

### 5.5 .dockerignore

Archivo que excluye archivos del contexto de build (como `.gitignore`):

```
# .dockerignore
__pycache__
*.pyc
.git
.env
.venv
node_modules
*.md
.dockerignore
Dockerfile
docker-compose.yml
```

### 5.6 Buenas practicas para Dockerfiles

```
1. Usar imagenes base especificas    FROM python:3.12-slim  (NO python:latest)
2. Minimizar capas                   Combinar RUN con &&
3. Ordenar instrucciones por cambio  Lo que cambia menos va primero
4. Usar .dockerignore                No copiar archivos innecesarios
5. No ejecutar como root             USER appuser
6. Una responsabilidad por contenedor Un servicio = un contenedor
7. Usar multi-stage builds           Imagen final mas pequena
8. No guardar secretos en la imagen  Usar variables de entorno
```

---

## 6. Volumenes y Persistencia de Datos

### 6.1 Teoria: El problema de la persistencia

Los contenedores son **efimeros**: cuando se eliminan, sus datos desaparecen.
Los volumenes resuelven esto conectando directorios del host con el contenedor.

```
Sin volumen:                        Con volumen:
+--Contenedor--+                    +--Contenedor--+
| /app/data    |  docker rm ->      | /app/data    |----+
| datos.db     |  TODO SE PIERDE    | datos.db     |    |
+--------------+                    +--------------+    |
                                                        |
                                    +--Host-----------+ |
                                    | /var/lib/docker/ |<+
                                    | volumes/mi-vol/  |
                                    | datos.db         | <- PERSISTE
                                    +-----------------+
```

### 6.2 Tipos de almacenamiento

```
1. VOLUMES (recomendado)          Gestionados por Docker
   docker volume create datos     en /var/lib/docker/volumes/
   -v datos:/app/data

2. BIND MOUNTS                   Directorio especifico del host
   -v /home/user/data:/app/data  Tu controlas la ubicacion

3. TMPFS                         Solo en memoria RAM
   --tmpfs /app/cache            Desaparece al detener contenedor
```

### 6.3 Comandos de volumenes

```bash
# Crear un volumen
docker volume create mis-datos

# Listar volumenes
docker volume ls

# Inspeccionar un volumen
docker volume inspect mis-datos

# Usar volumen en un contenedor
docker run -d \
  -v mis-datos:/var/lib/postgresql/data \
  --name mi-postgres \
  postgres:16

# Bind mount (directorio del host)
docker run -d \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  -p 8080:80 \
  --name web \
  nginx
# :ro = read-only (el contenedor no puede modificar)

# Eliminar volumenes sin usar
docker volume prune

# Eliminar un volumen especifico
docker volume rm mis-datos
```

### 6.4 Ejemplo: Base de datos con datos persistentes

```bash
# Crear volumen para PostgreSQL
docker volume create pg-data

# Ejecutar PostgreSQL con volumen
docker run -d \
  --name mi-db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secreto123 \
  -e POSTGRES_DB=universidad \
  -v pg-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16

# Conectarse y crear datos
docker exec -it mi-db psql -U admin -d universidad -c "
  CREATE TABLE alumnos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    carrera VARCHAR(100)
  );
  INSERT INTO alumnos (nombre, carrera) VALUES
    ('Ana Garcia', 'Ingenieria en Sistemas'),
    ('Carlos Lopez', 'Ingenieria en Software');
"

# Eliminar el contenedor
docker rm -f mi-db

# Crear uno nuevo con el MISMO volumen
docker run -d \
  --name mi-db-nuevo \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secreto123 \
  -e POSTGRES_DB=universidad \
  -v pg-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16

# Verificar que los datos persisten
docker exec -it mi-db-nuevo psql -U admin -d universidad -c "SELECT * FROM alumnos;"
#  id |    nombre     |        carrera
# ----+---------------+-----------------------
#   1 | Ana Garcia    | Ingenieria en Sistemas
#   2 | Carlos Lopez  | Ingenieria en Software
```

---

## 7. Redes en Docker

### 7.1 Teoria: Redes de contenedores

Docker crea redes virtuales para que los contenedores se comuniquen entre si
y con el mundo exterior.

```
                    Internet
                       |
              +--------+--------+
              |   Host (Linux)  |
              |   eth0: 192.168.1.10
              |                 |
              |   docker0: 172.17.0.1  (bridge por defecto)
              |        |
              |   +----+----+--------+
              |   |         |        |
              | .0.2      .0.3     .0.4
              | nginx    python   postgres
              +-------------------------+
```

### 7.2 Tipos de redes

| Driver | Descripcion | Caso de uso |
|---|---|---|
| `bridge` | Red interna (por defecto) | Contenedores en un mismo host |
| `host` | Usa la red del host directamente | Maximo rendimiento de red |
| `none` | Sin red | Contenedores aislados |
| `overlay` | Red entre multiples hosts | Docker Swarm / clusters |

### 7.3 Comandos de redes

```bash
# Listar redes
docker network ls

# Crear una red personalizada
docker network create mi-red

# Ejecutar contenedores en la misma red
docker run -d --name web --network mi-red nginx
docker run -d --name api --network mi-red python:3.12-slim sleep infinity

# En redes personalizadas, los contenedores se encuentran POR NOMBRE
docker exec api ping web     # Funciona! Docker hace DNS automatico
# PING web (172.18.0.2): 56 data bytes

# En la red por defecto (bridge) NO hay DNS automatico
# Solo funciona por IP, por eso se recomienda crear redes propias

# Inspeccionar una red
docker network inspect mi-red

# Conectar un contenedor existente a una red
docker network connect mi-red otro-contenedor

# Desconectar
docker network disconnect mi-red otro-contenedor

# Eliminar red
docker network rm mi-red
```

### 7.4 Ejemplo: Comunicacion entre contenedores

```bash
# Crear red
docker network create app-network

# Base de datos
docker run -d \
  --name db \
  --network app-network \
  -e POSTGRES_PASSWORD=pass123 \
  postgres:16

# Aplicacion que se conecta a la base de datos
# Nota: usa "db" como hostname (nombre del contenedor)
docker run -it --rm \
  --network app-network \
  postgres:16 \
  psql -h db -U postgres
# Conecta exitosamente porque estan en la misma red
# Docker resuelve "db" -> 172.18.0.2 automaticamente
```

---

## 8. Docker Compose - Aplicaciones Multi-contenedor

### 8.1 Teoria: Por que Compose

En aplicaciones reales necesitas multiples servicios coordinados:

```
Aplicacion web tipica:
  - Frontend (nginx)
  - Backend (python/node)
  - Base de datos (postgres)
  - Cache (redis)
  - Cola de tareas (rabbitmq)

Sin Compose: 5 comandos "docker run" largos, dificiles de recordar
Con Compose: UN archivo YAML que describe todo
```

### 8.2 Estructura de docker-compose.yml

```yaml
# docker-compose.yml

# Definicion de servicios (contenedores)
services:
  nombre-servicio:
    image: imagen:tag          # Imagen de Docker Hub
    # O construir desde Dockerfile:
    build:
      context: ./directorio
      dockerfile: Dockerfile
    ports:
      - "8080:80"             # puerto_host:puerto_contenedor
    environment:
      - VARIABLE=valor
    volumes:
      - datos:/app/data       # Volumen nombrado
      - ./codigo:/app         # Bind mount
    depends_on:
      - otro-servicio         # Iniciar despues de este
    networks:
      - mi-red
    restart: unless-stopped    # Politica de reinicio

# Definicion de volumenes
volumes:
  datos:

# Definicion de redes
networks:
  mi-red:
    driver: bridge
```

### 8.3 Comandos de Docker Compose

```bash
# Levantar todos los servicios (en segundo plano)
docker compose up -d

# Ver estado de los servicios
docker compose ps

# Ver logs de todos los servicios
docker compose logs
docker compose logs -f api          # Seguir logs de un servicio

# Detener todos los servicios
docker compose down

# Detener y ELIMINAR volumenes (borra datos)
docker compose down -v

# Reconstruir imagenes
docker compose build
docker compose up -d --build        # Build + levantar

# Ejecutar comando en un servicio
docker compose exec api bash

# Escalar un servicio (multiples instancias)
docker compose up -d --scale api=3
```

### 8.4 Ejemplo completo: App web con API + DB + Cache

**docker-compose.yml:**

```yaml
services:
  # --- Base de datos PostgreSQL ---
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: app_pass
      POSTGRES_DB: app_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d app_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  # --- Cache Redis ---
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # --- API Backend (Python) ---
  api:
    build:
      context: ./api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://app_user:app_pass@db:5432/app_db
      REDIS_URL: redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    volumes:
      - ./api:/app    # Bind mount para desarrollo (hot reload)

  # --- Frontend (Nginx sirviendo archivos estaticos) ---
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - api

volumes:
  postgres_data:
```

---

## 9. Ejercicios Practicos Resueltos

### Ejercicio 1: Servidor web estatico con Nginx

**Objetivo**: Crear un contenedor Nginx que sirva una pagina HTML personalizada
usando un bind mount.

**Paso 1: Crear la estructura del proyecto.**

```bash
mkdir -p ~/docker-ejercicio1/html
cd ~/docker-ejercicio1
```

**Paso 2: Crear la pagina HTML.**

Archivo `html/index.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Primera Pagina en Docker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2496ed; }
        .info { background: #e8f4fd; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hola desde Docker + Nginx</h1>
        <p>Esta pagina esta siendo servida por un contenedor Docker.</p>
        <div class="info">
            <h3>Que esta pasando:</h3>
            <ul>
                <li>Nginx corre dentro de un contenedor Docker</li>
                <li>El puerto 80 del contenedor esta mapeado al 8080 del host</li>
                <li>Este archivo HTML esta montado via bind mount</li>
                <li>Si editas el HTML, los cambios se reflejan al instante</li>
            </ul>
        </div>
    </div>
</body>
</html>
```

**Paso 3: Ejecutar el contenedor.**

```bash
docker run -d \
  --name ejercicio1-web \
  -p 8080:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:alpine
```

**Paso 4: Verificar.**

```bash
# Verificar que esta corriendo
docker ps

# Probar con curl
curl http://localhost:8080

# Ver los logs
docker logs ejercicio1-web
```

**Paso 5: Modificar en caliente.**

```bash
# Editar el HTML (los cambios se ven inmediatamente)
echo "<h1>Pagina actualizada!</h1>" >> html/index.html

# Recargar el navegador o:
curl http://localhost:8080
```

**Paso 6: Limpiar.**

```bash
docker rm -f ejercicio1-web
```

**Conceptos aplicados:**
- `docker run` con flags `-d`, `-p`, `-v`, `--name`
- Bind mount con `:ro` (read-only)
- Mapeo de puertos
- Imagen oficial de Nginx

---

### Ejercicio 2: Aplicacion Python con Dockerfile personalizado

**Objetivo**: Crear una API REST con Flask, construir la imagen con un Dockerfile
y ejecutar el contenedor.

**Paso 1: Crear la estructura.**

```bash
mkdir -p ~/docker-ejercicio2
cd ~/docker-ejercicio2
```

**Paso 2: Crear la aplicacion.**

Archivo `app.py`:

```python
from flask import Flask, jsonify, request
import platform
import os
import datetime

app = Flask(__name__)

# Base de datos simulada en memoria
tareas = [
    {"id": 1, "titulo": "Aprender Docker", "completada": True},
    {"id": 2, "titulo": "Crear un Dockerfile", "completada": False},
    {"id": 3, "titulo": "Usar Docker Compose", "completada": False},
]


@app.route("/")
def info():
    """Informacion del sistema dentro del contenedor."""
    return jsonify({
        "servicio": "API de Tareas",
        "version": os.environ.get("APP_VERSION", "1.0"),
        "hostname": platform.node(),
        "python": platform.python_version(),
        "hora_servidor": datetime.datetime.now().isoformat(),
        "endpoints": ["/", "/tareas", "/tareas/<id>", "/salud"]
    })


@app.route("/tareas", methods=["GET"])
def listar_tareas():
    """Listar todas las tareas."""
    return jsonify({"total": len(tareas), "tareas": tareas})


@app.route("/tareas/<int:tarea_id>", methods=["GET"])
def obtener_tarea(tarea_id):
    """Obtener una tarea por ID."""
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(tarea)


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    """Crear una nueva tarea."""
    datos = request.get_json()
    if not datos or "titulo" not in datos:
        return jsonify({"error": "Se requiere 'titulo'"}), 400

    nueva = {
        "id": max(t["id"] for t in tareas) + 1 if tareas else 1,
        "titulo": datos["titulo"],
        "completada": False
    }
    tareas.append(nueva)
    return jsonify(nueva), 201


@app.route("/salud")
def health():
    """Health check para Docker."""
    return jsonify({"estado": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
```

Archivo `requirements.txt`:

```
flask==3.1.1
```

**Paso 3: Crear el Dockerfile.**

Archivo `Dockerfile`:

```dockerfile
# Imagen base ligera
FROM python:3.12-slim

# Metadatos
LABEL maintainer="estudiante@universidad.edu"
LABEL description="API de Tareas - Ejercicio Docker"

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (optimiza cache de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo de la aplicacion
COPY app.py .

# Variables de entorno
ENV PORT=5000
ENV APP_VERSION=1.0

# Documentar puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/salud')" || exit 1

# Comando de ejecucion
CMD ["python", "app.py"]
```

Archivo `.dockerignore`:

```
__pycache__
*.pyc
.git
.env
*.md
```

**Paso 4: Construir la imagen.**

```bash
# Build
docker build -t api-tareas:1.0 .

# Verificar
docker images | grep api-tareas
# api-tareas   1.0   abc123def   125MB
```

**Paso 5: Ejecutar y probar.**

```bash
# Ejecutar
docker run -d \
  --name api \
  -p 5000:5000 \
  -e APP_VERSION=1.0 \
  api-tareas:1.0

# Probar todos los endpoints
echo "=== Info del servidor ==="
curl -s http://localhost:5000 | python3 -m json.tool

echo "=== Listar tareas ==="
curl -s http://localhost:5000/tareas | python3 -m json.tool

echo "=== Obtener tarea 1 ==="
curl -s http://localhost:5000/tareas/1 | python3 -m json.tool

echo "=== Crear nueva tarea ==="
curl -s -X POST http://localhost:5000/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Practicar Docker Compose"}' | python3 -m json.tool

echo "=== Health check ==="
curl -s http://localhost:5000/salud | python3 -m json.tool
```

**Paso 6: Inspeccionar el contenedor.**

```bash
# Estado del health check
docker inspect --format='{{.State.Health.Status}}' api

# Ver las capas de la imagen
docker history api-tareas:1.0

# Entrar al contenedor
docker exec -it api bash
# ls /app
# cat /etc/os-release  <- Ver que SO base usa
# exit
```

**Paso 7: Limpiar.**

```bash
docker rm -f api
docker rmi api-tareas:1.0
```

**Conceptos aplicados:**
- Escritura de Dockerfile completo
- Optimizacion de capas (COPY requirements primero)
- Variables de entorno con ENV y -e
- HEALTHCHECK
- .dockerignore
- Build y ejecucion de imagen personalizada

---

### Ejercicio 3: Aplicacion multi-contenedor con Docker Compose

**Objetivo**: Crear una aplicacion con 3 servicios (API + PostgreSQL + Adminer)
usando Docker Compose, con persistencia de datos y red interna.

**Paso 1: Crear la estructura.**

```bash
mkdir -p ~/docker-ejercicio3/api
cd ~/docker-ejercicio3
```

**Paso 2: Crear la API.**

Archivo `api/requirements.txt`:

```
flask==3.1.1
psycopg2-binary==2.9.10
```

Archivo `api/app.py`:

```python
from flask import Flask, jsonify, request
import psycopg2
import os
import time

app = Flask(__name__)

def get_db():
    """Obtener conexion a PostgreSQL."""
    return psycopg2.connect(os.environ["DATABASE_URL"])


def init_db():
    """Crear tabla si no existe."""
    max_retries = 10
    for intento in range(max_retries):
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    carrera VARCHAR(100) NOT NULL,
                    semestre INTEGER DEFAULT 1,
                    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Insertar datos de ejemplo si la tabla esta vacia
            cur.execute("SELECT COUNT(*) FROM estudiantes")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                    INSERT INTO estudiantes (nombre, carrera, semestre) VALUES
                    ('Ana Garcia', 'Ing. Sistemas', 6),
                    ('Carlos Lopez', 'Ing. Software', 4),
                    ('Maria Torres', 'Ciencias de la Computacion', 8)
                """)
            conn.commit()
            cur.close()
            conn.close()
            print("Base de datos inicializada correctamente")
            return
        except psycopg2.OperationalError:
            print(f"Esperando base de datos... intento {intento+1}/{max_retries}")
            time.sleep(2)

    raise Exception("No se pudo conectar a la base de datos")


@app.route("/")
def home():
    return jsonify({
        "servicio": "API de Estudiantes",
        "endpoints": {
            "GET /estudiantes": "Listar todos",
            "GET /estudiantes/<id>": "Obtener uno",
            "POST /estudiantes": "Crear nuevo",
            "DELETE /estudiantes/<id>": "Eliminar"
        }
    })


@app.route("/estudiantes", methods=["GET"])
def listar():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, carrera, semestre, creado_en FROM estudiantes ORDER BY id")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({
        "total": len(filas),
        "estudiantes": [
            {
                "id": f[0],
                "nombre": f[1],
                "carrera": f[2],
                "semestre": f[3],
                "creado_en": f[4].isoformat() if f[4] else None
            }
            for f in filas
        ]
    })


@app.route("/estudiantes/<int:est_id>", methods=["GET"])
def obtener(est_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, carrera, semestre FROM estudiantes WHERE id = %s", (est_id,))
    fila = cur.fetchone()
    cur.close()
    conn.close()
    if not fila:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"id": fila[0], "nombre": fila[1], "carrera": fila[2], "semestre": fila[3]})


@app.route("/estudiantes", methods=["POST"])
def crear():
    datos = request.get_json()
    if not datos or "nombre" not in datos or "carrera" not in datos:
        return jsonify({"error": "Se requiere 'nombre' y 'carrera'"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO estudiantes (nombre, carrera, semestre) VALUES (%s, %s, %s) RETURNING id",
        (datos["nombre"], datos["carrera"], datos.get("semestre", 1))
    )
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": nuevo_id, "mensaje": "Estudiante creado"}), 201


@app.route("/estudiantes/<int:est_id>", methods=["DELETE"])
def eliminar(est_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM estudiantes WHERE id = %s RETURNING id", (est_id,))
    eliminado = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not eliminado:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify({"mensaje": f"Estudiante {est_id} eliminado"})


@app.route("/salud")
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"estado": "ok", "db": "conectada"})
    except Exception as e:
        return jsonify({"estado": "error", "db": str(e)}), 503


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
```

Archivo `api/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PORT=8000
EXPOSE 8000

CMD ["python", "app.py"]
```

**Paso 3: Crear docker-compose.yml.**

Archivo `docker-compose.yml`:

```yaml
services:
  # --- Base de datos ---
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secreto123
      POSTGRES_DB: universidad
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d universidad"]
      interval: 5s
      timeout: 3s
      retries: 10

  # --- API Backend ---
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:secreto123@db:5432/universidad
      PORT: "8000"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  # --- Adminer (interfaz web para la BD) ---
  adminer:
    image: adminer:latest
    ports:
      - "8080:8080"
    depends_on:
      - db
    environment:
      ADMINER_DEFAULT_SERVER: db

volumes:
  pgdata:
```

**Paso 4: Levantar todo.**

```bash
cd ~/docker-ejercicio3

# Construir y levantar
docker compose up -d --build

# Ver estado
docker compose ps
# NAME          SERVICE   STATUS    PORTS
# ...-db-1      db        running   0.0.0.0:5432->5432/tcp
# ...-api-1     api       running   0.0.0.0:8000->8000/tcp
# ...-adminer-1 adminer   running   0.0.0.0:8080->8080/tcp

# Ver logs
docker compose logs -f api
```

**Paso 5: Probar la aplicacion.**

```bash
# Info
curl -s http://localhost:8000 | python3 -m json.tool

# Listar estudiantes (tiene 3 de ejemplo)
curl -s http://localhost:8000/estudiantes | python3 -m json.tool

# Crear nuevo estudiante
curl -s -X POST http://localhost:8000/estudiantes \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Luis Ramirez", "carrera": "Ing. en Redes", "semestre": 5}' \
  | python3 -m json.tool

# Verificar que se guardo
curl -s http://localhost:8000/estudiantes | python3 -m json.tool

# Health check
curl -s http://localhost:8000/salud | python3 -m json.tool
```

Tambien se puede acceder a **Adminer** (interfaz web de la BD) en `http://localhost:8080`:
- Sistema: PostgreSQL
- Servidor: db
- Usuario: admin
- Contrasena: secreto123
- Base de datos: universidad

**Paso 6: Verificar persistencia.**

```bash
# Detener TODO
docker compose down

# Levantar de nuevo (los datos deben persistir por el volumen pgdata)
docker compose up -d

# Verificar que los datos siguen ahi
curl -s http://localhost:8000/estudiantes | python3 -m json.tool
# Debe mostrar los 4 estudiantes (3 originales + Luis)
```

**Paso 7: Limpiar.**

```bash
# Detener y eliminar contenedores + redes (mantiene datos)
docker compose down

# Detener y eliminar TODO incluyendo datos
docker compose down -v
```

**Conceptos aplicados:**
- Docker Compose con 3 servicios
- Healthchecks y depends_on con condicion
- Red interna automatica (DNS por nombre de servicio)
- Volumen nombrado para persistencia de datos
- Build desde Dockerfile dentro de Compose
- Variables de entorno para configuracion

---

### Ejercicio 4: Limitar recursos y monitorear contenedores

**Objetivo**: Demostrar como Docker usa cgroups para limitar CPU y memoria,
y monitorear el uso de recursos.

**Paso 1: Ejecutar contenedor con limites.**

```bash
# Contenedor con limite de 128MB RAM y 0.5 CPUs
docker run -d \
  --name limitado \
  --memory=128m \
  --cpus=0.5 \
  nginx:alpine
```

**Paso 2: Monitorear recursos.**

```bash
# Ver uso de recursos en tiempo real
docker stats limitado --no-stream

# Salida esperada:
# NAME       CPU %   MEM USAGE / LIMIT   MEM %   NET I/O     BLOCK I/O
# limitado   0.00%   5.5MiB / 128MiB     4.30%   946B / 0B   0B / 8.19kB
```

**Paso 3: Probar el limite de memoria.**

```bash
# Ejecutar un contenedor que intenta usar mas memoria de la permitida
docker run --rm \
  --memory=50m \
  --name stress-test \
  python:3.12-slim \
  python3 -c "
# Intentar asignar 100MB cuando el limite es 50MB
data = []
try:
    for i in range(100):
        data.append(b'x' * 1024 * 1024)  # 1MB por iteracion
        print(f'Asignados: {i+1} MB')
except MemoryError:
    print(f'MemoryError: el contenedor fue limitado a 50MB')
"
# Docker matara el proceso con OOM Killer cuando exceda los 50MB
```

**Paso 4: Inspeccionar los limites configurados.**

```bash
# Ver configuracion de cgroups
docker inspect limitado --format '
  Memoria limite: {{.HostConfig.Memory}} bytes
  CPUs: {{.HostConfig.NanoCpus}} nanoCPUs
'

# Limpiar
docker rm -f limitado
```

**Conceptos aplicados:**
- cgroups para limitar CPU y memoria
- docker stats para monitoreo
- OOM Killer cuando se excede el limite
- docker inspect para verificar configuracion

---

### Ejercicio 5: Imagen multi-stage para aplicacion Go

**Objetivo**: Demostrar la optimizacion de imagenes con multi-stage build.
Compilar una aplicacion en una imagen grande y copiar solo el binario
a una imagen minima.

**Paso 1: Crear el proyecto.**

```bash
mkdir -p ~/docker-ejercicio5
cd ~/docker-ejercicio5
```

**Paso 2: Crear la aplicacion Go.**

Archivo `main.go`:

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "runtime"
    "time"
)

type InfoResponse struct {
    Mensaje     string `json:"mensaje"`
    Hostname    string `json:"hostname"`
    GoVersion   string `json:"go_version"`
    SO          string `json:"so"`
    Arquitectura string `json:"arquitectura"`
    HoraServidor string `json:"hora_servidor"`
    NumCPUs     int    `json:"num_cpus"`
}

func infoHandler(w http.ResponseWriter, r *http.Request) {
    hostname, _ := os.Hostname()
    resp := InfoResponse{
        Mensaje:      "Hola desde un binario Go en Docker!",
        Hostname:     hostname,
        GoVersion:    runtime.Version(),
        SO:           runtime.GOOS,
        Arquitectura: runtime.GOARCH,
        HoraServidor: time.Now().Format(time.RFC3339),
        NumCPUs:      runtime.NumCPU(),
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "3000"
    }

    http.HandleFunc("/", infoHandler)

    fmt.Printf("Servidor escuchando en :%s\n", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}
```

Archivo `go.mod`:

```
module docker-ejercicio5

go 1.22
```

**Paso 3: Crear Dockerfile con multi-stage.**

```dockerfile
# ============================================
# ETAPA 1: Compilacion (imagen ~800MB)
# ============================================
FROM golang:1.22-alpine AS builder

WORKDIR /build
COPY go.mod .
COPY main.go .

# Compilar binario estatico (sin dependencias externas)
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o server .

# ============================================
# ETAPA 2: Produccion (imagen ~7MB)
# ============================================
FROM scratch

# Copiar SOLO el binario compilado
COPY --from=builder /build/server /server

EXPOSE 3000

ENTRYPOINT ["/server"]
```

**Paso 4: Construir y comparar tamanos.**

```bash
# Construir
docker build -t go-app:multi-stage .

# Ver tamano de la imagen
docker images | grep go-app
# go-app   multi-stage   abc123   7.2MB   <- Solo 7MB!

# Comparar: si usaramos golang como imagen final
docker pull golang:1.22-alpine
docker images | grep golang
# golang   1.22-alpine   def456   261MB   <- 261MB con todo el toolchain

# La imagen multi-stage es ~36x mas pequena
```

**Paso 5: Ejecutar y probar.**

```bash
docker run -d -p 3000:3000 --name go-api go-app:multi-stage
curl -s http://localhost:3000 | python3 -m json.tool

# Limpiar
docker rm -f go-api
```

**Conceptos aplicados:**
- Multi-stage build: separar compilacion de ejecucion
- Imagen `scratch` (la imagen mas pequena posible: 0 bytes)
- Compilacion de binario estatico
- Reduccion de superficie de ataque (menos software = menos vulnerabilidades)

---

## 10. Ejercicios Propuestos

### Ejercicio Propuesto 1: Blog con WordPress

**Dificultad**: Basica

Crear un `docker-compose.yml` que levante:
- **WordPress** en el puerto 8080
- **MySQL 8** como base de datos
- Un **volumen** para persistir los datos de MySQL
- Un **volumen** para persistir los uploads de WordPress

Requisitos:
- WordPress debe esperar a que MySQL este listo antes de iniciar.
- Los datos deben sobrevivir a un `docker compose down` y `docker compose up`.

**Pistas:**
- Imagen de WordPress: `wordpress:latest`
- Imagen de MySQL: `mysql:8`
- Variables de entorno de WordPress: `WORDPRESS_DB_HOST`, `WORDPRESS_DB_USER`,
  `WORDPRESS_DB_PASSWORD`, `WORDPRESS_DB_NAME`
- Variables de MySQL: `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`

---

### Ejercicio Propuesto 2: Balanceo de carga

**Dificultad**: Intermedia

Crear una arquitectura con:
- **3 instancias** de un servidor web (puede ser la API de Flask del ejercicio 2)
- **1 Nginx** como balanceador de carga que distribuya el trafico entre las 3 instancias
- Verificar que cada request va a un contenedor diferente (ver el hostname en la respuesta)

**Pistas:**
- Usar `docker compose up -d --scale api=3`
- Crear un `nginx.conf` personalizado con un bloque `upstream` apuntando a las 3 instancias
- Docker Compose crea DNS round-robin automaticamente cuando se escala un servicio

---

### Ejercicio Propuesto 3: Pipeline CI/CD simulado

**Dificultad**: Intermedia

Crear un script bash que simule un pipeline CI/CD:
1. **Build**: Construir la imagen de la aplicacion
2. **Test**: Ejecutar un contenedor que corra las pruebas automatizadas
3. **Tag**: Etiquetar la imagen con el hash del commit de git
4. **Deploy**: Levantar la nueva version con docker compose

```bash
#!/bin/bash
# pipeline.sh

echo "=== BUILD ==="
docker build -t mi-app:$(git rev-parse --short HEAD) .

echo "=== TEST ==="
docker run --rm mi-app:$(git rev-parse --short HEAD) python -m pytest

echo "=== TAG ==="
docker tag mi-app:$(git rev-parse --short HEAD) mi-app:latest

echo "=== DEPLOY ==="
docker compose up -d --build
```

---

### Ejercicio Propuesto 4: Monitoreo con Prometheus y Grafana

**Dificultad**: Avanzada

Crear un `docker-compose.yml` con:
- Tu aplicacion (cualquiera de los ejercicios anteriores)
- **Prometheus** para recolectar metricas
- **Grafana** para visualizar las metricas en dashboards
- **cAdvisor** para obtener metricas de los contenedores

**Pistas:**
- Prometheus: `prom/prometheus:latest` - puerto 9090
- Grafana: `grafana/grafana:latest` - puerto 3000
- cAdvisor: `gcr.io/cadvisor/cadvisor:latest` - puerto 8081
- Prometheus necesita un `prometheus.yml` con los targets a monitorear

---

### Ejercicio Propuesto 5: Red multi-host simulada

**Dificultad**: Avanzada

Crear 3 redes Docker separadas que simulen una arquitectura de 3 capas:

```
Red "frontend"  (172.20.0.0/16)
    |
    +--- nginx (proxy reverso)
    |
Red "backend"  (172.21.0.0/16)
    |
    +--- api (Flask/Node)
    |
Red "database"  (172.22.0.0/16)
    |
    +--- postgres
```

Reglas:
- Nginx SOLO puede hablar con la API (no con la base de datos)
- La API puede hablar con Nginx y con PostgreSQL
- PostgreSQL SOLO puede hablar con la API (no con Nginx)

**Pistas:**
- Crear 3 redes con `docker network create`
- Nginx se conecta a "frontend" y "backend"
- API se conecta a "backend" y "database"
- PostgreSQL solo se conecta a "database"
- Verificar aislamiento con `docker exec nginx ping postgres` (debe fallar)

---

## Referencia Rapida de Comandos

```
IMAGENES
  docker pull <imagen>:<tag>        Descargar imagen
  docker images                     Listar imagenes
  docker build -t <nombre> .        Construir imagen
  docker rmi <imagen>               Eliminar imagen
  docker image prune                Limpiar imagenes sin usar

CONTENEDORES
  docker run -d -p H:C --name N I  Ejecutar contenedor
  docker ps                         Listar activos
  docker ps -a                      Listar todos
  docker logs <nombre>              Ver logs
  docker exec -it <nombre> bash     Entrar al contenedor
  docker stop <nombre>              Detener
  docker start <nombre>             Iniciar
  docker rm <nombre>                Eliminar
  docker stats                      Monitor de recursos

VOLUMENES
  docker volume create <nombre>     Crear volumen
  docker volume ls                  Listar volumenes
  docker volume rm <nombre>         Eliminar volumen
  docker volume prune               Limpiar sin usar

REDES
  docker network create <nombre>    Crear red
  docker network ls                 Listar redes
  docker network inspect <nombre>   Ver detalles
  docker network rm <nombre>        Eliminar red

COMPOSE
  docker compose up -d              Levantar servicios
  docker compose down               Detener servicios
  docker compose down -v            Detener + eliminar datos
  docker compose ps                 Estado de servicios
  docker compose logs -f            Seguir logs
  docker compose build              Reconstruir imagenes
  docker compose exec <svc> bash    Shell en un servicio

LIMPIEZA GENERAL
  docker system prune               Limpiar todo lo sin usar
  docker system prune -a            Limpiar TODO (incluye imagenes)
  docker system df                  Ver uso de disco
```
