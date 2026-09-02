# 6. Manejo de múltiples despliegues

Cuando un proyecto tiene varios entornos (desarrollo, staging/QA, producción) — o varias versiones en producción a la vez — la pregunta ya no es solo "qué flujo de ramas" sino "cómo se traduce el estado de una rama en el estado de un servidor real".

## Estrategia 1 — Una rama por entorno

La más directa: cada entorno de despliegue corresponde exactamente a una rama.

```
develop   ──●──●──●──●──●──●──   → se despliega automático a DEV
                  \
staging   ─────────●──●──●────   → se despliega automático a STAGING
                        \
main      ───────────────●────   → se despliega automático a PRODUCCIÓN
```

Flujo: el código avanza de `develop` → `staging` → `main` mediante Pull Requests (nunca commits directos), y cada fusión dispara el despliegue de ese ambiente vía CI/CD.

**Ventaja:** extremadamente simple de razonar — "¿qué hay en producción? lo que está en `main`".
**Desventaja:** si necesitas desplegar algo a staging sin llevarlo aún a producción, y luego otra cosa distinta también a staging, las ramas empiezan a divergir de forma confusa.

## Estrategia 2 — Tags de versión + una sola rama principal

Común en Trunk-Based Development y GitHub Flow: no hay ramas por ambiente. En vez de eso, cada despliegue a producción se marca con un **tag** inmutable.

```bash
git tag -a v2.4.0 -m "Release 2.4.0: agrega checkout con Apple Pay"
git push origin v2.4.0
```

El sistema de despliegue no despliega "una rama", despliega "un tag específico" — así producción siempre corresponde a un punto exacto e inmutable del historial, sin importar qué pase después en `main`.

**Ventaja:** producción es trazable a un commit exacto sin ambigüedad; permite tener staging apuntando a `main` (móvil) y producción apuntando a un tag (fijo) sin ramas extra.
**Desventaja:** requiere disciplina de taggear cada release; sin herramienta de automatización se vuelve manual y propenso a error.

## Versionado semántico (SemVer)

Los tags de versión siguen el formato `MAJOR.MINOR.PATCH`:

```
2.4.1
│ │ └── PATCH: solo fixes, compatible hacia atrás
│ └──── MINOR: nueva funcionalidad, compatible hacia atrás
└────── MAJOR: rompe compatibilidad
```

Esto conecta directo con Conventional Commits ([03_mensajes_de_commit.md](03_mensajes_de_commit.md)): un commit `fix:` sugiere subir el PATCH, un `feat:` sugiere subir el MINOR, y un `BREAKING CHANGE` obliga a subir el MAJOR. Herramientas como `semantic-release` calculan el próximo número de versión automáticamente leyendo el historial de commits desde el último tag.

## Hotfixes en producción sin traer código no probado

**El problema:** hay un bug urgente en producción, pero `main`/`develop` ya tiene trabajo nuevo a medio terminar que no debe ir a producción todavía.

**La solución — rama hotfix desde el tag de producción, no desde `develop`:**

```bash
# Producción está en el tag v2.4.0
git checkout -b hotfix/prod-500-checkout v2.4.0

# ... arreglar el bug, commitear ...

git tag -a v2.4.1 -m "Hotfix: corrige error 500 en checkout"
git push origin v2.4.1     # esto es lo que se despliega a producción

# Traer el fix de vuelta a la rama de desarrollo para que no se pierda
git checkout develop
git merge hotfix/prod-500-checkout
```

Esto garantiza que el hotfix contiene **exactamente** el código de producción más el fix — nada del trabajo en progreso de `develop` se cuela por accidente.

## Cherry-pick: llevar un commit específico entre ramas

Cuando un fix necesita aplicarse a producción **y** a una versión anterior con soporte activo (ej. `v1.x` sigue en soporte mientras se desarrolla `v2.x`):

```bash
git log --oneline           # identificar el hash del commit del fix
git checkout release/1.x
git cherry-pick a1b2c3d      # aplica SOLO ese commit, no toda la rama
```

`cherry-pick` copia un commit puntual de una rama a otra sin fusionar el historial completo — ideal para backportear un fix de seguridad a múltiples versiones en soporte simultáneo.

## Rollback: revertir un despliegue

Si algo salió mal después de desplegar, hay dos formas:

**Opción A — Revertir el commit (preferida, deja rastro):**

```bash
git revert -m 1 <hash-del-merge-commit>
git push origin main
# CI/CD despliega automáticamente el revert
```

**Opción B — Redesplegar el tag anterior (más rápido, sin cambiar el historial):**

```bash
# Simplemente le decimos al sistema de despliegue: vuelve a desplegar v2.3.0
```

La opción B es más rápida para "apagar el incendio" ahora mismo; la opción A es necesaria después para que el historial refleje qué pasó y por qué (y para que el próximo `git pull` de cualquiera no reintroduzca el bug).

## Resumen — checklist de un pipeline de múltiples despliegues sano

- [ ] Cada entorno tiene una fuente de verdad clara (una rama, o un tag) — nunca "lo que el servidor tenga ahora mismo".
- [ ] Producción se despliega desde un punto **inmutable** (tag), no desde la punta móvil de una rama.
- [ ] Los hotfixes nacen del código *en producción*, no del código en desarrollo.
- [ ] Existe un camino documentado de rollback que no dependa de memoria humana bajo presión.
- [ ] El número de versión sube según el impacto real del cambio (SemVer), no arbitrariamente.
