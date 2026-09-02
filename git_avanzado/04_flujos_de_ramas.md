# 4. Flujos de ramas (branching strategies)

Un "flujo de ramas" es el conjunto de reglas que dicen: qué ramas existen, para qué sirve cada una, y cómo se mueve el código entre ellas hasta llegar a producción. Elegir uno malo para el tamaño/ritmo del equipo genera fricción constante — elegirlo bien hace que el equipo casi ni piense en Git.

## Git Flow

El más estructurado, pensado para proyectos con **ciclos de release programados** (no despliegue continuo).

```
main        ●───────────────●───────●        (solo versiones publicadas, taggeadas)
             \               \       \
release/1.2   \               ●───●   \        (estabilización antes de publicar)
               \             /         \
develop    ●────●────●──────●──●───●────●     (integración continua de features)
            \        \          /
feature/a    ●───●────●        /
                                
feature/b        ●────●───────●
```

- **`main`** — solo código que ya está en producción. Cada commit en `main` idealmente es un tag de versión.
- **`develop`** — rama de integración; siempre "el próximo release en construcción".
- **`feature/*`** — sale de `develop`, vuelve a `develop`.
- **`release/*`** — sale de `develop` cuando se congela el alcance de una versión; solo recibe fixes de última hora; al terminar se fusiona a `main` (y se tag-ea) y de vuelta a `develop`.
- **`hotfix/*`** — sale de `main` directo (no de `develop`) para arreglar algo urgente en producción sin esperar el siguiente release; se fusiona a `main` y a `develop`.

**Cuándo usarlo:** software con versiones formales (apps de escritorio, librerías publicadas, sistemas con ventanas de mantenimiento). Es más pesado de lo que necesita un equipo que despliega varias veces al día.

## GitHub Flow

Mucho más simple, pensado para **despliegue continuo**.

```
main    ●──●──●──●──●──●──●──●     (siempre desplegable)
         \       \        \
feature/a ●───●───●
                  feature/b ●──●──●
```

Reglas:

1. `main` siempre está en estado desplegable.
2. Todo cambio nace en una rama (`feature/algo`) desde `main`.
3. Se abre un Pull Request tan pronto como sea útil recibir feedback (no solo al terminar).
4. Al aprobarse el PR (y pasar CI), se fusiona a `main`.
5. Fusionar a `main` dispara el despliegue (automático o manual, pero inmediato).

**Cuándo usarlo:** aplicaciones web con despliegue continuo, equipos pequeños/medianos, SaaS. Es el flujo por default recomendado si no hay una razón específica para algo más complejo.

## Trunk-Based Development

El más agresivo hacia la simplicidad: **casi no hay ramas de larga duración**, todo el mundo integra a `main` (el "trunk") con mucha frecuencia — a veces varias veces al día.

```
main    ●●●●●●●●●●●●●●●●●●●●●●●●●●●●     (commits directos o ramas de vida <1 día)
```

- Ramas de feature, si existen, duran horas, no días — se fusionan rápido con **feature flags** para ocultar funcionalidad incompleta en producción, en vez de mantenerla aislada en una rama.
- Requiere una suite de tests robusta y CI confiable, porque no hay una rama "segura" donde aislar código a medio terminar.
- Es el flujo que usan Google, Meta y la mayoría de equipos de alto rendimiento con release continuo varias veces al día.

**Cuándo usarlo:** equipos con CI/CD maduro, buena cobertura de tests, y cultura de feature flags. Mal ajuste si el equipo no tiene disciplina de tests — sin eso, `main` se rompe constantemente.

## Comparativa rápida

| | Git Flow | GitHub Flow | Trunk-Based |
|---|---|---|---|
| Complejidad | Alta | Baja | Muy baja |
| Ramas de larga duración | Sí (`develop`, `release/*`) | No | Casi ninguna |
| Ideal para | Releases versionados, apps con múltiples versiones en soporte | Despliegue continuo web/SaaS | Equipos grandes con CI/CD maduro |
| Requiere feature flags | No (las ramas aíslan el trabajo) | A veces | Sí, casi siempre |
| Frecuencia de fusión a la rama principal | Baja (por release) | Media (por feature) | Muy alta (varias veces al día) |

## Regla práctica para decidir

- ¿El software se distribuye en versiones con soporte paralelo (v1.x sigue recibiendo fixes mientras se desarrolla v2.0)? → **Git Flow**.
- ¿Es una app web/SaaS que se despliega seguido y solo existe "la versión actual en producción"? → **GitHub Flow**.
- ¿El equipo ya tiene CI/CD sólido y quiere velocidad máxima? → **Trunk-Based**.

Ver [06_multiples_despliegues.md](06_multiples_despliegues.md) para cómo cada flujo se adapta cuando además hay varios **entornos** (dev/staging/producción), que es una pregunta distinta a "qué flujo de ramas usar".
