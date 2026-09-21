# Proyecto integrador: Sistema de gestión de ACOM (Actividades Complementarias — TecNM)

Práctica de proyecto completo para Desarrollo Web Avanzado: un sistema real, con reglas de negocio reales, que ejercita todo lo visto en las Unidades 1 y 3 (buenas prácticas, patrones de diseño, MVT, instalación/estructura de un framework) sobre un caso de uso reconocible para cualquier estudiante del TecNM.

## El problema real que resuelve

En el Tecnológico Nacional de México, las **ACOM (Actividades Complementarias)** son un requisito obligatorio para titularse: cada estudiante debe acumular **5 créditos complementarios** a lo largo de la carrera, en actividades que **no son materias del plan de estudios** — investigación, cursos/diplomados, publicaciones, cultura/deporte, tutorías, o impacto social.

El proceso de acreditación tiene tres pasos con tres responsables distintos:

```
Estudiante                Responsable de la              Departamento
                          actividad (docente/                Académico
                          entrenador/tutor)
    │                            │                              │
    │  1. Se inscribe             │                              │
    ├────────────────────────────►│                              │
    │                            │  2. Evalúa desempeño          │
    │                            │     y emite constancia        │
    │                            ├─────────────────────────────►│
    │                            │                              │  3. Valida constancia
    │                            │                              │     y registra créditos
    │◄──────────────────────────────────────────────────────────┤     en el expediente
    │        Créditos visibles en su expediente (SITEC/SII)       │
```

Este proyecto modela exactamente ese flujo: **inscripción → evaluación → constancia → validación y registro de créditos**, con un límite de 5 créditos y reglas de quién puede hacer qué en cada paso.

## Categorías de actividad (según el modelo oficial del TecNM)

| Categoría | Ejemplos |
|---|---|
| Investigación y desarrollo tecnológico | Veranos de investigación, proyectos con docentes, InnovatecNM, prototipos, patentes |
| Cursos, talleres y diplomados | Software especializado, lenguajes de programación, certificaciones |
| Publicaciones y ponencias | Artículos científicos, memorias de congreso, ponente |
| Actividades culturales y deportivas | Selecciones del instituto, música, danza, teatro |
| Tutorías y asesorías | Tutor entre pares, apoyo académico institucional |
| Impacto social y ambiente | Protección ambiental, brigadas, actividades comunitarias |

## Estructura del proyecto

```
proyecto_acom/
└── acom/                      # la app Django — se integra a cualquier proyecto existente
    ├── models.py                # ActividadComplementaria, Inscripcion, Constancia, RegistroCreditos
    ├── exceptions.py              # TransicionInvalidaError, LimiteCreditosError
    ├── services.py                 # InscripcionService, CreditosService — Service Layer (Unidad 1)
    ├── signals.py                    # inscripcion_validada — Observer (Unidad 1)
    ├── receivers.py                    # reacciona a la signal (ej. notificar)
    ├── apps.py                          # registra los receivers en ready()
    ├── forms.py                          # EvaluacionForm
    ├── views.py                           # 5 vistas — MVT (Unidad 1)
    ├── urls.py                             # app_name="acom"
    ├── admin.py                             # gestión desde /admin/
    ├── templates/acom/                       # 5 templates mínimos
    ├── test_services.py                       # 4 tests de la lógica de negocio
    └── test_views.py                           # 1 test del flujo HTTP completo
```

Todo el código de esta carpeta fue **verificado ejecutándolo**: `makemigrations`, `migrate`, y los 5 tests (`test_services.py` + `test_views.py`) pasan (`OK`, 5/5) contra una base de datos real en un proyecto Django 5.0 de prueba.

## Modelo de datos

```
ActividadComplementaria
├── nombre, categoria, descripcion
├── responsable (FK User)       ← quién evalúa esta actividad
├── creditos_valor (decimal)
└── activa (bool)

Inscripcion
├── estudiante (FK User), actividad (FK)
├── estado: inscrito → evaluado_aprobado/rechazado → constancia_emitida → validado
├── fecha_inscripcion, fecha_evaluacion, observaciones
└── constraint: un estudiante no puede inscribirse dos veces a la misma actividad

Constancia (1 a 1 con Inscripcion)
├── folio (único, autogenerado: ACOM-000001)
├── fecha_emision, emitida_por (FK User)

RegistroCreditos (1 a 1 con Inscripcion)
├── creditos_otorgados, fecha_registro, validado_por (FK User)
```

