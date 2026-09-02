# 7. Ejercicios integradores

## Ejercicio 1 — Commits atómicos con `git add -p`

1. Crea un repositorio nuevo con un archivo `calculadora.py` con dos funciones: `sumar(a, b)` y `restar(a, b)`.
2. Haz un commit inicial.
3. En una sola sesión de edición: agrega una función `multiplicar(a, b)` y corrige un typo en el docstring de `sumar`.
4. Usa `git add -p` para separar ambos cambios en dos commits atómicos, cada uno con un mensaje Conventional Commits correcto.
5. Verifica con `git log -p` que cada commit contiene únicamente lo que le corresponde.

**Solución:**

```bash
mkdir practica-commits && cd practica-commits
git init

cat > calculadora.py << 'EOF'
def sumar(a, b):
    """Retorna la suam de a y b."""
    return a + b


def restar(a, b):
    """Retorna la resta de a menos b."""
    return a - b
EOF

git add calculadora.py
git commit -m "feat: agrega funciones sumar y restar"

# Editar: agregar multiplicar + corregir typo "suam"
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

# Separar con add -p: primero solo el typo
git add -p calculadora.py
# responder 'y' al hunk del typo, 'n' al de multiplicar
git commit -m "docs: corrige typo en docstring de sumar"

git add calculadora.py
git commit -m "feat: agrega función multiplicar"

git log -p
```

## Ejercicio 2 — Reescribir un historial desordenado

Dado este historial real de un repositorio:

```
a1b2c3d cambios
e4f5g6h fix
h7i8j9k mas cambios y el readme
k1l2m3n arreglado
```

Sin conocer el diff exacto, escribe qué preguntas le harías al autor para reconstruir mensajes Conventional Commits correctos, y propone un ejemplo de cómo debieron verse esos 4 commits si en realidad representaban: un fix de un bug de validación de formularios, una actualización de la versión de una dependencia, una corrección de documentación, y una nueva función de exportar a PDF.

**Solución sugerida (orden no importa, depende del historial real):**

```
fix(formularios): valida campos vacíos antes de enviar
build: actualiza reportlab a 4.1.0
docs(readme): corrige instrucciones de instalación
feat(reportes): agrega exportación de reportes a PDF
```

## Ejercicio 3 — Simular Git Flow completo

1. Crea un repositorio con `main` y `develop`.
2. Crea `feature/exportar-pdf` desde `develop`, agrega un archivo `exportar.py`, commitea, fusiona de vuelta a `develop` con `--no-ff`.
3. Crea `release/1.1.0` desde `develop`. Simula un fix de última hora directo en la release.
4. Fusiona la release a `main` (con tag `v1.1.0`) y de vuelta a `develop`.
5. Simula un bug crítico en producción: crea `hotfix/prod-crash` desde el tag `v1.1.0` (no desde `develop`), arréglalo, fusiona a `main` (tag `v1.1.1`) y a `develop`.
6. Corre `git log --graph --all --oneline` y verifica que la topología coincide con lo esperado en [04_flujos_de_ramas.md](04_flujos_de_ramas.md).

## Ejercicio 4 — Nombrar ramas correctamente

Corrige estos nombres de rama mal formados a la convención de [05_nombres_de_ramas.md](05_nombres_de_ramas.md):

1. `Mi-Feature-De-Login`
2. `bug_fix_2`
3. `juan_trabajo_en_progreso`
4. `RELEASE-2.0`

**Solución sugerida:**

1. `feature/login` (o `feature/PROJ-XXX-login` si hay ticket)
2. `fix/PROJ-XXX-descripcion-del-bug` (el nombre original no dice qué bug es — ese es justo el problema a evitar)
3. `feature/PROJ-XXX-nombre-descriptivo` (nunca poner el nombre de la persona en el nombre de rama)
4. `release/v2.0.0`

## Ejercicio 5 — Backport con cherry-pick

1. Crea `main` con 3 commits y taggea el tercero como `v1.0.0`.
2. Crea `release/1.x` desde ese tag (simulando una versión anterior en soporte).
3. En `main`, agrega un 4to commit que arregla un bug de seguridad.
4. Usa `git cherry-pick` para llevar **solo ese commit** a `release/1.x`, sin traer nada más de `main`.
5. Taggea el resultado en `release/1.x` como `v1.0.1`.

## Ejercicio 6 — Discusión (sin código)

Un equipo despliega a producción 15 veces al día, tiene 40 desarrolladores, y usa Git Flow con ramas `develop` y `release/*` de larga duración. Los merges a `main` se acumulan y generan conflictos frecuentes.

Responde:

1. ¿Qué flujo de ramas de [04_flujos_de_ramas.md](04_flujos_de_ramas.md) encaja mejor con su ritmo de despliegue real?
2. ¿Qué tendrían que cambiar en su proceso de testing/CI para adoptarlo?
3. ¿Qué rol jugarían los feature flags en la transición?

**Guía de respuesta:** Trunk-Based Development — el ritmo de 15 despliegues/día es incompatible con ramas de larga duración como `develop`/`release/*`, que por diseño acumulan divergencia. Requeriría CI muy rápido y confiable, cobertura de tests alta antes de poder integrar directo a `main` con confianza, y feature flags para poder fusionar código incompleto a `main` sin exponerlo a usuarios reales hasta que esté listo.
