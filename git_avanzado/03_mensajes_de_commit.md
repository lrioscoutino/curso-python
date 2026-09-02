# 3. Mensajes de commit — Conventional Commits

## Por qué un formato estándar

Un mensaje de commit libre ("arreglos", "cambios varios", "fix") no sirve para nada automatizable: no se puede generar un changelog, no se puede saber si un cambio rompe compatibilidad, no se puede filtrar el historial por tipo de cambio. **Conventional Commits** (conventionalcommits.org) es la convención más adoptada en la industria — la usan Angular, Vue, Electron, y es la base de herramientas como `semantic-release` y `commitizen`.

## Formato

```
<tipo>(<scope opcional>): <descripción corta en imperativo>

<cuerpo opcional — el "por qué", no el "qué">

<footer opcional — BREAKING CHANGE, referencias a issues>
```

## Tipos estándar

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Una nueva funcionalidad para el usuario final |
| `fix` | Corrección de un bug |
| `docs` | Solo cambios de documentación |
| `style` | Formato, espacios, punto y coma — sin cambio de lógica |
| `refactor` | Cambio de código que no arregla un bug ni agrega funcionalidad |
| `perf` | Cambio que mejora el rendimiento |
| `test` | Agregar o corregir tests, sin tocar código de producción |
| `build` | Cambios al sistema de build o dependencias externas |
| `ci` | Cambios a configuración de integración continua |
| `chore` | Tareas de mantenimiento que no encajan en las anteriores |
| `revert` | Revierte un commit anterior |

## Regla de oro de la primera línea

- Máximo ~50-72 caracteres.
- **Imperativo, no pasado**: "agrega validación", no "agregado" ni "agregué". Piensa: "Este commit, al aplicarse, **hace** X" — no "hizo" X.
- Sin punto final.
- Todo en minúsculas salvo nombres propios/siglas.

## `scope` — de qué parte del proyecto se trata

Opcional, entre paréntesis, indica el módulo o área afectada:

```
feat(auth): agrega login con Google OAuth
fix(checkout): corrige cálculo de impuestos en carritos con descuento
docs(readme): documenta variables de entorno requeridas
```

En un monorepo o proyecto grande, el `scope` permite filtrar el historial rápidamente: `git log --grep="^fix(auth)"`.

## `BREAKING CHANGE` — cambios que rompen compatibilidad

Se marca en el footer (o con `!` después del tipo/scope) cuando el cambio rompe la API pública:

```
feat(api)!: cambia el formato de respuesta de /usuarios a paginado

BREAKING CHANGE: el endpoint ya no devuelve un array plano, sino
{ "items": [...], "next_cursor": "..." }. Actualizar los clientes
que consumen /usuarios antes de desplegar.
```

Esto es lo que herramientas de versionado semántico automático usan para decidir si el siguiente release es un `MAJOR` (rompe compatibilidad), `MINOR` (nueva funcionalidad compatible) o `PATCH` (solo fixes) — ver [06_multiples_despliegues.md](06_multiples_despliegues.md).

## Ejemplos completos

```
fix(pagos): evita doble cobro cuando el webhook llega duplicado

Stripe puede reenviar el mismo evento de pago si no confirmamos
rápido. Se agrega verificación por idempotency_key antes de
procesar el cobro.

Closes #482
```

```
refactor(usuarios): extrae lógica de validación a un servicio

Sin cambio de comportamiento — separa la validación de reglas de
negocio de la vista, para poder testearla de forma aislada.
```

```
chore: actualiza dependencias de desarrollo

- black 24.1.0 -> 24.2.0
- pytest 8.0.0 -> 8.1.0
```

## Herramientas que dependen de este formato

- **`git log --oneline --grep="^feat"`** — filtra solo features para armar notas de release.
- **`semantic-release`** / **`standard-version`** — generan automáticamente el número de versión y el `CHANGELOG.md` a partir del historial.
- **Commit hooks** (`commitlint`) — rechazan un commit en CI si no sigue el formato, forzando la disciplina en todo el equipo.

## Práctica

Reescribe estos mensajes reales (tomados de un historial desordenado) al formato Conventional Commits:

1. `"arreglado el bug del carrito"`
2. `"nueva feature de notificaciones push"`
3. `"cambios en el readme y arreglo de typos"`
4. `"cambia el modelo de Usuario, ahora requiere migración"`

**Solución sugerida:**

1. `fix(carrito): corrige el cálculo total cuando hay productos sin stock`
2. `feat(notificaciones): agrega envío de notificaciones push`
3. `docs: corrige typos y actualiza instrucciones de instalación`
4. `feat(usuarios)!: agrega campo obligatorio fecha_nacimiento` + footer `BREAKING CHANGE: requiere correr la migración 0042 antes de desplegar`
