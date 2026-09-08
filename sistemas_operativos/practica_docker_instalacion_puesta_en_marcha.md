# Práctica: instalación de Docker y puesta en marcha (paso a paso)

Práctica complementaria a la Unidad 1 de este curso. Docker es el ejemplo más accesible y actual de **virtualización a nivel de sistema operativo**: en vez de emular una computadora completa (como una máquina virtual), aísla procesos dentro del mismo kernel usando dos mecanismos que se relacionan directo con los conceptos ya vistos:

- **Namespaces** — aíslan lo que un proceso puede ver (su propio espacio de PIDs, red, sistema de archivos).
- **cgroups** — limitan cuánto CPU/memoria puede usar ese proceso.

Es decir: un contenedor **no es una computadora nueva, es un proceso con una vista de mundo restringida**. Esta práctica instala Docker de cero y lo lleva hasta correr tu propia aplicación en un contenedor, verificando en cada paso esa conexión con los conceptos de sistemas operativos.

> Para dominar Docker en profundidad (Dockerfile avanzado, volúmenes, redes, Docker Compose, ejercicios adicionales) usa [`tutorial_docker/README.md`](../tutorial_docker/README.md) como siguiente paso — esta práctica se queda solo en "instalación → primera puesta en marcha".

## Requisitos

- Linux (Ubuntu/Debian), Windows con WSL2, o macOS.
- Conexión a internet (Docker descarga imágenes de Docker Hub).
- Permisos de administrador para instalar software.

---

## Paso 1 — Instalar Docker

### Linux (Ubuntu/Debian)

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

`usermod -aG docker $USER` agrega tu usuario al grupo `docker` para no tener que escribir `sudo` antes de cada comando. **Cierra sesión y vuelve a entrar** (o reinicia la terminal) para que el cambio de grupo tome efecto.

### Windows / macOS

