# Plan de trabajo — 7 equipos extienden ACOM según el lineamiento TecNM

**Duración:** 2 semanas (10 días hábiles). **Base:** el código actual de `acom_backend` (4 capas + API v1 con JWT).
**Fuente de requisitos:** *Lineamiento para la Acreditación de Actividades Complementarias* del TecNM (documento compartido en clase).

Cada equipo implementa **una funcionalidad** que falta respecto al lineamiento. Todas atraviesan las cuatro capas (Infraestructura → Dominio → Aplicación → Presentación) y la API. La regla de dependencia del [`README.md`](README.md) sigue vigente: nadie puede saltarse una capa.

> `limite_cupo` **no** es parte de este plan: sigue siendo la *Ronda final* del README.

---

## 1. Qué pide el lineamiento y qué falta en el código

| Lineamiento TecNM | Estado actual | Equipo |
|---|---|---|
| 6 campos de formación con nombres oficiales y un catálogo de actividades por campo | `CategoriaActividad` (`acom/models.py`) tiene 6 opciones con nombres distintos (p. ej. "Publicaciones y ponencias" ≠ "Actividades académicas y de vinculación"); no hay subtipos | **E1** |
| 20 horas ≈ 1 crédito; cada actividad vale entre 1 y 2 créditos | `creditos_valor` es libre (solo `> 0`) y no hay horas | **E2** |
| Una sola actividad o campo no puede dar todos los créditos (formación variada) | Solo existe el límite global `META_CREDITOS = 5` (`acom/domain/reglas.py`) | **E3** |
| Cumplir el mínimo de horas antes de acreditar | `evaluar` no revisa horas | **E4** |
| Las actividades se ofertan por periodo escolar | No hay periodo ni fechas de inscripción | **E5** |
| Constancia de acreditación firmada por el responsable del área | `Constancia` solo guarda el folio; no hay documento | **E6** |
| 5 créditos totales durante la carrera, repartidos entre campos | `resumen` solo da el total y lo que falta | **E7** |

---

## 2. Reglas comunes para todos los equipos

1. **Capas:** el dominio no importa Django (`ReglaDeDependenciaTest` en `acom/tests/test_domain.py` debe seguir pasando). Las reglas nuevas son funciones puras en `acom/domain/`.
2. **Errores:** cada error nuevo hereda de `AcomError` (`acom/domain/exceptions.py`). La API lo convierte en `400` sin cambios gracias a `api/exceptions.py`; si necesitan otro código, lo agregan **ahí** y en ningún otro lugar.
3. **Permisos:** solo en `acom/services/permisos.py` (reutilicen `exigir_responsable` y `exigir_permiso`).
4. **Lecturas:** toda consulta nueva es una función en `acom/selectors.py`; las vistas y los servicios no arman consultas.
5. **API v1:** solo cambios **aditivos**. No se borra ni renombra ningún campo ni endpoint existente. Documenten cada endpoint nuevo con `extend_schema` para que aparezca en `/api/docs/`.
6. **Pruebas mínimas por equipo:**
   - dominio con `SimpleTestCase` (sin base de datos);
   - servicio con `AcomTestCase` (`acom/tests/base.py`);
   - API con JWT, siguiendo el patrón de `autenticar_con_jwt` en `api/tests.py`.
7. **Calidad:** `uv run python manage.py test` y `uv run ruff check --no-fix acom api config` en verde antes de abrir el PR.

### Archivos compartidos (zona de conflictos)

`acom/models.py`, `acom/domain/exceptions.py`, `acom/domain/reglas.py`, `acom/services/inscripciones.py`, `acom/selectors.py`, `acom/tests/base.py`, `api/serializers.py`, `api/urls.py`, `api/exceptions.py`.

- **Solo agregar**, al final de su bloque. No reordenar, no reformatear código ajeno.
- Prefieran **archivos nuevos** para su código: `acom/services/horas.py`, `acom/services/periodos.py`, `api/views_kardex.py`, `acom/tests/test_horas.py`, etc.
- Si su funcionalidad obliga a cambiar los *fixtures* de `acom/tests/base.py` (E2, E3 y E4 casi seguro), avisen en el canal del grupo y hagan el cambio en un commit aparte y pequeño.

---

## 3. Fichas por equipo

