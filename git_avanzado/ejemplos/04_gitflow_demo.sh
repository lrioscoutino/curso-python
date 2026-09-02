#!/usr/bin/env bash
# 4. Git Flow — demo ejecutable
#
# Simula el ciclo completo: main + develop, una feature, una release
# (con tag), y un hotfix que nace del tag de producción — NO de
# develop — para no arrastrar trabajo a medio terminar.
#
# Uso: bash 04_gitflow_demo.sh

set -euo pipefail

REPO_DIR="$(mktemp -d -t git-demo-gitflow-XXXX)"
cd "$REPO_DIR"

git init -q -b main
git config user.name "Demo"
git config user.email "demo@example.com"

echo "=== Repo temporal creado en: $REPO_DIR ==="
echo ""

echo "Version: 1.0.0" > VERSION
git add VERSION
git commit -q -m "chore: inicializa el proyecto"

git switch -c develop
echo "--- Rama develop creada desde main ---"

# --- Feature: exportar a PDF ---
git switch -c feature/exportar-pdf
echo "def exportar_pdf(): pass" > exportar.py
git add exportar.py
git commit -q -m "feat(reportes): agrega exportación a PDF"

git switch develop
git merge --no-ff -q feature/exportar-pdf -m "merge: integra feature/exportar-pdf a develop"
git branch -d feature/exportar-pdf
echo "--- Feature fusionada a develop ---"

# --- Release 1.1.0: se congela el alcance, se estabiliza ---
git switch -c release/1.1.0
echo "Version: 1.1.0" > VERSION
git add VERSION
git commit -q -m "chore(release): prepara 1.1.0"

# fix de última hora detectado durante estabilización
echo "def exportar_pdf(): return True" > exportar.py
git add exportar.py
git commit -q -m "fix(reportes): exportar_pdf ahora retorna estado de éxito"
echo "--- Release estabilizada con un fix de último momento ---"

# --- Cerrar la release: a main (con tag) y de vuelta a develop ---
git switch main
git merge --no-ff -q release/1.1.0 -m "merge: cierra release/1.1.0"
git tag -a v1.1.0 -m "Release 1.1.0: exportación a PDF"

git switch develop
git merge --no-ff -q release/1.1.0 -m "merge: trae release/1.1.0 de vuelta a develop"
git branch -d release/1.1.0
echo "--- Release 1.1.0 cerrada y taggeada, develop actualizado ---"

# --- Trabajo nuevo en develop que NO debe ir a producción todavía ---
git switch develop
echo "def nueva_feature_a_medias(): pass" > wip.py
git add wip.py
git commit -q -m "feat(wip): trabajo en progreso, no listo para producción"
echo "--- develop avanza con trabajo que NO debe salir aún ---"

# --- Bug crítico en producción: hotfix desde el TAG, no desde develop ---
git switch -c hotfix/prod-crash v1.1.0
echo "def exportar_pdf(): return True  # fix crash con PDFs vacios" > exportar.py
git add exportar.py
git commit -q -m "fix(reportes): corrige crash al exportar PDF vacío"
echo "Version: 1.1.1" > VERSION
git add VERSION
git commit -q -m "chore(release): prepara hotfix 1.1.1"

git switch main
git merge --no-ff -q hotfix/prod-crash -m "merge: aplica hotfix/prod-crash a main"
git tag -a v1.1.1 -m "Hotfix 1.1.1: corrige crash en exportación"

git switch develop
git merge --no-ff -q hotfix/prod-crash -m "merge: trae hotfix/prod-crash a develop"
git branch -d hotfix/prod-crash
echo "--- Hotfix aplicado a producción SIN arrastrar wip.py ---"

echo ""
echo "=== Verificación clave: wip.py NO está en el hotfix ni en main ==="
git show v1.1.1:. 2>/dev/null | grep -v wip.py || true
if git cat-file -e v1.1.1:wip.py 2>/dev/null; then
    echo "ERROR: wip.py se coló en el hotfix"
else
    echo "OK: wip.py no existe en el tag v1.1.1 (el hotfix nació del tag, no de develop)"
fi

echo ""
echo "=== Tags disponibles ==="
git tag -l

echo ""
echo "=== Topología completa ==="
git log --graph --oneline --all

echo ""
echo "Repo de ejemplo en: $REPO_DIR (bórralo con 'rm -rf $REPO_DIR' cuando termines)"