Instalar [Docker Desktop](https://docs.docker.com/get-docker/) — incluye Docker Engine, Docker Compose y una interfaz gráfica. En Windows requiere WSL2 habilitado (Docker Desktop lo configura automáticamente si no lo tienes).

### Verificar instalación

```bash
docker --version
docker compose version
```

**Checkpoint:** debe imprimir un número de versión sin errores. Si da `permission denied` en Linux, es porque el cambio de grupo del paso anterior no se aplicó todavía — cierra y reabre la terminal.

---

## Paso 2 — Primera puesta en marcha: `hello-world`

```bash
docker run hello-world
```

Salida esperada (resumida):

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image...
 4. The Docker daemon streamed that output to the Docker client...
```

Eso mismo describe la arquitectura cliente-servidor de Docker: el comando `docker` es un cliente que le habla al **daemon** (`dockerd`), que es quien realmente crea y administra los contenedores.

---

## Paso 3 — Levantar un servicio real con puerto expuesto

```bash
docker run -d --name servidor-web -p 8088:80 nginx
```

- `-d` — corre en segundo plano (*detached*), como correría un servicio real.
- `--name servidor-web` — nombre para referirte a él después, en vez de su ID.
- `-p 8088:80` — mapea el puerto 80 del contenedor (donde nginx escucha) al puerto 8088 de tu máquina.

Verifica que responde:

```bash
curl http://localhost:8088
# o abre http://localhost:8088 en el navegador
```

**Checkpoint:** debe devolver el HTML de bienvenida de nginx.

---

## Paso 4 — Ver el contenedor desde el ángulo de sistemas operativos

```bash
docker ps                       # contenedores corriendo — como listar servicios activos
docker top servidor-web           # procesos REALES dentro del contenedor
docker stats --no-stream servidor-web    # CPU/memoria en vivo — igual que top/htop
```

`docker top` muestra procesos con PIDs del **host** — la prueba de que el contenedor no es una máquina aparte, sino procesos normales del kernel de tu sistema, solo que con una vista aislada (namespace) de red y sistema de archivos.

```bash
docker exec -it servidor-web sh       # entra a una shell DENTRO del contenedor
ps aux                                  # aquí sí ves solo LOS PROCESOS de este namespace
exit
```

**Checkpoint:** el PID que ve `ps aux` dentro del contenedor es distinto al PID que ves con `docker top` desde fuera — es el mismo proceso, pero cada vista usa su propio namespace de PIDs.

---

## Paso 5 — Construir tu propia imagen (Dockerfile)

Crea un mini-servidor en Python:

```bash
mkdir mi-app-docker && cd mi-app-docker
cat > app.py << 'EOF'
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hola desde mi contenedor\n")

HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
EOF
```

Crea el `Dockerfile` (la receta para construir la imagen):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]
```

| Instrucción | Qué hace |
|---|---|
| `FROM` | Imagen base — aquí, Python 3.12 ya instalado sobre una distribución mínima (`slim`). |
| `WORKDIR` | Directorio de trabajo dentro de la imagen. |
| `COPY` | Copia archivos de tu máquina a la imagen. |
| `EXPOSE` | Documenta qué puerto usa la aplicación (informativo — el mapeo real lo hace `-p` al correr). |
| `CMD` | Comando que se ejecuta cuando arranca un contenedor de esta imagen. |

Construir la imagen:

```bash
docker build -t mi-app-demo .
```

`-t mi-app-demo` le da un nombre (tag) a la imagen resultante; `.` le dice a Docker que use el `Dockerfile` del directorio actual.

---

## Paso 6 — Correr tu propia imagen

```bash
docker run -d --name mi-app --rm -p 8089:8000 mi-app-demo
curl http://localhost:8089
```

`--rm` hace que el contenedor se elimine automáticamente al detenerse — útil para pruebas rápidas que no necesitas conservar.

**Checkpoint:** debe responder `Hola desde mi contenedor`.

---

## Paso 7 — Limpieza

```bash
docker stop servidor-web mi-app
docker rm servidor-web            # mi-app ya se autoeliminó por --rm
docker rmi mi-app-demo             # elimina la imagen construida (opcional)
docker ps -a                         # confirma que no quedan contenedores activos
```

---

## Resumen — qué acabas de hacer, en términos de sistemas operativos

| Comando Docker | Concepto de SO detrás |
|---|---|
| `docker run` | Crea un **proceso** aislado con namespaces + cgroups, a partir de una imagen — no una máquina nueva. |
| `-p 8088:80` | Redirección de puerto — el contenedor "vive" con su propia interfaz de red aislada (namespace de red). |
| `docker top` | Los PIDs que ves son procesos reales del kernel del **host**. |
| `docker exec ... ps aux` | Vista distinta de los mismos procesos, dentro del namespace de PIDs del contenedor. |
| `docker stats` | cgroups en acción: límites y consumo real de CPU/memoria por proceso. |
| `docker build` | Empaqueta un sistema de archivos en capas (imagen) — no instala un SO nuevo, reutiliza el kernel del host. |

## Actividades de aprendizaje

- Repite el Paso 4 pero corriendo dos contenedores a la vez (`nginx` y `mi-app-demo`) — compara sus namespaces de red con `docker inspect <nombre> | grep IPAddress`.
- Investiga qué pasa si corres `docker run -d nginx` **sin** `-p` — ¿el servicio funciona? ¿Puedes acceder desde tu navegador? Explica por qué en términos de namespaces de red.
- Modifica el `Dockerfile` del Paso 5 para limitar recursos al correr el contenedor: `docker run --memory=128m --cpus=0.5 ...` — verifica el límite con `docker stats`.
- Compara (en una tabla) la virtualización por contenedores (esta práctica) contra la virtualización por hipervisor (VirtualBox/VMware) en cuanto a: qué se comparte con el host, overhead, y tiempo de arranque.

## Siguientes pasos

Esta práctica cubre justo "instalación → primera puesta en marcha". Dos caminos para seguir:

- [`practica_floci_servicios_cloud_locales.md`](practica_floci_servicios_cloud_locales.md) — usar esta misma instalación de Docker para levantar un emulador de servicios cloud (S3, DynamoDB) y practicar administración de "servidor" sin cuenta real.
- [`tutorial_docker/README.md`](../tutorial_docker/README.md) — para Dockerfile avanzado, volúmenes y persistencia de datos, redes entre contenedores, Docker Compose y ejercicios adicionales resueltos.
