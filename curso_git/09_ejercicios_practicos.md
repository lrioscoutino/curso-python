# 9. Ejercicios prácticos

## Ejercicio 1 — Flujo completo básico

1. Crea un repositorio llamado `tienda-online`.
2. Añade archivos: `index.html`, `style.css`, `script.js`.
3. Haz commits individuales para cada archivo.
4. Crea una rama `mejoras-ui`.
5. Modifica `style.css` y haz commit.
6. Fusiona la rama en `main`.

**Solución:**

```bash
mkdir tienda-online && cd tienda-online
git init -b main

echo "<!DOCTYPE html>" > index.html
echo "<html><head><title>Tienda Online</title></head>" >> index.html
echo "<body><h1>Bienvenido a nuestra tienda</h1></body></html>" >> index.html

echo "body { font-family: Arial; }" > style.css
echo "h1 { color: blue; }" >> style.css

echo "console.log('Tienda online cargada');" > script.js

git add index.html
git commit -m "Añade estructura HTML básica"

git add style.css
git commit -m "Añade estilos CSS básicos"

git add script.js
git commit -m "Añade funcionalidad JavaScript"

git switch -c mejoras-ui
echo "h1 { color: #2c3e50; text-align: center; }" >> style.css
echo ".container { max-width: 1200px; margin: 0 auto; }" >> style.css
git add style.css
git commit -m "Mejora estilos de la interfaz de usuario"

git switch main
git merge mejoras-ui
git branch -d mejoras-ui

git log --oneline --graph
```

## Ejercicio 2 — Colaboración con un repositorio propio

> **Importante:** usa siempre un repositorio **que tú creaste** en GitHub — nunca uno de otra persona u organización. Intentar hacer `git push` a un repositorio que no controlas falla con `403 Permission denied`, sin importar qué tan correcto sea tu código.

1. Crea un repositorio nuevo y vacío en tu cuenta de GitHub.
2. Clónalo localmente.
3. Crea una rama con tu nombre y añade un archivo con información sobre ti.
4. Sube la rama a tu repositorio.
5. Simula un conflicto modificando el mismo archivo desde dos ramas distintas.

**Solución:**

```bash
# 1-2. Crear (en GitHub, vacío) y clonar TU PROPIO repositorio
git clone https://github.com/TU-USUARIO/mi-repo-practica.git
cd mi-repo-practica

# 3. Rama con tu nombre + archivo de perfil
git switch -c feature/juan-perez
cat > mi-perfil.md << 'EOF'
# Juan Pérez

## Información personal
- Nombre: Juan Pérez
- Rol: Desarrollador Frontend
- Tecnologías: JavaScript, React, Git
EOF
git add mi-perfil.md
git commit -m "Añade perfil de Juan Pérez"

# 4. Subir la rama a TU repositorio (donde sí tienes permiso de escritura)
git push -u origin feature/juan-perez

# 5. Simular conflicto: dos ramas que tocan la misma línea
git switch -c feature/contacto-email
echo "Contacto: juan@ejemplo.com" >> mi-perfil.md
git add mi-perfil.md
git commit -m "Añade email de contacto"

git switch feature/juan-perez
git switch -c feature/contacto-telefono
echo "Contacto: +1234567890" >> mi-perfil.md
git add mi-perfil.md
git commit -m "Añade teléfono de contacto"

git switch feature/juan-perez
git merge feature/contacto-email --no-edit          # este se completa sin problema
git merge feature/contacto-telefono --no-edit        # este genera conflicto (misma línea "Contacto:")

# Resolver editando mi-perfil.md a mano, luego:
git add mi-perfil.md
git commit -m "Resuelve conflicto de información de contacto"
```

## Ejercicio 3 — Historial y navegación

1. Crea un proyecto con al menos 10 commits.
2. Usa `git log` con diferentes opciones para explorar el historial.
3. Navega a un commit anterior.
4. Crea una rama desde un commit específico.
5. Experimenta con `git diff` entre distintos commits.

**Solución:**

```bash
mkdir proyecto-historial && cd proyecto-historial
git init -b main

echo "# Proyecto de Historial" > README.md
git add README.md
git commit -m "Commit 1: Añade README inicial"

mkdir src
echo "console.log('Hola mundo');" > src/main.js
git add src/main.js
git commit -m "Commit 2: Añade archivo principal"

echo "function saludar() { return 'Hola'; }" >> src/main.js
git add src/main.js
git commit -m "Commit 3: Añade función saludar"

echo "body { margin: 0; }" > src/styles.css
git add src/styles.css
git commit -m "Commit 4: Añade estilos CSS"

echo "## Instalación" >> README.md
git add README.md
git commit -m "Commit 5: Actualiza documentación"

mkdir tests
echo "// Tests placeholder" > tests/main.test.js
git add tests/main.test.js
git commit -m "Commit 6: Añade estructura de tests"

echo "function despedir() { return 'Adiós'; }" >> src/main.js
git add src/main.js
git commit -m "Commit 7: Añade función despedir"

echo ".container { width: 100%; }" >> src/styles.css
git add src/styles.css
git commit -m "Commit 8: Mejora estilos CSS"

echo "## Uso" >> README.md
git add README.md
git commit -m "Commit 9: Añade sección de uso"

echo "module.exports = { saludar, despedir };" >> src/main.js
git add src/main.js
git commit -m "Commit 10: Añade exports"

# 2. Explorar el historial
git log --oneline
git log --graph --all
git log --author="Tu Nombre"
git log -p                       # con el diff completo de cada commit
git log --stat                    # con estadísticas de archivos cambiados

# 3. Navegar a un commit anterior (detached HEAD)
git checkout HEAD~5
git log --oneline -n 3
git switch main                    # volver

# 4. Crear una rama desde un commit específico (en un solo paso)
COMMIT_HASH=$(git log --oneline | sed -n '7p' | cut -d' ' -f1)
git switch -c rama-desde-commit7 "$COMMIT_HASH"
git log --oneline -n 3

# 5. Comparar commits con git diff
git switch main
git diff HEAD~3                    # working directory vs 3 commits atrás
git diff HEAD~5 HEAD~2               # entre dos commits específicos
git diff --stat HEAD~3                 # solo estadísticas
git diff --name-only HEAD~3              # solo nombres de archivos
```