### E1 — Catálogo oficial de campos y tipos de actividad · *Oleada 1*

**Lineamiento:** las actividades se agrupan en 6 campos de formación, y cada campo tiene un catálogo de actividades permitidas.

| Capa | Cambios |
|---|---|
| Infraestructura | Cambiar las **etiquetas** de `CategoriaActividad` a los 6 nombres oficiales (Tutoría; Actividades formativas / Cursos; Investigación y desarrollo tecnológico; Actividades académicas y de vinculación; Actividades culturales y deportivas; Compromiso social y ambiental). **No cambien los `value`** para no romper datos. Nuevo modelo `TipoActividad(campo, nombre, descripcion)` y FK opcional `ActividadComplementaria.tipo`. Migración de datos que cargue el catálogo del lineamiento (tutoría entre pares, certificación profesional, idiomas, InnovatecNM, verano de investigación, congreso, concurso académico, selección deportiva, brigada comunitaria, etc.). Registrar en `admin.py`. |
| Dominio | Regla pura `tipo_pertenece_a_campo(campo_tipo, campo_actividad) -> bool`. Error `TipoNoCorrespondeError`. |
| Aplicación | Servicio `asignar_tipo(actividad, tipo, usuario)` que valida la regla (solo el departamento, con `exigir_permiso`). |
| Presentación | HTML: mostrar campo y tipo en `lista_actividades.html`. API: `GET /api/v1/campos/` (campos con sus tipos) y `tipo` en `ActividadComplementariaSerializer`. |

**Aceptación:** Swagger lista los 6 campos oficiales con sus tipos; una actividad no acepta un tipo de otro campo.

---

### E2 — Horas y valor en créditos · *Oleada 1*

**Lineamiento:** 20 horas equivalen a 1 crédito; cada actividad vale entre 1 y 2 créditos.

| Capa | Cambios |
|---|---|
| Infraestructura | Campo `horas_requeridas` (`PositiveIntegerField`) en `ActividadComplementaria`. `CheckConstraint` 1 ≤ `creditos_valor` ≤ 2. |
| Dominio | Constantes `HORAS_POR_CREDITO = 20`, `CREDITOS_MIN = 1`, `CREDITOS_MAX = 2`. Reglas puras `creditos_por_horas(horas) -> Decimal` y `creditos_en_rango(creditos) -> bool`. Error `CreditosFueraDeRangoError`. |
| Aplicación | Servicio `crear_actividad(...)` (o validación en un servicio existente) que calcule los créditos a partir de las horas y rechace valores fuera de rango. |
| Presentación | Mostrar horas y créditos en HTML. API: `horas_requeridas` en `ActividadComplementariaSerializer`. |

**Ojo:** `test_no_se_registran_creditos_pasado_el_limite` (`acom/tests/test_services.py`) crea una actividad de `3.00` créditos, que queda fuera de rango. Ajusten esa prueba para que siga probando el límite de 5 créditos con actividades de 1–2 créditos.

**Aceptación:** 40 horas dan 2 créditos; una actividad de 3 créditos no se puede guardar.

---

### E3 — Límite de créditos por campo · *Oleada 2 (depende de E1)*

**Lineamiento:** un solo campo no puede aportar todos los créditos, para garantizar una formación variada.

| Capa | Cambios |
|---|---|
| Infraestructura | Selector `total_validado_por_campo(estudiante, campo) -> Decimal`, con el mismo `quantize` que `total_validado`. |
| Dominio | Constante `MAX_CREDITOS_POR_CAMPO = Decimal("2.00")`. Regla pura `excede_limite_campo(total_campo, creditos_nuevos) -> bool`. Error `LimiteCampoError`. |
| Aplicación | `validar_y_registrar` revisa el límite por campo **después** de bloquear al estudiante (el `select_for_update` que ya existe también protege esta regla). |
| Presentación | El panel del departamento muestra el error; la API responde `400` con el mensaje. |

**Ojo:** los *fixtures* crean todas las actividades en `INVESTIGACION`. Agreguen un parámetro `categoria` a `crear_actividad` en `acom/tests/base.py` (con el valor actual como *default*) para que las pruebas de límite global sigan pasando.

**Aceptación:** un estudiante con 2 créditos en Investigación no puede validar otro crédito en Investigación, pero sí en Tutoría.

