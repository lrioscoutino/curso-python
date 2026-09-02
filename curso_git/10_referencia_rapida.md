# 10. Comandos de referencia rápida

## Configuración

```bash
git config --global user.name "Nombre"
git config --global user.email "email@ejemplo.com"
git config --global init.defaultBranch main
```

## Repositorios

```bash
git init -b main             # inicializar repositorio, rama principal "main"
git clone <url>                 # clonar repositorio
git remote add origin <url>       # añadir remoto
```

## Cambios básicos

```bash
git status                  # estado del repositorio
git add .                    # preparar todos los archivos
git commit -m "mensaje"       # confirmar cambios
git push                       # subir cambios
git pull                        # descargar cambios
```

## Ramas

```bash
git branch                  # listar ramas
git switch -c nueva          # crear y cambiar a una rama nueva
git merge rama                # fusionar una rama en la actual
git branch -d rama              # eliminar rama (si ya está fusionada)
```

## Historial

```bash
git log                     # ver historial
git log --oneline            # historial resumido
git log --graph --all         # con gráfico de todas las ramas
git diff                       # ver diferencias
```

## Deshacer cambios

```bash
git restore archivo             # descartar cambios no confirmados en un archivo
git restore --staged archivo     # quitar un archivo del staging area
git revert <commit>                # revertir un commit ya compartido (crea uno nuevo)
git reset --hard HEAD~1              # deshacer el último commit por completo (¡solo si es local!)
```

## Siguiente paso

Este curso cubre lo básico-intermedio. Para trabajar en equipo con confianza —commits atómicos, mensajes trackeables, elegir el flujo de ramas correcto, y manejar varios entornos de despliegue sin pisarse— continúa con [`git_avanzado`](../git_avanzado/README.md).

---

**Anterior:** [09_ejercicios_practicos.md](09_ejercicios_practicos.md)
