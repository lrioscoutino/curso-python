# 8. Buenas prácticas (introducción)

Esta sección da el mínimo indispensable. Para el tratamiento completo —commits atómicos, Conventional Commits, comparativa de flujos de ramas (Git Flow / GitHub Flow / Trunk-Based), y manejo de múltiples entornos de despliegue— ver el curso [`git_avanzado`](../git_avanzado/README.md).

## Mensajes de commit

- Usa **imperativo**: "Añade" en vez de "Añadido" o "Añadí" — el commit, al aplicarse, *hace* algo.
- Primera línea corta (idealmente bajo 50-72 caracteres).
- Si hace falta más contexto, deja una línea en blanco y luego el cuerpo explicando el **por qué**, no el cómo (el diff ya muestra el cómo).

```bash
git commit -m "Añade validación de email en formulario de registro

Implementa validación tanto en frontend como backend
para prevenir emails inválidos en la base de datos."
```

> El siguiente paso natural después de esto es adoptar un formato estándar como **Conventional Commits** (`feat:`, `fix:`, `docs:`, ...) — ver [git_avanzado/03_mensajes_de_commit.md](../git_avanzado/03_mensajes_de_commit.md).

## Estructura de ramas (vista rápida)

- `main` — código de producción.
- `develop` — rama de integración de desarrollo (si el proyecto usa Git Flow).
- `feature/nombre` — nuevas características.
- `hotfix/nombre` — correcciones urgentes.
- `release/version` — preparación de una versión.

> Ver [git_avanzado/04_flujos_de_ramas.md](../git_avanzado/04_flujos_de_ramas.md) para cuándo conviene cada flujo, y [git_avanzado/05_nombres_de_ramas.md](../git_avanzado/05_nombres_de_ramas.md) para una convención de nombres completa.

## Comandos útiles para mantener el repo limpio

```bash
git branch --merged                # ver ramas locales ya fusionadas (candidatas a borrar)
git remote prune origin            # limpiar referencias a ramas remotas que ya no existen
git gc                             # garbage collection — compacta el repositorio
```

---

**Anterior:** [07_resolucion_conflictos.md](07_resolucion_conflictos.md) · **Siguiente:** [09_ejercicios_practicos.md](09_ejercicios_practicos.md)
