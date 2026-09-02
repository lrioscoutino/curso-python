# Manual de Git: de básico a intermedio

Curso introductorio de Git — conceptos, comandos y ejercicios prácticos para llegar a manejar ramas, colaboración remota y conflictos con confianza. Para el siguiente nivel (commits atómicos, Conventional Commits, flujos de ramas, y manejo de múltiples entornos de despliegue), continúa con [`git_avanzado`](../git_avanzado/README.md).

## Contenido

1. [01_introduccion_y_conceptos.md](01_introduccion_y_conceptos.md) — Qué es Git, los tres estados de un archivo
2. [02_configuracion_inicial.md](02_configuracion_inicial.md) — Identidad, editor, rama por defecto
3. [03_comandos_basicos.md](03_comandos_basicos.md) — init, add, commit, log, diff
4. [04_ramas.md](04_ramas.md) — Crear, cambiar, fusionar y eliminar ramas
5. [05_trabajo_colaborativo.md](05_trabajo_colaborativo.md) — Remotos, push, pull
6. [06_comandos_intermedios.md](06_comandos_intermedios.md) — restore/reset, stash, rebase, cherry-pick
7. [07_resolucion_conflictos.md](07_resolucion_conflictos.md) — Provocar y resolver un conflicto real
8. [08_buenas_practicas.md](08_buenas_practicas.md) — Mensajes de commit, estructura de ramas (introducción)
9. [09_ejercicios_practicos.md](09_ejercicios_practicos.md) — 5 ejercicios integradores con solución
10. [10_referencia_rapida.md](10_referencia_rapida.md) — Chuleta de comandos

## Requisito

Git instalado (`git --version`). No requiere cuenta de GitHub hasta el capítulo 5 (trabajo colaborativo).

## Nota sobre esta versión

Todos los ejercicios y comandos de este curso fueron **verificados ejecutándolos** — incluidas las correcciones a dos problemas reales de una versión anterior: el Ejercicio 2 pedía hacer `git push` a un repositorio público que el estudiante no controla (falla con `403 Permission denied`), y el Ejercicio 4 mezclaba tres modos de `git reset` en una secuencia confusa que se pisaba a sí misma. Ambos quedaron corregidos y probados de punta a punta.
