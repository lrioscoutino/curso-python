# 7. Resolución de conflictos

## ¿Qué son los conflictos?

Un conflicto ocurre cuando Git no puede fusionar automáticamente dos cambios porque ambas ramas modificaron las **mismas líneas** de un archivo (o una rama modificó un archivo que la otra eliminó). Git se detiene y te pide que decidas tú cuál versión — o combinación de ambas — es la correcta.

## Resolución manual

```bash
git status                         # ver qué archivos están en conflicto
# abrir y editar el/los archivo(s) manualmente
git add archivo-resuelto.txt       # marcar como resuelto
git commit                         # completar el merge (Git ya prepara el mensaje)
```

## Herramientas de merge

```bash
git config --global merge.tool vimdiff
git mergetool                      # abre una herramienta visual para resolver conflictos
```

## Práctica 6 — Provocar y resolver un conflicto real

1. Crea dos ramas que modifiquen la misma línea de un archivo.
2. Intenta fusionarlas para generar un conflicto.
3. Resuelve el conflicto manualmente.
4. Completa el merge.

**Solución:**

```bash
mkdir practica-conflictos && cd practica-conflictos
git init -b main
echo "Línea 1: Contenido original" > conflicto.txt
echo "Línea 2: Contenido base" >> conflicto.txt
echo "Línea 3: Final del archivo" >> conflicto.txt
git add conflicto.txt
git commit -m "Añade archivo base para conflicto"

# 1. Crear primera rama y modificar la misma línea
git switch -c rama-A
sed -i 's/Contenido base/Modificado en rama A/' conflicto.txt
git add conflicto.txt
git commit -m "Modifica línea 2 en rama A"

# Volver a main y crear segunda rama desde ahí (NO desde rama-A)
git switch main
git switch -c rama-B
sed -i 's/Contenido base/Modificado en rama B/' conflicto.txt
git add conflicto.txt
git commit -m "Modifica línea 2 en rama B"

# 2. Fusionar ambas en main
git switch main
git merge rama-A --no-edit     # este merge se completa sin problema
git merge rama-B --no-edit     # este SÍ genera conflicto — ambas tocaron la misma línea
```

En este punto Git detiene el merge y `conflicto.txt` contiene marcadores:

```
Línea 1: Contenido original
<<<<<<< HEAD
Línea 2: Modificado en rama A
=======
Línea 2: Modificado en rama B
>>>>>>> rama-B
Línea 3: Final del archivo
```

```bash
# 3. Ver el estado del conflicto
git status

# 4. Resolver manualmente: decide qué queda (aquí, combinamos ambas)
cat > conflicto.txt << 'EOF'
Línea 1: Contenido original
Línea 2: Contenido fusionado de ambas ramas
Línea 3: Final del archivo
EOF

# Marcar como resuelto y completar el merge
git add conflicto.txt
git commit -m "Resuelve conflicto entre rama-A y rama-B"

git log --oneline --graph
```

## Comandos útiles durante un conflicto

```bash
git status                 # qué archivos están en conflicto
git diff                    # ver los marcadores de conflicto

git merge --abort            # cancelar el merge por completo y volver al estado anterior

git show HEAD                  # tu versión (la rama en la que estás)
git show rama-B                  # la versión de la otra rama

git mergetool                      # herramienta visual de resolución
git diff --cached                    # ver qué quedó preparado tras resolver
```

`git merge --abort` es tu salida de emergencia: si te confundes a mitad de resolver un conflicto, esto te regresa exactamente al estado de antes de intentar el merge — no hay penalización por usarlo mientras el merge siga sin completarse (sin haber hecho `git commit` todavía).

---

**Anterior:** [06_comandos_intermedios.md](06_comandos_intermedios.md) · **Siguiente:** [08_buenas_practicas.md](08_buenas_practicas.md)
