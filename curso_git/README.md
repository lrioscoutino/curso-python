# Manual de Git: De Básico a Intermedio

## Tabla de Contenidos
1. [Introducción a Git](#introducción-a-git)
2. [Conceptos Fundamentales](#conceptos-fundamentales)
3. [Configuración Inicial](#configuración-inicial)
4. [Comandos Básicos](#comandos-básicos)
5. [Trabajo con Ramas (Branches)](#trabajo-con-ramas-branches)
6. [Trabajo Colaborativo](#trabajo-colaborativo)
7. [Comandos Intermedios](#comandos-intermedios)
8. [Resolución de Conflictos](#resolución-de-conflictos)
9. [Buenas Prácticas](#buenas-prácticas)
10. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción a Git

### ¿Qué es Git?
Git es un sistema de control de versiones distribuido que permite rastrear cambios en archivos y coordinar el trabajo entre múltiples desarrolladores. Fue creado por Linus Torvalds en 2005 para el desarrollo del kernel de Linux.

### Características principales:
- **Distribuido**: Cada desarrollador tiene una copia completa del historial del proyecto
- **Velocidad**: Operaciones locales rápidas
- **Integridad**: Verificación mediante checksums SHA-1
- **Soporte para desarrollo no lineal**: Ramas y fusiones eficientes

---

## Conceptos Fundamentales

### Repository (Repositorio)
Un repositorio es un directorio que contiene todos los archivos del proyecto y el historial completo de cambios.

### Working Directory (Directorio de Trabajo)
El directorio donde tienes los archivos del proyecto en tu sistema de archivos local.

### Staging Area (Área de Preparación)
Un área intermedia donde se preparan los cambios antes de confirmarlos. También conocida como "index".

### Commit
Una instantánea de los cambios en un momento específico. Cada commit tiene un identificador único (hash SHA-1).

### Branch (Rama)
Una línea de desarrollo independiente. La rama principal se llama `main` o `master`.

### HEAD
Un puntero que indica el commit actual en el que te encuentras.

### Remote (Remoto)
Una versión del repositorio alojada en internet o red, como GitHub, GitLab, etc.

---

## Configuración Inicial

### Configuración de identidad
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

### Configuración del editor
```bash
git config --global core.editor "code --wait"  # Para VS Code
git config --global core.editor "vim"          # Para Vim
```

### Verificar configuración
```bash
git config --list
git config user.name
git config user.email
```

### **Práctica 1: Configuración inicial**
1. Configura tu nombre y email globalmente
2. Establece tu editor preferido
3. Verifica que la configuración se aplicó correctamente

#### **Solución:**
```bash
# 1. Configurar nombre y email globalmente
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

# 2. Establecer editor preferido (ejemplo con VS Code)
git config --global core.editor "code --wait"

# 3. Verificar configuración
git config --list
git config user.name
git config user.email
```

---

## Comandos Básicos

### Inicializar un repositorio
```bash
git init
```
Crea un nuevo repositorio Git en el directorio actual.

### Clonar un repositorio
```bash
git clone <url-del-repositorio>
git clone https://github.com/usuario/proyecto.git
```

### Ver el estado del repositorio
```bash
git status
```
Muestra el estado de los archivos (modificados, preparados, no rastreados).

### Añadir archivos al staging area
```bash
git add archivo.txt          # Añadir un archivo específico
git add .                    # Añadir todos los archivos
git add *.js                 # Añadir todos los archivos .js
git add -A                   # Añadir todos los cambios (incluyendo eliminaciones)
```

### Confirmar cambios (commit)
```bash
git commit -m "Mensaje descriptivo del commit"
git commit -am "Añadir y commitear archivos modificados"  # Atajo para add + commit
```

### Ver historial de commits
```bash
git log
git log --oneline            # Versión resumida
git log --graph              # Con representación gráfica
git log -n 5                 # Últimos 5 commits
```

### Ver diferencias
```bash
git diff                     # Cambios no preparados
git diff --staged            # Cambios preparados
git diff HEAD~1              # Comparar con el commit anterior
```

### **Práctica 2: Flujo básico**
1. Crea un directorio llamado `mi-proyecto`
2. Inicializa un repositorio Git
3. Crea un archivo `README.md` con contenido
4. Añádelo al staging area y haz tu primer commit
5. Modifica el archivo y haz otro commit
6. Revisa el historial con `git log`

#### **Solución:**
```bash
# 1. Crear directorio
mkdir mi-proyecto
cd mi-proyecto

# 2. Inicializar repositorio Git
git init

# 3. Crear archivo README.md con contenido
echo "# Mi Proyecto" > README.md
echo "Este es mi primer proyecto con Git" >> README.md

# 4. Añadir al staging area y hacer primer commit
git add README.md
git commit -m "Añade README inicial"

# 5. Modificar el archivo y hacer otro commit
echo "" >> README.md
echo "## Descripción" >> README.md
echo "Proyecto para aprender Git" >> README.md
git add README.md
git commit -m "Añade descripción al README"

# 6. Revisar historial
git log
git log --oneline
```

---

## Trabajo con Ramas (Branches)

### ¿Por qué usar ramas?
- Desarrollo de características en paralelo
- Experimentación sin afectar el código principal
- Colaboración organizada
- Aislamiento de cambios

### Comandos de ramas
```bash
git branch                   # Listar ramas locales
git branch -a                # Listar todas las ramas (locales y remotas)
git branch nueva-rama        # Crear nueva rama
git checkout nueva-rama      # Cambiar a una rama
git checkout -b nueva-rama   # Crear y cambiar a nueva rama
git switch nueva-rama        # Cambiar de rama (comando moderno)
git switch -c nueva-rama     # Crear y cambiar (comando moderno)
```

### Fusionar ramas (merge)
```bash
git checkout main
git merge nueva-rama         # Fusiona nueva-rama en main
```

### Eliminar ramas
```bash
git branch -d rama-terminada    # Eliminar rama local (seguro)
git branch -D rama-terminada    # Eliminar rama local (forzado)
git push origin --delete rama   # Eliminar rama remota
```

### **Práctica 3: Trabajo con ramas**
1. Crea una nueva rama llamada `feature-login`
2. Cambia a esa rama y crea un archivo `login.js`
3. Haz commit de los cambios
4. Vuelve a la rama `main`
5. Fusiona la rama `feature-login`
6. Elimina la rama `feature-login`

#### **Solución:**
```bash
# 1. Crear nueva rama
git branch feature-login

# 2. Cambiar a la rama y crear archivo
git checkout feature-login
# O usando el comando moderno: git switch feature-login

# Crear archivo login.js
echo "function login() {" > login.js
echo "  console.log('Función de login');" >> login.js
echo "}" >> login.js

# 3. Hacer commit de los cambios
git add login.js
git commit -m "Añade función de login"

# 4. Volver a la rama main
git checkout main
# O usando: git switch main

# 5. Fusionar la rama feature-login
git merge feature-login

# 6. Eliminar la rama feature-login
git branch -d feature-login

# Verificar que la fusión fue exitosa
git log --oneline
```

---

## Trabajo Colaborativo

### Repositorios remotos
```bash
git remote -v                      # Ver repositorios remotos
git remote add origin <url>        # Añadir repositorio remoto
git remote remove origin           # Eliminar repositorio remoto
```

### Subir cambios (push)
```bash
git push origin main               # Subir rama main al remoto
git push -u origin nueva-rama      # Subir y trackear nueva rama
git push --all                     # Subir todas las ramas
```

### Descargar cambios (pull/fetch)
```bash
git fetch                          # Descargar cambios sin fusionar
git pull                           # Descargar y fusionar cambios
git pull origin main               # Pull específico de una rama
```

### **Práctica 4: Trabajo remoto**
1. Crea un repositorio en GitHub
2. Conecta tu repositorio local con el remoto
3. Sube tu código con `git push`
4. Haz cambios desde GitHub (edita un archivo)
5. Descarga los cambios con `git pull`

#### **Solución:**
```bash
# 1. Crear repositorio en GitHub
# Esto se hace desde la interfaz web de GitHub
# Crear nuevo repositorio -> Nombre: mi-proyecto-remoto

# 2. Conectar repositorio local con el remoto
git remote add origin https://github.com/tu-usuario/mi-proyecto-remoto.git

# Verificar conexión remota
git remote -v

# 3. Subir código al repositorio remoto
git push -u origin main
# El flag -u establece tracking entre la rama local y remota

# 4. Hacer cambios desde GitHub
# Ir a GitHub -> Editar README.md -> Añadir contenido -> Commit changes

# 5. Descargar cambios con git pull
git pull origin main
# O simplemente: git pull (si ya hay tracking establecido)

# Verificar que los cambios se descargaron
git log --oneline
```

#### **Comandos adicionales útiles:**
```bash
# Ver estado de ramas remotas
git branch -a

# Obtener información sin fusionar
git fetch origin

# Ver diferencias con remoto
git diff origin/main

# Subir rama específica
git push origin nombre-rama
```

---

## Comandos Intermedios

### Revertir cambios
```bash
git checkout -- archivo.txt       # Descartar cambios no confirmados
git reset HEAD archivo.txt        # Quitar archivo del staging area
git reset --soft HEAD~1           # Deshacer último commit (mantener cambios)
git reset --hard HEAD~1           # Deshacer último commit (eliminar cambios)
git revert <commit-hash>           # Crear commit que revierte cambios
```

### Stash (guardar cambios temporalmente)
```bash
git stash                          # Guardar cambios temporalmente
git stash pop                      # Aplicar último stash y eliminarlo
git stash list                     # Ver lista de stashes
git stash apply stash@{0}          # Aplicar stash específico
git stash drop stash@{0}           # Eliminar stash específico
```

### Rebase
```bash
git rebase main                    # Rebase rama actual sobre main
git rebase -i HEAD~3               # Rebase interactivo (últimos 3 commits)
```

### Cherry-pick
```bash
git cherry-pick <commit-hash>      # Aplicar commit específico a rama actual
```

### **Práctica 5: Comandos intermedios**
1. Haz algunos cambios sin commitear
2. Usa `git stash` para guardarlos temporalmente
3. Cambia de rama y vuelve
4. Recupera los cambios con `git stash pop`
5. Practica revertir un commit con `git revert`

#### **Solución:**
```bash
# 1. Hacer algunos cambios sin commitear
echo "Cambios temporales" >> README.md
echo "console.log('temporal');" >> login.js

# Verificar estado
git status

# 2. Usar git stash para guardar cambios temporalmente
git stash
# O con mensaje descriptivo: git stash save "Cambios temporales en progreso"

# Verificar que el directorio está limpio
git status

# 3. Cambiar de rama y volver
git checkout -b rama-temporal
echo "Archivo en nueva rama" > temporal.txt
git add temporal.txt
git commit -m "Añade archivo temporal"

# Volver a la rama principal
git checkout main

# 4. Recuperar cambios con git stash pop
git stash pop

# Verificar que los cambios volvieron
git status
git diff

# 5. Hacer commit de los cambios y luego revertirlo
git add .
git commit -m "Commit que será revertido"

# Revertir el último commit
git revert HEAD
# Esto abrirá un editor para el mensaje del commit de reversión
```

#### **Comandos adicionales de stash:**
```bash
# Ver lista de stashes
git stash list

# Aplicar stash específico sin eliminarlo
git stash apply stash@{0}

# Eliminar stash específico
git stash drop stash@{0}

# Limpiar todos los stashes
git stash clear

# Crear stash incluyendo archivos no rastreados
git stash -u
```

---

## Resolución de Conflictos

### ¿Qué son los conflictos?
Los conflictos ocurren cuando Git no puede fusionar automáticamente cambios porque dos ramas han modificado las mismas líneas de un archivo.

### Resolución manual
```bash
# Durante un merge con conflictos
git status                         # Ver archivos en conflicto
# Editar archivos manualmente
git add archivo-resuelto.txt       # Marcar como resuelto
git commit                         # Completar el merge
```

### Herramientas de merge
```bash
git config --global merge.tool vimdiff
git mergetool                      # Abrir herramienta de merge
```

### **Práctica 6: Conflictos**
1. Crea dos ramas que modifiquen la misma línea de un archivo
2. Intenta fusionarlas para generar un conflicto
3. Resuelve el conflicto manualmente
4. Completa el merge

#### **Solución:**
```bash
# Preparación: Crear archivo base
echo "Línea 1: Contenido original" > conflicto.txt
echo "Línea 2: Contenido base" >> conflicto.txt
echo "Línea 3: Final del archivo" >> conflicto.txt
git add conflicto.txt
git commit -m "Añade archivo base para conflicto"

# 1. Crear primera rama y modificar
git checkout -b rama-A
sed -i 's/Contenido base/Modificado en rama A/' conflicto.txt
git add conflicto.txt
git commit -m "Modifica línea 2 en rama A"

# Volver a main y crear segunda rama
git checkout main
git checkout -b rama-B
sed -i 's/Contenido base/Modificado en rama B/' conflicto.txt
git add conflicto.txt
git commit -m "Modifica línea 2 en rama B"

# 2. Intentar fusionar para generar conflicto
git checkout main
git merge rama-A    # Este merge será exitoso
git merge rama-B    # Este generará conflicto

# 3. Ver el estado del conflicto
git status

# 4. Resolver conflicto manualmente
# El archivo tendrá marcadores como:
# <<<<<<< HEAD
# Contenido de rama A
# =======
# Contenido de rama B
# >>>>>>> rama-B

# Editar el archivo para resolverlo:
echo "Línea 1: Contenido original" > conflicto.txt
echo "Línea 2: Contenido fusionado de ambas ramas" >> conflicto.txt
echo "Línea 3: Final del archivo" >> conflicto.txt

# Marcar como resuelto y completar merge
git add conflicto.txt
git commit -m "Resuelve conflicto entre rama-A y rama-B"

# Verificar resultado
git log --oneline --graph
```

#### **Comandos útiles para conflictos:**
```bash
# Ver archivos en conflicto
git status
git diff

# Abortar merge si es necesario
git merge --abort

# Ver diferencias de cada rama
git show HEAD        # Versión actual
git show rama-B      # Versión de la otra rama

# Usar herramienta visual para resolver conflictos
git mergetool

# Ver estado después de resolver
git diff --cached
```

---

## Buenas Prácticas

### Mensajes de commit
- Usa imperativo: "Añade" en lugar de "Añadido"
- Primera línea máximo 50 caracteres
- Deja línea en blanco antes de descripción detallada
- Explica el "qué" y "por qué", no el "cómo"

```bash
# Buen ejemplo
git commit -m "Añade validación de email en formulario de registro

Implementa validación tanto en frontend como backend
para prevenir emails inválidos en la base de datos."
```

### Estructura de ramas
- `main/master`: Código de producción
- `develop`: Rama de desarrollo principal
- `feature/nombre`: Nuevas características
- `hotfix/nombre`: Correcciones urgentes
- `release/version`: Preparación de releases

### Comandos útiles para limpieza
```bash
git branch --merged                # Ver ramas ya fusionadas
git remote prune origin            # Limpiar referencias remotas obsoletas
git gc                             # Garbage collection
```

---

## Ejercicios Prácticos

### Ejercicio 1: Flujo completo básico
1. Crea un repositorio llamado `tienda-online`
2. Añade archivos: `index.html`, `style.css`, `script.js`
3. Haz commits individuales para cada archivo
4. Crea una rama `mejoras-ui`
5. Modifica `style.css` y haz commit
6. Fusiona la rama en `main`

#### **Solución:**
```bash
# 1. Crear repositorio
mkdir tienda-online
cd tienda-online
git init

# 2. Crear archivos base
echo "<!DOCTYPE html>" > index.html
echo "<html><head><title>Tienda Online</title></head>" >> index.html
echo "<body><h1>Bienvenido a nuestra tienda</h1></body></html>" >> index.html

echo "body { font-family: Arial; }" > style.css
echo "h1 { color: blue; }" >> style.css

echo "console.log('Tienda online cargada');" > script.js
echo "document.addEventListener('DOMContentLoaded', function() {" >> script.js
echo "  console.log('DOM cargado');" >> script.js
echo "});" >> script.js

# 3. Commits individuales
git add index.html
git commit -m "Añade estructura HTML básica"

git add style.css
git commit -m "Añade estilos CSS básicos"

git add script.js
git commit -m "Añade funcionalidad JavaScript"

# 4. Crear rama mejoras-ui
git checkout -b mejoras-ui

# 5. Modificar style.css
echo "h1 { color: #2c3e50; text-align: center; }" >> style.css
echo ".container { max-width: 1200px; margin: 0 auto; }" >> style.css
git add style.css
git commit -m "Mejora estilos de la interfaz de usuario"

# 6. Fusionar en main
git checkout main
git merge mejoras-ui
git branch -d mejoras-ui

# Verificar resultado
git log --oneline --graph
```

### Ejercicio 2: Colaboración simulada
1. Clona un repositorio público de GitHub
2. Crea una rama con tu nombre
3. Añade un archivo con información sobre ti
4. Sube la rama al repositorio
5. Simula conflictos modificando el mismo archivo desde dos ramas

#### **Solución:**
```bash
# 1. Clonar repositorio público (ejemplo)
git clone https://github.com/octocat/Hello-World.git
cd Hello-World

# 2. Crear rama con tu nombre
git checkout -b feature/juan-perez

# 3. Añadir archivo con información personal
cat > mi-perfil.md << 'EOF'
# Juan Pérez

## Información Personal
- **Nombre**: Juan Pérez
- **Rol**: Desarrollador Frontend
- **Experiencia**: 3 años
- **Tecnologías**: JavaScript, React, Git

## Objetivos
- Mejorar conocimientos en Git
- Colaborar en proyectos open source
- Aprender nuevas tecnologías
EOF

git add mi-perfil.md
git commit -m "Añade perfil de Juan Pérez"

# 4. Subir rama al repositorio
git push -u origin feature/juan-perez

# 5. Simular conflictos
# Crear primera rama de feature
git checkout -b feature/contacto-email
echo "Email: juan@ejemplo.com" >> mi-perfil.md
git add mi-perfil.md
git commit -m "Añade email de contacto"

# Volver y crear segunda rama
git checkout feature/juan-perez
git checkout -b feature/contacto-telefono
echo "Teléfono: +1234567890" >> mi-perfil.md
git add mi-perfil.md
git commit -m "Añade teléfono de contacto"

# Fusionar primera rama
git checkout feature/juan-perez
git merge feature/contacto-email

# Intentar fusionar segunda (generará conflicto)
git merge feature/contacto-telefono

# Resolver conflicto editando el archivo
# Luego:
git add mi-perfil.md
git commit -m "Resuelve conflicto de información de contacto"
```

### Ejercicio 3: Historial y navegación
1. Crea un proyecto con al menos 10 commits
2. Usa `git log` con diferentes opciones para explorar el historial
3. Navega a commits anteriores con `git checkout`
4. Crea una rama desde un commit específico
5. Experimenta con `git diff` entre diferentes commits

#### **Solución:**
```bash
# 1. Crear proyecto con 10 commits
mkdir proyecto-historial
cd proyecto-historial
git init

# Crear commits graduales
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

# 2. Explorar historial con diferentes opciones
git log                           # Historial completo
git log --oneline                # Versión condensada
git log --graph --all             # Con gráfico de ramas
git log --since="1 hour ago"      # Commits recientes
git log --author="Tu Nombre"      # Por autor
git log -p                        # Con diferencias
git log --stat                    # Con estadísticas

# 3. Navegar a commits anteriores
git log --oneline                 # Ver lista de commits
git checkout HEAD~5               # Ir 5 commits atrás
git log --oneline -n 3            # Ver dónde estamos
git checkout main                 # Volver a main

# 4. Crear rama desde commit específico
COMMIT_HASH=$(git log --oneline | sed -n '7p' | cut -d' ' -f1)
git checkout $COMMIT_HASH
git checkout -b rama-desde-commit7
git log --oneline -n 3

# 5. Experimentar con git diff
git checkout main
git diff HEAD~3                   # Diferencias con 3 commits atrás
git diff HEAD~5 HEAD~2            # Entre dos commits específicos
git diff $COMMIT_HASH main        # Entre commit específico y main
git diff --stat HEAD~3            # Solo estadísticas
git diff --name-only HEAD~3       # Solo nombres de archivos
```

### Ejercicio 4: Recuperación de errores
1. Haz cambios y commitéalos
2. Usa `git reset` para deshacer commits
3. Practica con `git revert` para revertir cambios
4. Simula pérdida de trabajo y recupéralo con `git reflog`

#### **Solución:**
```bash
# Preparación: crear repositorio de prueba
mkdir recuperacion-errores
cd recuperacion-errores
git init

# Crear commits base
echo "Archivo original" > archivo.txt
git add archivo.txt
git commit -m "Commit inicial"

echo "Línea 2" >> archivo.txt
git add archivo.txt
git commit -m "Añade línea 2"

echo "Línea 3" >> archivo.txt
git add archivo.txt
git commit -m "Añade línea 3"

# 1. Hacer cambios y commitearlos
echo "Cambio problemático" >> archivo.txt
git add archivo.txt
git commit -m "Commit problemático que queremos deshacer"

echo "Otro cambio" >> archivo.txt
git add archivo.txt
git commit -m "Otro commit"

# Ver historial antes de deshacer
git log --oneline

# 2. Usar git reset para deshacer commits
# Opción 1: Reset soft (mantiene cambios en staging)
git reset --soft HEAD~1
git status                    # Ver que los cambios están en staging

# Opción 2: Reset mixed (default, mantiene cambios en working directory)
git commit -m "Rehacer último commit"
git reset HEAD~1
git status                    # Ver que los cambios están sin preparar

# Opción 3: Reset hard (elimina todos los cambios)
git add archivo.txt
git commit -m "Commit temporal"
git reset --hard HEAD~2       # Elimina últimos 2 commits completamente
git log --oneline

# 3. Practicar con git revert
echo "Cambio que revertiremos" >> archivo.txt
git add archivo.txt
git commit -m "Commit para revertir"

# Revertir el último commit (crea nuevo commit de reversión)
git revert HEAD
git log --oneline             # Ver que hay un commit de revert

# 4. Simular pérdida y recuperación con git reflog
# Simular pérdida accidental
git reset --hard HEAD~3       # "Perder" varios commits

# Ver que los commits parecen perdidos
git log --oneline

# Usar reflog para recuperar
git reflog                    # Ver historial de referencias
# Buscar el hash del commit que queremos recuperar

# Recuperar commit "perdido" (usar hash del reflog)
LOST_COMMIT=$(git reflog | grep "Commit para revertir" | cut -d' ' -f1)
git checkout $LOST_COMMIT
git checkout -b recuperacion
git log --oneline

# Opcional: fusionar recuperación con main
git checkout main
git merge recuperacion
```

#### **Comandos de recuperación útiles:**
```bash
# Ver reflog de una rama específica
git reflog show main

# Reflog con fechas
git reflog --date=relative

# Recuperar archivo específico de commit anterior
git checkout HEAD~1 -- archivo.txt

# Ver commits "huérfanos" (dangling)
git fsck --lost-found
```

### Ejercicio 5: Flujo de trabajo avanzado
1. Implementa el flujo Git Flow en un proyecto
2. Crea ramas `feature`, `develop`, y `release`
3. Simula el desarrollo de múltiples características en paralelo
4. Practica hotfixes en producción
5. Documenta el proceso

#### **Solución:**
```bash
# Preparación: crear proyecto para Git Flow
mkdir proyecto-gitflow
cd proyecto-gitflow
git init

# Setup inicial con main y develop
echo "# Proyecto Git Flow" > README.md
echo "Versión: 1.0.0" > VERSION
git add .
git commit -m "Commit inicial del proyecto"

# 1. Crear rama develop (rama principal de desarrollo)
git checkout -b develop
echo "## Desarrollo" >> README.md
git add README.md
git commit -m "Configura rama develop"

# 2. Desarrollar múltiples features en paralelo
# Feature 1: Sistema de usuarios
git checkout -b feature/sistema-usuarios
mkdir src
echo "class Usuario {" > src/usuario.js
echo "  constructor(nombre) { this.nombre = nombre; }" >> src/usuario.js
echo "}" >> src/usuario.js
git add src/usuario.js
git commit -m "Añade clase Usuario"

echo "  login() { return 'Logueado'; }" >> src/usuario.js
git add src/usuario.js
git commit -m "Añade método login a Usuario"

# Fusionar feature en develop
git checkout develop
git merge feature/sistema-usuarios --no-ff
git branch -d feature/sistema-usuarios

# Feature 2: Sistema de productos (en paralelo)
git checkout -b feature/sistema-productos
echo "class Producto {" > src/producto.js
echo "  constructor(nombre, precio) {" >> src/producto.js
echo "    this.nombre = nombre;" >> src/producto.js
echo "    this.precio = precio;" >> src/producto.js
echo "  }" >> src/producto.js
echo "}" >> src/producto.js
git add src/producto.js
git commit -m "Añade clase Producto"

git checkout develop
git merge feature/sistema-productos --no-ff
git branch -d feature/sistema-productos

# 3. Crear release
git checkout -b release/v1.1.0
echo "Versión: 1.1.0" > VERSION
echo "## Changelog v1.1.0" >> CHANGELOG.md
echo "- Añade sistema de usuarios" >> CHANGELOG.md
echo "- Añade sistema de productos" >> CHANGELOG.md
git add VERSION CHANGELOG.md
git commit -m "Prepara release v1.1.0"

# Finalizar release
git checkout main
git merge release/v1.1.0 --no-ff
git tag -a v1.1.0 -m "Release v1.1.0"

git checkout develop
git merge release/v1.1.0 --no-ff
git branch -d release/v1.1.0

# 4. Simular hotfix en producción
git checkout main
git checkout -b hotfix/correccion-critica
echo "  logout() { return 'Deslogueado'; }" >> src/usuario.js
git add src/usuario.js
git commit -m "Corrige bug crítico en Usuario"

echo "Versión: 1.1.1" > VERSION
git add VERSION
git commit -m "Bump version para hotfix"

# Fusionar hotfix
git checkout main
git merge hotfix/correccion-critica --no-ff
git tag -a v1.1.1 -m "Hotfix v1.1.1"

git checkout develop
git merge hotfix/correccion-critica --no-ff
git branch -d hotfix/correccion-critica

# Ver el resultado
git log --graph --all --oneline --decorate
```

#### **Documentación del proceso Git Flow:**
```markdown
# Git Flow Workflow

## Ramas principales:
- **main**: Código de producción estable
- **develop**: Rama de integración para desarrollo

## Ramas de soporte:
- **feature/***: Nuevas características
- **release/***: Preparación de nuevas versiones
- **hotfix/***: Correcciones urgentes de producción

## Flujo típico:
1. Crear feature desde develop
2. Desarrollar y hacer commits en feature
3. Fusionar feature en develop
4. Crear release desde develop
5. Finalizar release fusionando en main y develop
6. Crear hotfix desde main cuando sea necesario
7. Fusionar hotfix en main y develop
```

#### **Comandos Git Flow útiles:**
```bash
# Ver todas las ramas
git branch -a

# Ver gráfico del historial
git log --graph --oneline --all

# Ver tags
git tag -l

# Eliminar ramas remotas
git push origin --delete feature/nombre-rama
```

---

## Comandos de Referencia Rápida

### Configuración
```bash
git config --global user.name "Nombre"
git config --global user.email "email@ejemplo.com"
```

### Repositorios
```bash
git init                    # Inicializar repositorio
git clone <url>             # Clonar repositorio
git remote add origin <url> # Añadir remoto
```

### Cambios básicos
```bash
git status                  # Estado del repositorio
git add .                   # Añadir todos los archivos
git commit -m "mensaje"     # Confirmar cambios
git push                    # Subir cambios
git pull                    # Descargar cambios
```

### Ramas
```bash
git branch                  # Listar ramas
git checkout -b nueva       # Crear y cambiar rama
git merge rama              # Fusionar rama
git branch -d rama          # Eliminar rama
```

### Historial
```bash
git log                     # Ver historial
git log --oneline           # Historial resumido
git diff                    # Ver diferencias
```

### Deshacer cambios
```bash
git checkout -- archivo    # Descartar cambios
git reset HEAD archivo     # Quitar del staging
git revert <commit>         # Revertir commit
```

---
