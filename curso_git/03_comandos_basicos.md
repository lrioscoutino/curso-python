# 3. Comandos básicos

## Inicializar un repositorio

```bash
git init
```

Crea un nuevo repositorio Git en el directorio actual (agrega una carpeta oculta `.git/`).

## Clonar un repositorio

```bash
git clone <url-del-repositorio>
git clone https://github.com/usuario/proyecto.git
```

## Ver el estado del repositorio

```bash
git status
```

Muestra el estado de los archivos: modificados, preparados (staged), o sin rastrear (untracked).

## Añadir archivos al staging area

```bash
git add archivo.txt          # un archivo específico
git add .                    # todos los archivos del directorio actual
git add *.js                 # todos los archivos .js
git add -A                   # todos los cambios, incluyendo eliminaciones
```

## Confirmar cambios (commit)

```bash
git commit -m "Mensaje descriptivo del commit"
git commit -am "Mensaje"     # atajo: add de archivos ya rastreados + commit
```

> `-am` solo funciona con archivos que Git **ya conocía** (modificados). Un archivo nuevo (untracked) siempre necesita `git add` explícito primero.

## Ver historial de commits

```bash
git log
git log --oneline            # una línea por commit
git log --graph              # con representación gráfica de ramas
git log -n 5                 # últimos 5 commits
```

## Ver diferencias

```bash
git diff                     # cambios en el working directory, sin preparar
git diff --staged            # cambios ya preparados (staged), pendientes de commit
git diff HEAD~1              # comparar el working directory con el commit anterior
```

## Práctica 2 — Flujo básico

1. Crea un directorio llamado `mi-proyecto`.
2. Inicializa un repositorio Git.
3. Crea un archivo `README.md` con contenido.
4. Añádelo al staging area y haz tu primer commit.
5. Modifica el archivo y haz otro commit.
6. Revisa el historial con `git log`.

**Solución:**

```bash
mkdir mi-proyecto
cd mi-proyecto
git init

echo "# Mi Proyecto" > README.md
echo "Este es mi primer proyecto con Git" >> README.md

git add README.md
git commit -m "Añade README inicial"

echo "" >> README.md
echo "## Descripción" >> README.md
echo "Proyecto para aprender Git" >> README.md
git add README.md
git commit -m "Añade descripción al README"

git log
git log --oneline
```

---

**Anterior:** [02_configuracion_inicial.md](02_configuracion_inicial.md) · **Siguiente:** [04_ramas.md](04_ramas.md)
