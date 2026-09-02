#!/usr/bin/env bash
# 4. GitHub Flow — demo ejecutable
#
# Simula el flujo completo: main siempre desplegable, una rama de
# feature nace de main, se integra vía "Pull Request" (aquí un merge
# --no-ff que dispararía CI/CD en la vida real) y se elimina.
#
# Uso: bash 03_github_flow_demo.sh

set -euo pipefail

REPO_DIR="$(mktemp -d -t git-demo-githubflow-XXXX)"
cd "$REPO_DIR"

git init -q -b main
git config user.name "Demo"
git config user.email "demo@example.com"

echo "=== Repo temporal creado en: $REPO_DIR ==="
echo ""

echo "# Mi App" > README.md
git add README.md
git commit -q -m "chore: inicializa el proyecto"
echo "--- main: siempre desplegable desde el primer commit ---"

# --- Feature 1: nace de main, vive poco tiempo ---
git switch -c feature/PROJ-101-pagina-bienvenida
echo "<h1>Bienvenido</h1>" > index.html
git add index.html
git commit -q -m "feat(home): agrega página de bienvenida"
echo "--- Rama feature/PROJ-101-pagina-bienvenida lista, 'abre PR' ---"

# --- "Merge del PR" — --no-ff conserva el hecho de que fue una feature ---
git switch main
git merge --no-ff -q feature/PROJ-101-pagina-bienvenida -m "merge: integra feature/PROJ-101-pagina-bienvenida"
git branch -d feature/PROJ-101-pagina-bienvenida
echo "--- 'PR' fusionado a main -> esto dispararía el despliegue automático ---"

# --- Feature 2, en paralelo con lo que ya está en main ---
git switch -c feature/PROJ-102-footer
echo "<footer>© 2026</footer>" >> index.html
git add index.html
git commit -q -m "feat(footer): agrega pie de página"

git switch main
git merge --no-ff -q feature/PROJ-102-footer -m "merge: integra feature/PROJ-102-footer"
git branch -d feature/PROJ-102-footer
echo "--- Segundo 'PR' fusionado -> segundo despliegue automático ---"

echo ""
echo "=== Topología resultante (nótese: sin ramas de larga duración) ==="
git log --graph --oneline --all

echo ""
echo "Repo de ejemplo en: $REPO_DIR (bórralo con 'rm -rf $REPO_DIR' cuando termines)"
