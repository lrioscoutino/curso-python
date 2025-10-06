
# Práctica: Dockerizando una Base de Datos con MySQL

Esta práctica está diseñada para desarrolladores junior que deseen aprender a contenedorizar una base de datos MySQL utilizando Docker.

## Parte Teórica: Introducción a Docker y MySQL

### ¿Qué es Docker?

Docker is an open source platform that allows you to automate the deployment, scaling, and management of applications within software containers. A container is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.

### ¿Por qué usar Docker?

*   **Portabilidad:** Las aplicaciones en contenedores se ejecutan de la misma manera en cualquier entorno.
*   **Aislamiento:** Los contenedores aíslan las aplicaciones entre sí y del sistema operativo subyacente.
*   **Eficiencia:** Los contenedores son más ligeros y rápidos que las máquinas virtuales.
*   **Escalabilidad:** Es fácil crear y destruir contenedores para escalar aplicaciones horizontalmente.

### Conceptos Básicos de Docker

*   **Imagen (Image):** Una plantilla de solo lectura con instrucciones para crear un contenedor Docker.
*   **Contenedor (Container):** Una instancia en ejecución de una imagen.
*   **Volumen (Volume):** Un mecanismo para persistir los datos generados y utilizados por los contenedores Docker.

### MySQL con Docker

Correr MySQL en un contenedor de Docker ofrece varias ventajas:

*   **Configuración rápida:** Puedes levantar una instancia de MySQL con una sola línea de comando.
*   **Aislamiento de datos:** Cada contenedor puede tener su propia base de datos y configuración, evitando conflictos.
*   **Portabilidad:** Es fácil mover tu base de datos de un entorno a otro.

La imagen oficial de MySQL en Docker Hub es la forma más común de correr MySQL en Docker.

## Prerrequisitos

*   Tener Docker instalado en tu sistema.
*   Tener un cliente de MySQL instalado (como `mysql-client` en Linux o cualquier cliente GUI como DBeaver o MySQL Workbench).

### Instalación de Docker en Ubuntu

Si no tienes Docker instalado en Ubuntu, puedes seguir estos pasos:

1.  **Actualizar el índice de paquetes:**

    ```bash
    sudo apt-get update
    ```

2.  **Instalar paquetes para permitir que `apt` use un repositorio sobre HTTPS:**

    ```bash
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

3.  **Agregar la clave GPG oficial de Docker:**

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```

4.  **Configurar el repositorio estable:**

    ```bash
    echo \
      "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

5.  **Instalar Docker Engine:**

    ```bash
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

6.  **Verificar que Docker se ha instalado correctamente:**

    ```bash
    sudo docker run hello-world
    ```

## Ejercicios

### Ejercicio 1: Descargar la imagen de MySQL

Descarga la última imagen de MySQL desde Docker Hub.

```bash
docker pull mysql
```

### Ejercicio 2: Listar las imágenes locales

Verifica que la imagen de MySQL se ha descargado correctamente.

```bash
docker images
```

### Ejercicio 3: Correr un contenedor de MySQL (sin persistencia)

Corre un contenedor de MySQL sin un volumen para la persistencia de datos. Esto significa que si eliminas el contenedor, los datos se perderán.

```bash
docker run --name mysql-temporal -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
```

### Ejercicio 4: Listar los contenedores en ejecución

Verifica que el contenedor `mysql-temporal` se está ejecutando.

```bash
docker ps
```

### Ejercicio 5: Conectarse al contenedor

Conéctate al contenedor para ejecutar comandos de MySQL.

```bash
docker exec -it mysql-temporal mysql -p
```
(Ingresa la contraseña `my-secret-pw` cuando se te solicite)

### Ejercicio 6: Crear una base de datos

Dentro del shell de MySQL, crea una nueva base de datos.

```sql
CREATE DATABASE mi_app;
SHOW DATABASES;
EXIT;
```

### Ejercicio 7: Detener y eliminar el contenedor

Detén y elimina el contenedor.

```bash
docker stop mysql-temporal
docker rm mysql-temporal
```

### Ejercicio 8: Correr un contenedor de MySQL (con persistencia)

Ahora, corre un contenedor de MySQL utilizando un volumen para que los datos persistan incluso si el contenedor es eliminado.

```bash
docker run --name mysql-persistente -v mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
```

### Ejercicio 9: Verificar la persistencia

1.  Conéctate al nuevo contenedor y crea una base de datos.
2.  Detén y elimina el contenedor.
3.  Crea un nuevo contenedor con el mismo volumen.
4.  Conéctate al nuevo contenedor y verifica que la base de datos que creaste en el paso 1 todavía existe.

### Ejercicio 10: Exponer el puerto de MySQL

Para conectarte desde un cliente de MySQL en tu máquina anfitriona, necesitas exponer el puerto del contenedor.

```bash
docker run --name mysql-externo -p 3306:3306 -v mysql-data-externo:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
```

## Práctica Final

Crea un archivo `docker-compose.yml` para definir y correr tu contenedor de MySQL. Esto facilita la gestión de la configuración.

Crea un archivo llamado `docker-compose.yml` con el siguiente contenido:

```yaml
version: '3.8'
services:
  db:
    image: mysql
    container_name: mysql-compose
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
    ports:
      - "3306:3306"
    volumes:
      - mysql-compose-data:/var/lib/mysql

volumes:
  mysql-compose-data:
```

Ahora, levanta el servicio con:

```bash
docker-compose up -d
```

## Prueba desde un Cliente de MySQL

Con el contenedor corriendo y el puerto expuesto, puedes conectarte desde tu cliente de MySQL local:

*   **Host:** `127.0.0.1` o `localhost`
*   **Puerto:** `3306`
*   **Usuario:** `root`
*   **Contraseña:** `my-secret-pw`

Una vez conectado, deberías poder ver y gestionar las bases de datos dentro de tu contenedor de Docker.