---

### E4 — Registro de horas cumplidas · *Oleada 2 (depende de E2)*

**Lineamiento:** cada actividad exige un mínimo de horas cumplidas antes de acreditarse.

| Capa | Cambios |
|---|---|
| Infraestructura | Modelo `RegistroHoras(inscripcion, fecha, horas, registrado_por)` con `CheckConstraint` `horas > 0`. Selector `horas_acumuladas(inscripcion) -> int`. |
| Dominio | Regla pura `horas_cumplidas(acumuladas, requeridas) -> bool`. Error `HorasInsuficientesError`. |
| Aplicación | Nuevo `acom/services/horas.py` con `registrar_horas(inscripcion_id, usuario, fecha, horas)`: solo el responsable (`exigir_responsable`) y solo si la inscripción está en estado `INSCRITO`. `evaluar(aprobado=True)` exige horas cumplidas; rechazar no las exige. |
| Presentación | Formulario de horas en `panel_responsable.html`. API: `POST /api/v1/responsable/inscripciones/<id>/horas/` y horas acumuladas en el detalle. |

**Ojo:** `inscripcion_con_constancia` en `acom/tests/base.py` aprueba sin horas. Hagan que registre las horas requeridas antes de evaluar.

**Aceptación:** no se puede aprobar una inscripción con 15 de 20 horas; con 20 sí.

---

### E5 — Periodos escolares y fechas de inscripción · *Oleada 2 (independiente)*

**Lineamiento:** las actividades se ofertan y acreditan dentro de un periodo escolar.

| Capa | Cambios |
|---|---|
| Infraestructura | Modelo `Periodo(clave, inicio, fin)` (p. ej. `"2026-2"`, clave única). FK opcional `periodo` y campos `inscripcion_abre` / `inscripcion_cierra` en `ActividadComplementaria`. `actividades_activas()` acepta un `periodo` opcional. |
| Dominio | Regla pura `inscripcion_abierta(hoy, abre, cierra) -> bool` (si no hay fechas, está abierta). Error `InscripcionCerradaError`. |
| Aplicación | `inscribir` valida la ventana de fechas (reciban `hoy` como parámetro o usen `timezone.localdate()` en el servicio, **nunca** en el dominio). |
| Presentación | HTML: mostrar la ventana de inscripción. API: filtro `GET /api/v1/actividades/?periodo=2026-2` y los campos nuevos en el serializer. |

**Aceptación:** inscribirse fuera de la ventana devuelve `400` con mensaje claro; las pruebas de dominio usan fechas fijas, sin reloj real.

---

### E6 — Constancia de acreditación descargable · *Oleada 2 (independiente)*

**Lineamiento:** cada actividad requiere la Constancia de Acreditación firmada por el responsable del área.

| Capa | Cambios |
|---|---|
| Infraestructura | Campos `area_responsable` y `horas_acreditadas` en `Constancia` (valores por defecto para no romper registros existentes). Selector `constancia_de(inscripcion_id)`. |
| Dominio | Regla pura `puede_ver_constancia(usuario_id, estudiante_id, responsable_id) -> bool`. Reutilicen `generar_folio`. |
| Aplicación | `emitir_constancia` llena los campos nuevos. Servicio `obtener_constancia(inscripcion_id, usuario)` que autoriza con la regla anterior (en `permisos.py`). |
| Presentación | Plantilla imprimible `acom/templates/acom/constancia.html` (folio, estudiante, actividad, campo, horas, créditos, fecha, responsable y espacio de firma) y su URL en `acom/urls.py`. API: `GET /api/v1/mis-inscripciones/<id>/constancia/` devuelve los datos en JSON. **Extra opcional:** exportar a PDF. |

**Aceptación:** el estudiante dueño y el responsable ven la constancia; cualquier otro usuario recibe `403`.

---

### E7 — Kárdex y avance por campo · *Oleada 2 (depende de E1 y E3)*

**Lineamiento:** se necesitan 5 créditos durante la carrera, con formación variada entre campos.

