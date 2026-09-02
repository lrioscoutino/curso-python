#!/usr/bin/env bash
# 3. Conventional Commits — demo ejecutable
#
# Crea un historial con commits de distintos tipos y muestra cómo
# filtrar el historial por tipo — la razón práctica de seguir el
# formato: se vuelve una base de datos consultable.
#
# Uso: bash 02_conventional_commits_demo.sh

set -euo pipefail

REPO_DIR="$(mktemp -d -t git-demo-commits-XXXX)"
cd "$REPO_DIR"

git init -q
git config user.name "Demo"
git config user.email "demo@example.com"

echo "=== Repo temporal creado en: $REPO_DIR ==="
echo ""

touch app.py
git add app.py
git commit -q -m "chore: inicializa el proyecto"

echo "def login(): pass" > app.py
git add app.py
git commit -q -m "feat(auth): agrega función de login"

echo "def login(): return True" > app.py
git add app.py
git commit -q -m "fix(auth): corrige login que siempre retornaba None"

echo "# Notas" > README.md
git add README.md
git commit -q -m "docs: agrega README con notas de instalación"

echo "def login():\n    return True" > app.py
git add app.py
git commit -q -m "style(auth): aplica formato consistente a login"

echo "def logout(): pass" >> app.py
git add app.py
git commit -q -m "feat(auth): agrega función de logout"

cat > app.py << 'EOF'
def login():
    return True
EOF
git add app.py
git commit -q -m "fix(auth)!: login ahora requiere token válido

BREAKING CHANGE: las llamadas existentes a login() sin token dejarán
de funcionar. Actualizar los clientes antes de desplegar."

echo "=== Historial completo ==="
git log --oneline

echo ""
echo "=== Filtrar solo features (para armar notas de release) ==="
git log --oneline --grep="^feat"

echo ""
echo "=== Filtrar solo cambios del scope 'auth' ==="
git log --oneline --grep="(auth)"

echo ""
echo "=== Encontrar cambios que rompen compatibilidad ==="
git log --oneline --grep="BREAKING CHANGE"

echo ""
echo "=== Ver el mensaje completo de un commit con BREAKING CHANGE ==="
git log --grep="BREAKING CHANGE" -1 --format="%B"

echo ""
echo "Repo de ejemplo en: $REPO_DIR (bórralo con 'rm -rf $REPO_DIR' cuando termines)"
