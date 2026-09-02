# Git Avanzado — Buenas prácticas, commits y flujos de ramas para equipos reales

Curso complementario a [`curso_git`](../curso_git/README.md) (que cubre los comandos básicos-intermedios). Aquí el foco no es "cómo se usa el comando", sino **cómo trabaja un equipo real con Git**: cómo se escriben commits que cuentan una historia clara, cómo se nombran y organizan las ramas, y cómo se gestionan varios entornos de despliegue (dev/staging/producción) sin pisarse el trabajo entre personas.

## Contenido

- [01_buenas_practicas_generales.md](01_buenas_practicas_generales.md) — Principios generales de higiene de repositorio
- [02_commits_atomicos.md](02_commits_atomicos.md) — Qué es un commit atómico, cómo dividir cambios, `git add -p`
- [03_mensajes_de_commit.md](03_mensajes_de_commit.md) — Conventional Commits: tipos, formato, ejemplos reales
- [04_flujos_de_ramas.md](04_flujos_de_ramas.md) — Git Flow, GitHub Flow, Trunk-Based Development — cuándo usar cada uno
- [05_nombres_de_ramas.md](05_nombres_de_ramas.md) — Convenciones de naming para tracking automático
- [06_multiples_despliegues.md](06_multiples_despliegues.md) — Ramas por entorno, tags, releases, hotfixes, cherry-pick, versionado semántico
- [07_ejercicios.md](07_ejercicios.md) — Ejercicios integradores con solución
- [ejemplos/](ejemplos/README.md) — Scripts ejecutables (uno por tema) + hooks de Git reutilizables (`commit-msg`, `pre-push`)
- [practica_tutorial.md](practica_tutorial.md) — Tutorial paso a paso a mano en tu terminal: de cero a un flujo de release completo con hotfix

## A quién le sirve este curso

Alguien que ya sabe usar `git add`, `git commit`, `git branch`, `git merge` (ver `curso_git`) y ahora necesita trabajar en un repositorio con más de una persona, más de un ambiente de despliegue, y con expectativas de historial legible (para code review, changelogs automáticos, o simplemente para no perderse en 6 meses).
