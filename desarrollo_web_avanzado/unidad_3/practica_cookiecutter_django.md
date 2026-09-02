# Práctica: instalación y creación de un proyecto con Cookiecutter Django

Repo de referencia: https://github.com/cookiecutter/cookiecutter-django

Cubre 3.1–3.4 del temario (Concepto de framework, Ejemplos, Instalación, Estructura de directorios): en vez de arrancar un proyecto Django desde cero con `django-admin startproject`, se genera con una plantilla que ya trae configurado Docker, variables de entorno por ambiente, Celery, tests, CI y buenas prácticas de producción — exactamente el tipo de "framework de arranque" que un equipo real usaría.

## Requisitos previos

- Python 3.11+ instalado.
- [Docker](https://docs.docker.com/get-docker/) y Docker Compose — el flujo recomendado de esta plantilla corre todo en contenedores (Django, Postgres, Redis, etc.), sin instalar nada de eso en tu máquina.
- Git.
- Recomendado: [`uv`](https://docs.astral.sh/uv/) para instalar herramientas Python de forma aislada (`uv tool install`) en vez de `pip install --user`.

## Paso 1 — Instalar Cookiecutter

Cookiecutter es la herramienta genérica de plantillas; `cookiecutter-django` es una plantilla que corre sobre ella.

```bash
uv tool install "cookiecutter>=1.7.0"
```

Alternativa sin `uv`:

```bash
pip install --user "cookiecutter>=1.7.0"
```

Verificar instalación:

```bash
cookiecutter --version
```

## Paso 2 — Generar el proyecto

```bash
uvx cookiecutter https://github.com/cookiecutter/cookiecutter-django
```

Alternativa sin `uv` (con Cookiecutter ya instalado):

```bash
cookiecutter https://github.com/cookiecutter/cookiecutter-django
```

Esto descarga la plantilla y hace una serie de preguntas interactivas en terminal. Las más importantes:

| Prompt | Qué responder en esta práctica | Por qué importa |
|---|---|---|
| `project_name` | `Practica Cookiecutter` (o el nombre que quieras) | Nombre legible del proyecto |
| `project_slug` | se autogenera del nombre | Nombre del paquete Python / carpeta |
| `author_name`, `email`, `domain_name` | tus datos | Van en `LICENSE`, metadatos |
| `open_source_license` | `MIT` (o `Not open source`) | Licencia del repo generado |
| `username_type` | `username` | Login por username vs email |
| `timezone` | `America/Mexico_City` | Zona horaria de Django (`TIME_ZONE`) |
| `windows` / `use_docker` | `y` para `use_docker` | Habilita `docker-compose.local.yml` y `docker-compose.production.yml` |
| `postgresql_version` | la más reciente ofrecida | Versión de la imagen de Postgres |
| `cloud_provider` | `None` | Sin esto, evita configurar credenciales de AWS/GCP que no usaremos |
| `mail_service` | `Mailgun` (o cualquiera, no se usará) | Solo configura variables, no envía correos sin credenciales reales |
| `frontend_pipeline` | `None` | Evita instalar Gulp/Webpack para esta práctica |
| `rest_framework` | `Django REST Framework` (o `None` si no lo necesitas aún) | Agrega DRF ya configurado |
| `use_celery` | `n` para esta práctica | Evita levantar workers extra sin necesidad |
| `use_sentry`, `use_whitenoise`, ... | valores por defecto | No afectan el arranque local |

## Paso 3 — Recorrer la estructura generada (3.4)

```bash
cd practica_cookiecutter   # el project_slug que hayas elegido
ls -la
```

Estructura típica (resumida):

```
practica_cookiecutter/
├── config/
│   ├── settings/
│   │   ├── base.py       # settings compartidos
│   │   ├── local.py       # settings de desarrollo
│   │   ├── production.py   # settings de producción
│   │   └── test.py          # settings para tests
│   ├── urls.py                # urlconf raíz
│   └── wsgi.py / asgi.py        # entrypoints del servidor
├── practica_cookiecutter/     # el paquete de la app (project_slug)
│   ├── users/                  # app de usuarios ya incluida (auth completo)
│   ├── static/
│   └── templates/
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── docker-compose.local.yml
├── docker-compose.production.yml
├── manage.py
└── README.md
```

**Observación clave (conecta con 1.5 estructura por capas y 3.4):** los `settings` ya vienen **separados por entorno** (`base` → `local`/`production`/`test` heredan de él) — la misma buena práctica que vimos en Unidad 1 (nunca un solo `settings.py` con credenciales hardcodeadas), aquí ya resuelta por la plantilla.

## Paso 4 — Levantar el proyecto con Docker

```bash
docker compose -f docker-compose.local.yml build
docker compose -f docker-compose.local.yml up
```

En otra terminal, con el stack corriendo:

```bash
# Migraciones
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

# Crear superusuario
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

> **Importante:** para correr comandos de `manage.py` dentro del contenedor se usa `docker compose run --rm django ...`, **no** `docker exec` — la documentación oficial es explícita en esto, porque `run` crea un contenedor efímero con el entorno correcto y lo destruye al terminar (`--rm`).

Verificar que el sitio responde: abrir `http://localhost:8000` — debe verse la página de bienvenida del proyecto, y `http://localhost:8000/admin/` debe pedir login (usar el superusuario creado).

## Paso 5 — Correr los tests incluidos

La plantilla trae tests de ejemplo (para la app `users`) ya configurados con pytest:

```bash
docker compose -f docker-compose.local.yml run --rm django pytest
```

## Paso 6 — Apagar el stack

```bash
docker compose -f docker-compose.local.yml down
```

## Actividades de aprendizaje

- Generar el proyecto y documentar (captura o notas) las respuestas que diste a cada prompt y por qué.
- Ubicar en la estructura generada dónde vive cada pieza del patrón MVT visto en Unidad 1: modelos (`users/models.py`), vistas (`users/views.py`), templates (`templates/`), urls (`config/urls.py`).
- Explicar, con tus palabras, para qué sirve tener `local.py` / `production.py` / `test.py` separados en vez de un solo `settings.py`.
- Crear una app nueva dentro del proyecto generado (`python manage.py startapp catalogo`) y ubicarla correctamente según la convención de carpetas de la plantilla.
- Correr `pytest` y explicar qué prueba trae por defecto la app `users`.

## Evaluación sugerida

| Evidencia | Qué valora |
|---|---|
| Proyecto generado y corriendo (`docker compose up` sin errores) | Instalación correcta de Cookiecutter y generación exitosa |
| Captura de `/admin/` con sesión iniciada | Migraciones y superusuario aplicados correctamente |
| Documento de estructura de directorios | Identificación correcta de dónde vive cada capa (modelo/vista/template/settings) |
| Salida de `pytest` sin fallos | Verificación de que el entorno quedó correctamente configurado |

## Fuentes

- https://github.com/cookiecutter/cookiecutter-django
- https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html
