# Desarrollo Web Avanzado — Unidad 1: Introducción

Código de ejemplo y tareas para la Unidad 1 (buenas prácticas de programación y
patrones de diseño), en Python, con los patrones aplicados tal como se ven en
Django. Todo el código es standalone — corre con `python3 archivo.py` sin
necesitar Django instalado, ya que se simulan los conceptos (Manager, Signal,
Decorator, etc.) con clases planas de Python para enfocarse en el patrón, no
en la configuración del framework.

## Estructura

```
unidad_1/
├── ejemplos/     # código de referencia, resuelto y comentado — para estudiar y correr
├── tareas/       # ejercicios con TODO — el estudiante completa las funciones marcadas
└── soluciones/   # soluciones de referencia de cada tarea (no ver antes de intentarlo)
```

## Ejemplos (`ejemplos/`)

| Archivo | Tema |
|---|---|
| `01_pep8_legibilidad.py` | PEP 8 y legibilidad — código "malo" vs "bueno" lado a lado |
| `02_principios_solid.py` | Los 5 principios SOLID, uno por clase, con ejemplo violado vs corregido |
| `03_patron_factory_manager.py` | Factory Method — Manager de Django simulado (querysets filtrados) |
| `04_patron_decorator.py` | Decorator — `@login_required` y `@cache` simulados |
| `05_patron_observer_signals.py` | Observer — signals de Django simuladas (post_save) |
| `06_patron_singleton_settings.py` | Singleton — `django.conf.settings` simulado |
| `07_patron_service_layer.py` | Service Layer — lógica de negocio fuera de la vista |
| `08_django_singleton_real.py` | Singleton — `django.conf.settings` con código Django **real** (no ejecutable sin proyecto) |
| `09_django_mvt_real.py` | MVT — Modelo/Vista/Template/urls.py **reales** de un CRUD de Artículo (no ejecutable sin proyecto) |
| `10_django_factory_manager_real.py` | Factory Method — Manager + QuerySet personalizados **reales** con el ORM (no ejecutable sin proyecto) |

Los archivos `08`–`10` usan código Django auténtico (import real de `django.db.models`, `django.conf.settings`, etc.) en vez de simulaciones — por eso no corren standalone con `python3 archivo.py`: el código está comentado con docstrings triple-quote, documentado por bloques (`models.py`, `views.py`, `urls.py`, template), pensado para copiar dentro de un proyecto Django real o leer como referencia.

Correr los ejemplos standalone (01–07):

```bash
python3 ejemplos/03_patron_factory_manager.py
```

## Tareas (`tareas/`)

Cada archivo tiene funciones/clases con `# TODO` y `raise NotImplementedError`.
Cada archivo incluye pruebas al final que confirman si la tarea quedó bien resuelta.

| Archivo | Qué se pide |
|---|---|
| `tarea_01_refactor_pep8.py` | Refactorizar una función con mal estilo a PEP 8 |
| `tarea_02_solid_srp.py` | Separar una clase que viola SRP en clases con una sola responsabilidad |
| `tarea_03_factory_manager.py` | Implementar un Manager personalizado (Factory) para filtrar objetos |
| `tarea_04_decorator_retry.py` | Implementar un decorador `@reintentar` que reintenta una función N veces |
| `tarea_05_observer_eventos.py` | Implementar un sistema de eventos (Observer) tipo signals |

Correr una tarea (ejecuta sus propias pruebas):

```bash
python3 tareas/tarea_04_decorator_retry.py
```

## Soluciones (`soluciones/`)

Un archivo espejo por cada tarea, con la implementación completa.
