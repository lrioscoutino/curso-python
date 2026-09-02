#!/usr/bin/env bash
# 2. Commits atómicos — demo ejecutable
#
# Crea un repo temporal, hace dos cambios no relacionados sobre el mismo
# archivo en una sola sesión de edición, y los separa en dos commits
# atómicos. En una terminal real esto se hace con `git add -p`
# (interactivo); aquí se reproduce el mismo resultado por etapas para
# que el script corra de principio a fin sin intervención humana.
#
# Uso: bash 01_commits_atomicos_demo.sh

set -euo pipefail

REPO_DIR="$(mktemp -d -t git-demo-atomicos-XXXX)"
cd "$REPO_DIR"

git init -q
git config user.name "Demo"
git config user.email "demo@example.com"

echo "=== Repo temporal creado en: $REPO_DIR ==="
echo ""

cat > calculadora.py << 'EOF'
def sumar(a, b):
    """Retorna la suam de a y b."""
    return a + b


def restar(a, b):
    """Retorna la resta de a menos b."""
    return a - b
EOF

git add calculadora.py
git commit -q -m "feat: agrega funciones sumar y restar"
echo "--- Commit inicial ---"
git log --oneline

# Simulamos una sesión de edición que mezcla DOS cambios no relacionados:
# 1) corregir un typo en el docstring de sumar
# 2) agregar una función nueva multiplicar
cat > calculadora.py << 'EOF'
def sumar(a, b):
    """Retorna la suma de a y b."""
    return a + b


def restar(a, b):
    """Retorna la resta de a menos b."""
    return a - b


def multiplicar(a, b):
    """Retorna el producto de a y b."""
    return a * b
EOF

echo ""
echo "=== El working directory mezcla ahora dos cambios no relacionados ==="
git diff calculadora.py
echo ""
echo "=== En una terminal real: 'git add -p calculadora.py' y elegir hunk por hunk ==="
echo "    Aquí reproducimos ese resultado en dos pasos explícitos:"
echo ""

# --- Commit atómico 1/2: solo el fix del typo ---
cat > calculadora.py << 'EOF'
def sumar(a, b):
    """Retorna la suma de a y b."""
    return a + b


def restar(a, b):
    """Retorna la resta de a menos b."""
    return a - b
EOF

git add calculadora.py
git commit -q -m "docs: corrige typo en docstring de sumar"
echo "--- Commit atómico 1/2 ---"

# --- Commit atómico 2/2: ahora sí, la función nueva ---
cat > calculadora.py << 'EOF'
def sumar(a, b):
    """Retorna la suma de a y b."""
    return a + b


def restar(a, b):
    """Retorna la resta de a menos b."""
    return a - b


def multiplicar(a, b):
    """Retorna el producto de a y b."""
    return a * b
EOF

git add calculadora.py
git commit -q -m "feat: agrega función multiplicar"
echo "--- Commit atómico 2/2 ---"

echo ""
echo "=== Resultado: dos commits, cada uno revertible de forma independiente ==="
git log --oneline

echo ""
echo "=== git show del commit de docs: NO toca la función multiplicar ==="
git show --stat HEAD~1

echo ""
echo "Repo de ejemplo en: $REPO_DIR (bórralo con 'rm -rf $REPO_DIR' cuando termines)"
