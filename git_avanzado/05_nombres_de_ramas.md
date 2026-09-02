# 5. Nombres de ramas para tracking

## Por qué el nombre de la rama importa

El nombre de una rama es metadato gratis: si sigue un patrón, se puede filtrar, automatizar (CI que solo corre en `release/*`), vincular a un sistema de tickets, y entender de un vistazo qué es y quién la creó — sin abrir el PR.

## Patrón recomendado

```
<tipo>/<ticket-o-referencia>-<descripcion-corta-en-kebab-case>
```

Ejemplos:

```
feature/PROJ-482-login-google-oauth
fix/PROJ-511-doble-cobro-webhook-stripe
hotfix/prod-500-error-checkout
release/v2.3.0
chore/actualiza-dependencias-enero
docs/guia-contribucion
```

## Prefijos comunes

| Prefijo | Uso |
|---|---|
| `feature/` (o `feat/`) | Nueva funcionalidad |
| `fix/` | Corrección de bug |
| `hotfix/` | Corrección urgente directo desde producción |
| `release/` | Preparación de una versión (Git Flow) |
| `chore/` | Mantenimiento, dependencias, configuración |
| `docs/` | Solo documentación |
| `refactor/` | Reestructuración sin cambio de comportamiento |
| `spike/` o `experiment/` | Prueba de concepto, puede no llegar a mergearse |

## Por qué incluir el número de ticket

Cuando la rama incluye el ID del ticket (`PROJ-482`), la mayoría de herramientas (Jira, Linear, GitHub Issues con "Linked branches", GitLab) lo detectan automáticamente y:

- Conectan la rama/PR al ticket sin acción manual.
- Al fusionar el PR, pueden cerrar o mover el ticket de estado automáticamente.
- Permiten navegar desde el ticket directo a los commits relacionados.

Esto es tracking real: cualquiera puede reconstruir "qué código resolvió qué pedido de trabajo" meses después, sin depender de memoria ni de buscar en Slack.

## Reglas de formato

- **kebab-case, todo minúsculas** — evita espacios y mayúsculas, que causan problemas en distintos sistemas operativos y en URLs.
- **Corto pero descriptivo** — `fix/PROJ-511-doble-cobro-webhook-stripe` dice más que `fix/bug1` sin ser un párrafo.
- **Sin información que cambie** — no incluir fechas ni nombres de persona en el nombre de la rama de feature; esa información ya vive en los metadatos del commit/PR (autor, fecha).
- **Consistencia > preferencia personal** — la convención exacta importa menos que que **todo el equipo use la misma**.

## Ejemplo de flujo completo usando el nombre para automatización

```yaml
# .github/workflows/ci.yml (fragmento)
on:
  push:
    branches:
      - 'feature/**'
      - 'fix/**'

jobs:
  test:
    # corre en cualquier rama feature/* o fix/*
  deploy-preview:
    if: startsWith(github.ref, 'refs/heads/release/')
    # solo despliega un ambiente de preview para ramas release/*
```

El patrón de nombre no es solo estética — es lo que hace posible que la automatización (CI/CD) tome decisiones distintas según qué tipo de rama está corriendo.

## Práctica

Para cada situación, escribe el nombre de rama que seguiría la convención de este capítulo:

1. Vas a agregar autenticación de dos factores, ticket `AUTH-204`.
2. Hay un error 500 en producción en el checkout, sin ticket todavía (urgente).
3. Vas a actualizar la versión de Django del proyecto.
4. Vas a preparar la versión `3.0.0` del producto.

**Solución sugerida:**

1. `feature/AUTH-204-autenticacion-dos-factores`
2. `hotfix/prod-500-checkout`
3. `chore/actualiza-django`
4. `release/v3.0.0`
