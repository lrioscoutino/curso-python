# 6. Comandos intermedios

## Descartar y deshacer cambios

```bash
# Comandos modernos (Git 2.23+), preferidos — separan "restaurar archivos" de "cambiar de rama":
git restore archivo.txt              # descarta cambios no confirmados en el working directory
git restore --staged archivo.txt     # quita un archivo del staging area (sin perder el cambio)

# Comandos clásicos equivalentes (siguen funcionando, verás muchos tutoriales que los usan):
git checkout -- archivo.txt          # equivalente a git restore
git reset HEAD archivo.txt           # equivalente a git restore --staged

# Deshacer commits:
git reset --soft HEAD~1              # deshace el último commit, mantiene los cambios EN STAGING
git reset HEAD~1                     # (mixed, el default) mantiene los cambios SIN preparar
git reset --hard HEAD~1              # deshace el commit Y descarta los cambios por completo
git revert <commit-hash>              # crea un commit NUEVO que revierte los cambios de otro
```

**`reset` vs `revert` — la diferencia que más importa:**

| | `git reset` | `git revert` |
|---|---|---|
| Qué hace | Mueve el puntero de la rama hacia atrás, reescribiendo el historial | Crea un commit nuevo que deshace los cambios, el historial avanza |
| ¿Seguro en una rama compartida? | No — si alguien más ya descargó esos commits, su repo queda desincronizado | Sí — es la forma correcta de "deshacer" algo que ya se compartió |
| Cuándo usarlo | Commits que **solo existen en tu copia local**, aún no compartidos | Commits que **ya se subieron** a un remoto compartido |

## Stash — guardar cambios temporalmente

```bash
git stash                          # guarda cambios sin confirmar y limpia el working directory
git stash pop                      # aplica el último stash guardado Y lo elimina de la lista
git stash apply                    # aplica el último stash pero lo CONSERVA en la lista
git stash list                     # ver todos los stashes guardados
git stash apply stash@{0}          # aplicar un stash específico por índice
git stash drop stash@{0}           # eliminar un stash específico
git stash -u                       # incluir también archivos nuevos (untracked) en el stash
```

Útil cuando necesitas cambiar de rama urgentemente pero tienes cambios sin terminar que no quieres commitear todavía.

## Rebase

```bash
git rebase main                    # reaplica los commits de tu rama actual sobre la punta de main
git rebase -i HEAD~3                # rebase interactivo: reordenar, combinar o editar los últimos 3 commits
```

> Igual que `reset`, `rebase` reescribe historial — nunca lo hagas sobre commits que ya subiste a una rama que otras personas usan (ver [git_avanzado/01_buenas_practicas_generales.md](../git_avanzado/01_buenas_practicas_generales.md) para la regla completa).

## Cherry-pick

```bash
git cherry-pick <commit-hash>      # aplica UN commit específico de otra rama a la rama actual
```

## Práctica 5 — Comandos intermedios (stash y revert)

Este ejercicio es autocontenido — no depende de repositorios de prácticas anteriores.

1. Crea un repo con un archivo y un commit inicial.
2. Haz algunos cambios sin commitear.
3. Usa `git stash` para guardarlos temporalmente.
4. Crea una rama, haz un commit ahí, y vuelve a la rama original.
5. Recupera los cambios guardados con `git stash pop`.
6. Confírmalos y practica revertir ese commit con `git revert`.

**Solución:**

```bash
mkdir practica-intermedios && cd practica-intermedios
git init -b main    # -b main asegura el nombre de la rama sin importar tu configuración
echo "console.log('hola');" > app.js
git add app.js
git commit -m "Commit inicial"

# 2. Cambios sin commitear
echo "console.log('cambio sin terminar');" >> app.js
git status

# 3. Guardar con stash
git stash
git status                    # el working directory vuelve a estar limpio

# 4. Cambiar de rama y volver
git switch -c rama-temporal
echo "Archivo en nueva rama" > temporal.txt
git add temporal.txt
git commit -m "Añade archivo temporal"
git switch main

# 5. Recuperar el stash
git stash pop
git status                    # el cambio sin terminar vuelve a aparecer
git diff

# 6. Commitear y luego revertir
git add app.js
git commit -m "Commit que será revertido"
git revert HEAD --no-edit      # --no-edit acepta el mensaje autogenerado sin abrir el editor
git log --oneline              # hay un commit nuevo "Revert ..." — el original sigue en el historial
```

### Comandos adicionales de stash

```bash
git stash list
git stash apply stash@{0}
git stash drop stash@{0}
git stash clear                # elimina TODOS los stashes guardados
```

---

**Anterior:** [05_trabajo_colaborativo.md](05_trabajo_colaborativo.md) · **Siguiente:** [07_resolucion_conflictos.md](07_resolucion_conflictos.md)