## Arquitectura por capas (propuesta de evolución)

El código actual separa modelos, servicios y vistas, pero la autorización, la concurrencia y las reglas de estado siguen mezcladas en `services.py` y `views.py`. Esta sección propone formalizarlo en **cuatro capas** con una regla de dependencia: cada capa solo importa de las de abajo, y el dominio no importa nada de Django. Es una guía de diseño y refactor: el código de esta carpeta todavía **no** está organizado así.

```
┌──────────────────────────────────────────────┐
│ 1. PRESENTACIÓN   views · forms · templates  │  HTTP, validación de entrada
├──────────────────────────────────────────────┤
│ 2. APLICACIÓN     services/ (casos de uso)   │  orquesta, transacciones, permisos
├──────────────────────────────────────────────┤
│ 3. DOMINIO        domain/ (reglas puras)     │  estados, límites, excepciones
├──────────────────────────────────────────────┤
│ 4. INFRAESTRUCTURA models · selectors · signals · receivers │  ORM, correo, SITEC
└──────────────────────────────────────────────┘
```

### Estructura de carpetas propuesta

```
acom/
├── domain/
│   ├── estados.py         # EstadoInscripcion + TRANSICIONES permitidas (dict)
│   ├── reglas.py          # puede_evaluar(), excede_limite(): funciones puras
│   └── exceptions.py      # AcomError (base), TransicionInvalidaError, LimiteCreditosError
├── models.py              # solo campos, constraints y __str__
├── selectors.py           # lecturas: inscripciones_de(), total_validado()
├── services/
│   ├── inscripciones.py   # inscribir, evaluar, emitir_constancia, validar_y_registrar
│   └── permisos.py        # quién puede ejecutar cada caso de uso
├── signals.py / receivers.py
├── views/                 # delgadas: parsean, llaman al servicio, renderizan
├── forms.py
└── tests/
    ├── test_domain.py     # sin base de datos
    ├── test_services.py
    └── test_views.py
```

### Responsabilidad de cada capa

| Capa | Responsabilidad | De dónde sale hoy |
|---|---|---|
| **Dominio** | Máquina de estados como dato y reglas puras | Los `if estado != ...` repetidos en `services.py` |
| **Infraestructura** | Lecturas en `selectors.py`, escrituras por ORM | `CreditosService.total_validado` y consultas en las vistas |
| **Aplicación** | Un caso de uso por función, con `atomic()`, `select_for_update` y comprobación de permisos | `services.py` actual |
| **Presentación** | Traducir HTTP a llamadas y excepciones a mensajes | `views.py`, hoy con `render` duplicado |

### Idea central: las reglas como dato, los casos de uso como orquesta

```python
# domain/estados.py — la regla es un dato, no ifs dispersos
TRANSICIONES = {
    EstadoInscripcion.INSCRITO: {EVALUADO_APROBADO, EVALUADO_RECHAZADO},
    EstadoInscripcion.EVALUADO_APROBADO: {CONSTANCIA_EMITIDA},
    EstadoInscripcion.CONSTANCIA_EMITIDA: {VALIDADO},
}

def validar_transicion(actual, nuevo):
    if nuevo not in TRANSICIONES.get(actual, set()):
        raise TransicionInvalidaError(f"{actual} → {nuevo} no permitido")
```

```python
# services/inscripciones.py — el caso de uso coordina las capas
@transaction.atomic
def validar_y_registrar(inscripcion_id, usuario):
    permisos.exigir(usuario, "acom.can_validate_credits")
    insc = Inscripcion.objects.select_for_update().get(pk=inscripcion_id)
    validar_transicion(insc.estado, EstadoInscripcion.VALIDADO)
    if reglas.excede_limite(selectors.total_validado(insc.estudiante)):
        raise LimiteCreditosError(...)
    ...
    transaction.on_commit(lambda: inscripcion_validada.send(...))
```

### Qué problemas resuelve

- **Autorización:** queda centralizada en `permisos.py` y se llama desde el servicio, no desde cada vista. Hoy cualquier usuario con sesión puede abrir `panel_departamento` y registrar créditos.
- **Concurrencia:** `select_for_update` y `on_commit` viven en un solo lugar. Hoy dos validaciones simultáneas pueden sobrepasar el límite de créditos, y la signal se dispara aunque falle el commit.
- **Pruebas:** las reglas del dominio se prueban sin base de datos (`test_domain.py`).
- **Manejo de errores:** las vistas capturan `AcomError`, clase base de las excepciones propias, y desaparece el bloque de `render` duplicado. Hoy una doble inscripción devuelve un 500.

