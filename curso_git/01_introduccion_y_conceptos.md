# 1. Introducción y conceptos fundamentales

## ¿Qué es Git?

Git es un sistema de control de versiones distribuido que permite rastrear cambios en archivos y coordinar el trabajo entre múltiples desarrolladores. Fue creado por Linus Torvalds en 2005 para el desarrollo del kernel de Linux.

### Características principales

- **Distribuido** — cada desarrollador tiene una copia completa del historial del proyecto.
- **Velocidad** — operaciones locales rápidas (no dependen de la red salvo al sincronizar con un remoto).
- **Integridad** — cada commit se identifica con un hash SHA-1 calculado a partir de su contenido; cambiar cualquier byte del historial cambia el hash.
- **Soporte para desarrollo no lineal** — ramas y fusiones eficientes.

## Conceptos fundamentales

| Concepto | Qué es |
|---|---|
| **Repository (repositorio)** | Un directorio que contiene todos los archivos del proyecto y el historial completo de cambios. |
| **Working directory (directorio de trabajo)** | Los archivos del proyecto tal como existen en tu sistema de archivos local, en su estado actual. |
| **Staging area (área de preparación / index)** | Área intermedia donde se preparan los cambios antes de confirmarlos con un commit. |
| **Commit** | Una instantánea de los cambios en un momento específico, identificada por un hash único. |
| **Branch (rama)** | Una línea de desarrollo independiente. La rama principal suele llamarse `main` (antes `master`). |
| **HEAD** | Puntero que indica en qué commit (o rama) te encuentras parado ahora mismo. |
| **Remote (remoto)** | Una versión del repositorio alojada en otra máquina o servicio (GitHub, GitLab, etc.). |

## Los tres estados de un archivo

```
Working Directory  --git add-->  Staging Area  --git commit-->  Repository (historial)
   (modificado)                    (preparado)                     (confirmado)
```

Entender este flujo de tres pasos es la base de todo lo demás en Git: casi cualquier duda ("¿por qué mi cambio no aparece en el commit?", "¿cómo deshago esto?") se resuelve identificando en cuál de estos tres estados está el cambio en cuestión.

---

**Siguiente:** [02_configuracion_inicial.md](02_configuracion_inicial.md)
