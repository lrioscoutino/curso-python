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

### Ejercicio 2: Colaboración simulada
1. Clona un repositorio público de GitHub
2. Crea una rama con tu nombre
3. Añade un archivo con información sobre ti
4. Sube la rama al repositorio
5. Simula conflictos modificando el mismo archivo desde dos ramas

### Ejercicio 3: Historial y navegación
1. Crea un proyecto con al menos 10 commits
2. Usa `git log` con diferentes opciones para explorar el historial
3. Navega a commits anteriores con `git checkout`
4. Crea una rama desde un commit específico
5. Experimenta con `git diff` entre diferentes commits

### Ejercicio 4: Recuperación de errores
1. Haz cambios y commitéalos
2. Usa `git reset` para deshacer commits
3. Practica con `git revert` para revertir cambios
4. Simula pérdida de trabajo y recupéralo con `git reflog`

### Ejercicio 5: Flujo de trabajo avanzado
1. Implementa el flujo Git Flow en un proyecto
2. Crea ramas `feature`, `develop`, y `release`
3. Simula el desarrollo de múltiples características en paralelo
4. Practica hotfixes en producción
5. Documenta el proceso

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