## Ejercicio 4 — Recuperación de errores

1. Compara los tres modos de `git reset` (`--soft`, mixed, `--hard`) sobre el mismo punto de partida.
2. Practica `git revert` sobre un commit ya confirmado.
3. Simula una pérdida accidental y recupérala con `git reflog`.

**Solución:**

```bash
mkdir recuperacion-errores && cd recuperacion-errores
git init -b main

echo "v1" > archivo.txt
git add archivo.txt
git commit -m "Commit 1"

echo "v2" > archivo.txt
git add archivo.txt
git commit -m "Commit 2"

echo "v3" > archivo.txt
git add archivo.txt
git commit -m "Commit 3 (problemático)"

# --- Comparar los 3 modos de reset, cada uno en su propia rama desde el mismo punto ---

# A) --soft: deshace el commit, el cambio queda EN STAGING (listo para volver a commitear)
git switch -c demo-soft
git reset --soft HEAD~1
git status --short              # M  archivo.txt (con dos espacios: está en staging)
git log --oneline               # solo 2 commits — "Commit 3" desapareció del historial
git reset --hard -q             # limpiar antes de cambiar de rama

# B) mixed (el comportamiento por default de "git reset"): el cambio queda SIN preparar
git switch main
git switch -c demo-mixed
git reset HEAD~1
git status --short               #  M archivo.txt (un espacio: fuera de staging)
git log --oneline
git reset --hard -q

# C) --hard: el cambio se descarta por completo, sin rastro
git switch main
git switch -c demo-hard
git reset --hard HEAD~1
git status --short                # nada que mostrar — el cambio se perdió
git log --oneline

# --- Revert: la forma segura de deshacer un commit YA COMPARTIDO ---
git switch main
git revert HEAD --no-edit          # revierte "Commit 3" con un commit NUEVO
git log --oneline                  # "Commit 3" y su reversión AMBOS siguen visibles

# --- Simular pérdida accidental y recuperar con reflog ---
git reset --hard HEAD~1            # "perdemos" el commit de revert por accidente
git log --oneline                  # ya no se ve

git reflog                          # el historial de TODO lo que HEAD hizo, incluso lo "perdido"
LOST_COMMIT=$(git reflog | grep "Revert" | head -1 | cut -d' ' -f1)
git switch -c recuperado "$LOST_COMMIT"
git log --oneline -1                 # el commit "perdido" reaparece
```

> `git reflog` funciona porque Git no borra commits inmediatamente — los mantiene accesibles (por defecto ~90 días) hasta que el recolector de basura (`git gc`) los limpia. Mientras el hash siga en el reflog, el commit es recuperable.

### Comandos de recuperación útiles

```bash
git reflog show main             # reflog de una rama específica
git reflog --date=relative         # con fechas relativas ("hace 5 minutos")
git checkout HEAD~1 -- archivo.txt   # recuperar un archivo puntual de un commit anterior
git fsck --lost-found                  # encontrar commits "huérfanos" que ya no tiene ninguna rama
```

## Ejercicio 5 — Flujo de trabajo tipo Git Flow (introducción)

Este ejercicio da una primera pasada a Git Flow. Para la versión completa y ejecutable —incluyendo el punto más importante: por qué un hotfix debe nacer del tag de producción y no de `main`/`develop`— ver [git_avanzado/ejemplos/04_gitflow_demo.sh](../git_avanzado/ejemplos/04_gitflow_demo.sh) y la práctica guiada en [git_avanzado/practica_tutorial.md](../git_avanzado/practica_tutorial.md).

1. Crea `main` y `develop`.
2. Desarrolla una feature en su propia rama y intégrala a `develop`.
3. Prepara y cierra una release: fusiónala a `main` (taggeada) y de vuelta a `develop`.

**Solución:**

```bash
mkdir proyecto-gitflow && cd proyecto-gitflow
git init -b main

echo "# Proyecto Git Flow" > README.md
git add README.md
git commit -m "Commit inicial del proyecto"

git switch -c develop

# Feature: sistema de usuarios
git switch -c feature/sistema-usuarios
mkdir src
echo "class Usuario { constructor(nombre) { this.nombre = nombre; } }" > src/usuario.js
git add src/usuario.js
git commit -m "Añade clase Usuario"

git switch develop
git merge feature/sistema-usuarios --no-ff --no-edit
git branch -d feature/sistema-usuarios

# Release: preparar y cerrar
git switch -c release/v1.1.0
echo "1.1.0" > VERSION
git add VERSION
git commit -m "Prepara release v1.1.0"

git switch main
git merge release/v1.1.0 --no-ff --no-edit
git tag -a v1.1.0 -m "Release v1.1.0"

git switch develop
git merge release/v1.1.0 --no-ff --no-edit
git branch -d release/v1.1.0

git log --graph --all --oneline --decorate
git tag -l
```

---

**Anterior:** [08_buenas_practicas.md](08_buenas_practicas.md) · **Siguiente:** [10_referencia_rapida.md](10_referencia_rapida.md)
