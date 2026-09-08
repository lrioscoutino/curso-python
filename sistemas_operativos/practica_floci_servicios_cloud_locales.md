# Práctica: Floci — administrar servicios "cloud" locales con Docker

Continuación de [`practica_docker_instalacion_puesta_en_marcha.md`](practica_docker_instalacion_puesta_en_marcha.md). Ahí instalaste Docker y corriste tu primer contenedor; aquí usas esa base para practicar administración de **servicios de servidor** (almacenamiento, bases de datos, cómputo) exactamente como lo harías contra un proveedor de nube real — sin cuenta, sin costo, sin salir de tu máquina.

## Por qué esta práctica y no un VPS real

Un VPS real (DigitalOcean, AWS, etc.) cuesta dinero y requiere una cuenta — mal punto de partida para practicar en cada sesión. **Floci** (https://github.com/floci-io) resuelve esto: un contenedor Docker que emula localmente la API de AWS (S3, DynamoDB, SQS, Lambda, y más de 100 servicios) sin necesitar cuenta ni pagar. No sustituye a un servidor real, pero la administración de recursos es idéntica a la que harías contra la nube de verdad.

> Verificado al escribir esta práctica: el contenedor expone `AWS Local Emulator 2.0.1` (compatible con la API de LocalStack — el mismo endpoint de salud `/_localstack/health` responde) escuchando en el puerto 4566.

## Paso 1 — Requisito previo: Docker instalado

```bash
docker --version
```

Si no está instalado, ver [`practica_docker_instalacion_puesta_en_marcha.md`](practica_docker_instalacion_puesta_en_marcha.md) primero.

## Paso 2 — Levantar Floci

```bash
docker run -d --name floci \
  -p 4566:4566 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -u root \
  floci/floci:latest
```

Verificar que arrancó correctamente:

```bash
docker logs floci
# Debe terminar con: "=== AWS Local Emulator Ready ===" y "Listening on: http://0.0.0.0:4566"

curl http://localhost:4566/_localstack/health
# Debe responder JSON con servicios en estado "running" (s3, dynamodb, sqs, lambda, ...)
```

## Paso 3 — Instalar y configurar el AWS CLI para hablar con el emulador

```bash
pip install --user awscli   # o: sudo apt install awscli

export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
```

Estas credenciales son falsas a propósito — Floci no valida contra AWS real, solo necesita que el CLI mande *algo* en esos campos.

## Paso 4 — Administrar servicios "cloud" reales, corriendo local

```bash
# Crear un bucket S3 (almacenamiento) sin cuenta real de AWS
aws s3 mb s3://mi-bucket
aws s3 ls

# Crear una tabla DynamoDB (base de datos NoSQL)
aws dynamodb create-table \
  --table-name demo-table \
  --attribute-definitions AttributeName=pk,AttributeType=S \
  --key-schema AttributeName=pk,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

aws dynamodb list-tables
```

**Checkpoint:** `aws s3 ls` debe listar `mi-bucket`, y `aws dynamodb list-tables` debe listar `demo-table` — administración real de infraestructura, sin haber tocado una cuenta de AWS.

## Paso 5 — Monitorizar el "servidor" (conexión con Unidad 1 y 2)

```bash
docker top floci        # procesos reales dentro del contenedor — es un proceso más del host
docker stats --no-stream floci    # CPU/memoria en vivo, igual que top/htop en un VPS real
```

`docker top` demuestra otra vez lo mismo que en la práctica de Docker básico: Floci **no es una máquina nueva**, es un proceso aislado (namespaces + cgroups) del mismo kernel que ya tienes.

## Paso 6 — Cierre de la práctica

```bash
docker stop floci
docker rm floci
```

## Conexión con la teoría de la materia

- `docker run` crea un **proceso aislado** a partir de una imagen — refuerza 1.6 (Núcleo: modo usuario vs kernel) y anticipa la Unidad 2 (procesos, planificación).
- El puerto expuesto (4566) hace que Floci "viva" como si fuera remoto, aunque corre en la misma máquina — el mismo concepto de servidor administrado a distancia.
- `docker stats` es una probada práctica de lo que la Unidad 3 (administración de memoria) y Unidad 4 (administración de E/S) formalizarán con más rigor.

## Actividades de aprendizaje

- Crea un segundo bucket S3 y sube un archivo de prueba con `aws s3 cp archivo.txt s3://mi-bucket/`. Descárgalo de vuelta con `aws s3 cp s3://mi-bucket/archivo.txt archivo-copia.txt` y verifica que el contenido coincide.
- Elimina la tabla DynamoDB con `aws dynamodb delete-table --table-name demo-table` y confirma con `list-tables` que ya no aparece.
- Compara (en un párrafo) qué tan realista es esta práctica frente a administrar un VPS real de verdad: ¿qué SÍ estás practicando (comandos, administración de recursos) y qué NO (acceso SSH real, latencia de red real, facturación real)?

> **Nota:** Floci reemplaza la *cuenta y el costo* de un proveedor cloud real, no la máquina — sigues practicando administración de recursos (buckets, tablas, cómputo) tal como lo harías contra un servidor de verdad.