### Compromisos

Para 4 modelos y 5 vistas es más estructura de la necesaria. Se justifica aquí porque el objetivo es practicar arquitectura. Si quieres menos cambios, solo `domain/estados.py` y `selectors.py` aportan la mayor parte del valor.

### Actividad sugerida

Refactoriza el proyecto a estas cuatro capas por pasos, con las pruebas actuales pasando entre uno y otro:

1. Extrae `domain/estados.py` y sustituye los `if` de `services.py`.
2. Mueve las lecturas a `selectors.py`.
3. Divide `services.py` en `services/inscripciones.py` y `services/permisos.py`, con `select_for_update` y `on_commit`.
4. Adelgaza las vistas para que capturen `AcomError`.
5. Agrega pruebas de autorización, doble inscripción y rechazo.

## Reglas de negocio (en `services.py`, no en las vistas — Service Layer)

- Solo el **responsable de la actividad** (`actividad.responsable`) puede evaluarla — cualquier otro usuario lo intenta y `InscripcionService.evaluar` lanza `TransicionInvalidaError`.
- No se puede emitir constancia sin haber evaluado y aprobado primero.
- No se puede validar/registrar créditos sin constancia emitida.
- Si el estudiante **ya alcanzó los 5.00 créditos**, un nuevo intento de registro lanza `LimiteCreditosError` — el expediente no crece indefinidamente.
- Al validar y registrar, se dispara la signal `inscripcion_validada` (Observer) — el receptor actual solo loggea, pero ahí engancharías un correo real, una notificación push, o la sincronización con SITEC/SII sin tocar `services.py`.

## Cómo montarlo en un proyecto Django real

```bash
django-admin startproject config .
python manage.py startapp acom     # y sustituye su contenido por el de esta carpeta

# En config/settings.py:
#   INSTALLED_APPS += ["acom"]

# En config/urls.py:
#   from django.urls import include, path
#   urlpatterns += [path("acom/", include("acom.urls"))]

python manage.py makemigrations acom
python manage.py migrate
python manage.py createsuperuser        # para entrar a /admin/ y crear actividades de prueba

python manage.py test acom              # deben pasar los 5 tests
python manage.py runserver
```

Flujo manual para probarlo en el navegador:

1. Entra a `/admin/` y crea un `User` responsable, un `User` de departamento, y una `ActividadComplementaria`.
2. Inicia sesión como estudiante (o usa otra pestaña/incógnito) y entra a `/acom/` — inscríbete.
3. Inicia sesión como el responsable y entra a `/acom/responsable/<id>/` — evalúa y emite la constancia.
4. Inicia sesión como el usuario de departamento y entra a `/acom/departamento/<id>/` — valida y registra los créditos.
5. Vuelve a `/acom/mis-inscripciones/` como estudiante — verás el crédito reflejado.

## Actividades de aprendizaje (extender el proyecto)

- Agrega un campo `limite_cupo` a `ActividadComplementaria` y haz que `InscripcionService.inscribir` lance una excepción propia cuando ya se alcanzó el cupo.
- Agrega una vista de reporte para el Departamento Académico: lista de todos los estudiantes con sus créditos acumulados y cuántos les faltan (usa `CreditosService`).
- Convierte `panel_responsable` y `panel_departamento` a Class-Based Views, comparando la legibilidad contra las funciones actuales.
- Agrega un permiso de Django (`acom.can_validate_credits`) y restringe `panel_departamento` a usuarios con ese permiso en vez de solo `@login_required`.
- Escribe un nuevo receptor para `inscripcion_validada` que envíe un correo real (usa `django.core.mail.send_mail`, con backend de consola en desarrollo).

## Evaluación sugerida

| Evidencia | Qué valora |
|---|---|
| Tests pasando (`test_services.py` + `test_views.py`) | La lógica de negocio y el flujo HTTP funcionan de extremo a extremo |
| Diagrama de estados de `Inscripcion` dibujado por el estudiante | Comprensión del flujo de tres responsables |
| Extensión con cupo o reporte de créditos | Capacidad de extender el Service Layer sin romper lo existente |
| Explicación oral de dónde vive cada patrón (MVT, Service Layer, Observer) | Conexión explícita con la Unidad 1 |
