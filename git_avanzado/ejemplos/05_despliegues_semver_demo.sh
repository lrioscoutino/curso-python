#!/usr/bin/env bash
# 6. Múltiples despliegues — demo ejecutable
#
# Simula dos versiones en soporte simultáneo (v1.x y v2.x en main) y
# usa cherry-pick para backportear un fix de seguridad a v1.x sin
# traer nada del desarrollo de v2.x.
#
# Uso: bash 05_despliegues_semver_demo.sh

set -euo pipefail

REPO_DIR="$(mktemp -d -t git-demo-despliegues-XXXX)"
cd "$REPO_DIR"

git init -q -b main
git config user.name "Demo"
git config user.email "demo@example.com"

echo "=== Repo temporal creado en: $REPO_DIR ==="
echo ""

echo "def login(): pass" > auth.py
git add auth.py
git commit -q -m "feat(auth): agrega login inicial"

echo "def logout(): pass" >> auth.py
git add auth.py
git commit -q -m "feat(auth): agrega logout"

git tag -a v1.0.0 -m "Release 1.0.0"
echo "--- v1.0.0 taggeada — esto es lo que se despliega a producción ---"

# --- Rama de soporte para la versión 1.x, mientras main avanza a 2.x ---
git branch release/1.x v1.0.0
echo "--- release/1.x creada desde el tag, para dar soporte mientras main avanza ---"

# --- main sigue avanzando con trabajo de la próxima versión mayor ---
echo "def login_v2(token): pass" >> auth.py
git add auth.py
git commit -q -m "feat(auth)!: rediseña login para requerir token

BREAKING CHANGE: la firma de login() cambia por completo en v2."
git tag -a v2.0.0-alpha -m "Avance de v2.0.0 (breaking)"
echo "--- main avanza hacia v2.0.0 con cambios incompatibles ---"

# --- Aparece un bug de seguridad que afecta a AMBAS versiones ---
echo "def login(): return validar_credenciales()" > auth_fix.py
git add auth_fix.py
git commit -q -m "fix(auth): valida credenciales antes de autorizar (CVE-2026-0001)"
FIX_COMMIT="$(git rev-parse HEAD)"
echo "--- Fix de seguridad aplicado en main: $FIX_COMMIT ---"

echo ""
echo "=== Backport del fix a release/1.x SIN traer el trabajo de v2 ==="
git switch release/1.x
git cherry-pick "$FIX_COMMIT"
git tag -a v1.0.1 -m "Hotfix de seguridad backporteado desde main"

echo ""
echo "=== Verificación: release/1.x tiene el fix pero NO el rediseño de v2 ==="
if git cat-file -e "release/1.x:auth_fix.py" 2>/dev/null; then
    echo "OK: el fix de seguridad SÍ llegó a release/1.x"
fi
if grep -q "login_v2" auth.py 2>/dev/null; then
    echo "ERROR: el cambio incompatible de v2 se coló en release/1.x"
else
    echo "OK: el cambio incompatible de v2 NO está en release/1.x"
fi

echo ""
echo "=== Estado final: dos líneas de versión, cada una con el fix ==="
echo "--- Tags ---"
git tag -l
echo "--- Historial de main ---"
git log main --oneline
echo "--- Historial de release/1.x ---"
git log release/1.x --oneline

echo ""
echo "Repo de ejemplo en: $REPO_DIR (bórralo con 'rm -rf $REPO_DIR' cuando termines)"