| Capa | Cambios |
|---|---|
| Infraestructura | Selector `avance_por_campo(estudiante) -> dict[campo, Decimal]` (una sola consulta con `values(...).annotate(Sum(...))`). Selector `estudiantes_liberables()` para el departamento. |
| Dominio | Regla pura `puede_liberar(total, por_campo) -> bool`: total ≥ `META_CREDITOS` y ningún campo por encima de `MAX_CREDITOS_POR_CAMPO`. |
| Aplicación | Caso de uso `kardex(estudiante)` que junte total, faltantes, desglose y si puede liberar. |
| Presentación | HTML: vista de kárdex del estudiante. API: **ampliar** `GET /api/v1/mis-inscripciones/resumen/` con `por_campo` y `liberado` (se agregan campos a `ResumenCreditosSerializer` y los actuales se quedan). `GET /api/v1/departamento/liberables/` con `PuedeValidarCreditos`. |

**Aceptación:** el resumen muestra los 6 campos (incluidos los que están en 0) y `liberado` pasa a `true` al llegar a 5 créditos válidos.

---

## 4. Coordinación

### Dependencias y orden de merge

```
Oleada 1 (días 1–5):   E1 ──┐        E2 ──┐        E5, E6 (en paralelo, archivos propios)
                            │             │
Oleada 2 (días 6–9):   E3 ◄─┘        E4 ◄─┘
                        │
                       E7 ◄── E1 + E3
```

**Orden de merge a `main`:** E1 → E2 → E5 → E6 → E3 → E4 → E7.
E5 y E6 empiezan desde el día 1, pero se integran después de E1/E2 porque tocan los mismos modelos.

### Ramas y PR

- Rama por equipo: `equipo-1/catalogo-campos`, `equipo-2/horas-creditos`, …, `equipo-7/kardex`.
- Un PR por equipo hacia `main`, **revisado por otro equipo** (rotación: E1 revisa E2, E2 revisa E3, …, E7 revisa E1).
- Requisito de merge: pruebas y ruff en verde, y Swagger actualizado.

### Migraciones (riesgo principal)

1. Trabajen sin migración mientras diseñan; generen la suya **justo antes de abrir el PR**, después de `git pull origin main`.
2. Nunca editen una migración de otro equipo.
3. Si al integrar hay conflicto (dos migraciones `0002_...`), **borren la suya y regenérenla** sobre `main`: `uv run python manage.py makemigrations acom`.
4. Las migraciones de datos (E1) van en un archivo propio, no mezcladas con cambios de esquema.

---

## 5. Calendario

| Día | Actividad | Entregable |
|---|---|---|
| 1 | Leer el lineamiento y el README; cada equipo diseña su cambio por capa | Ficha de diseño (1 página) con la regla del lineamiento que implementa |
| 2–4 | Oleada 1: E1 y E2 implementan; E5 y E6 avanzan en dominio, servicios y pruebas | Pruebas de dominio en verde |
| 5 | Merge de E1 y E2; revisión cruzada | `main` con catálogo y horas |
| 6–8 | Oleada 2: E3, E4 y E7 sobre el `main` nuevo; E5 y E6 se integran | PRs abiertos |
| 9 | Integración: merges en orden, suite completa en verde, prueba manual en `/acom/` y `/api/docs/` | `main` estable |
| 10 | Demo de 10 minutos por equipo (misma dinámica del README) | Presentación + prueba en vivo |

---

## 6. Evaluación

| Criterio | Peso | Qué se revisa |
|---|---|---|
| Cumple el lineamiento | 25 % | La regla implementada coincide con el documento del TecNM y la ficha la cita |
| Respeta las capas | 25 % | Dominio sin Django, permisos en `permisos.py`, lecturas en `selectors.py`, errores como `AcomError` |
| Pruebas | 20 % | Dominio sin BD + servicio + API con JWT; la suite completa sigue en verde |
| API y documentación | 15 % | Endpoint visible y usable en Swagger, cambios aditivos en v1 |
| Trabajo en equipo | 15 % | PR limpio, revisión cruzada útil, sin romper el trabajo de otros equipos |

---

## 7. Cómo probar cada funcionalidad en Swagger

1. `uv run python manage.py runserver` y abrir `http://127.0.0.1:8000/api/docs/`.
2. `POST /api/v1/auth/token/` con su usuario → copiar `access`.
3. **Authorize** → pegar el token (sin `Bearer `).
4. Probar sus endpoints con usuarios de cada rol: estudiante, responsable y departamento con permiso *Puede validar constancias y registrar créditos*.
