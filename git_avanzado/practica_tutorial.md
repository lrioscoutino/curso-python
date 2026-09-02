# Práctica tutorial paso a paso — de cero a un flujo de release completo

Esta práctica se sigue **a mano, en tu propia terminal** (a diferencia de los scripts de `ejemplos/`, que corren solos) — algunos pasos, como `git add -p`, son interactivos por diseño y forman parte del aprendizaje. Al final habrás construido un mini-proyecto con historial atómico, mensajes trackeables, una feature integrada vía "PR", una release taggeada, y un hotfix aplicado sin contaminar producción.

Tiempo estimado: 30-40 minutos. Requisito: Git instalado (`git --version`).

---

## Parte 1 — Preparar el terreno

```bash
mkdir practica-tienda && cd practica-tienda
git init -b main
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
```

Instala los hooks de este curso para que Git mismo te avise si rompes una convención — copia `commit-msg` y `pre-push` desde [`ejemplos/hooks/`](ejemplos/hooks/) de este mismo curso a tu nuevo repo:

```bash
mkdir -p .git/hooks
cp ../git_avanzado/ejemplos/hooks/commit-msg .git/hooks/commit-msg
cp ../git_avanzado/ejemplos/hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/commit-msg .git/hooks/pre-push
```

> Ajusta la ruta `../git_avanzado/ejemplos/hooks/` según dónde hayas clonado `curso-python` respecto a `practica-tienda/`.

**Checkpoint:** `ls .git/hooks/` debe mostrar `commit-msg` y `pre-push` con permiso de ejecución (`-rwxr-xr-x`).

---

## Parte 2 — Primer commit (y probar que el hook funciona)

```bash
echo "# Tienda Online" > README.md
git add README.md
git commit -m "documentacion sin formato correcto"
```

**Esto debe fallar** — el hook `commit-msg` va a rechazarlo porque no sigue Conventional Commits. Lee el mensaje de error que imprime.

Ahora hazlo bien:

```bash
git commit -m "docs: agrega README inicial"
```

**Checkpoint:** `git log --oneline` muestra un commit con el mensaje correcto — el commit fallido anterior **no dejó rastro** (Git nunca llegó a crearlo).

---

## Parte 3 — Commits atómicos con `git add -p` (interactivo, de verdad)

```bash
cat > carrito.py << 'EOF'
def agregar_item(carrito, item):
    carrito.append(item)
    return carrito
EOF
git add carrito.py
git commit -m "feat(carrito): agrega función para añadir items"
```

Ahora edita el archivo mezclando **dos cambios no relacionados** en una sola sesión:

```bash
cat > carrito.py << 'EOF'
def agregar_item(carrito, item):
    """Agrega un item al carrito y lo retorna."""
    carrito.append(item)
    return carrito


def calcular_total(carrito):
    return sum(item["precio"] for item in carrito)
EOF
```

Revisa qué cambió:

```bash
git diff carrito.py
```

Vas a ver **dos cambios distintos**: un docstring agregado a `agregar_item`, y una función nueva `calcular_total`. Sepáralos con staging interactivo:

```bash
git add -p carrito.py
```

Git te muestra el primer *hunk* y pregunta `Stage this hunk [y,n,q,a,d,s,e,?]?`:

- Si el hunk que aparece es **solo el docstring**, responde `y`.
- Si aparece **junto con** la función nueva, responde `s` (split) para que Git intente partirlo en trozos más chicos, y evalúa cada trozo por separado.
- Cuando aparezca el hunk de `calcular_total`, responde `n` (lo dejamos para el siguiente commit).

Confirma el primer commit atómico:

```bash
git status                     # calcular_total debe seguir como cambio NO preparado
git commit -m "docs(carrito): documenta agregar_item"
```

Ahora el segundo:

```bash
git add carrito.py
git commit -m "feat(carrito): agrega cálculo de total"
```

**Checkpoint:** `git log -p -2` — cada commit debe mostrar únicamente el cambio que le corresponde. Si `docs(carrito)` incluye `calcular_total`, repite el `git add -p` con más cuidado en el paso `s`/`e`.

---

## Parte 4 — Feature branch con nombre convencional (y el hook de push)

```bash
git switch -c mi-feature-nueva
```

Intenta "pushear" (aunque no haya remoto, el hook corre igual antes de intentar contactar la red):

```bash
git push 2>&1 | head -5
```

Debe fallar por el nombre de rama. Corrígelo:

```bash
git branch -m feature/checkout-descuentos
```

Agrega la funcionalidad:

```bash
cat > descuentos.py << 'EOF'
def aplicar_descuento(total, porcentaje):
    return total * (1 - porcentaje / 100)
EOF
git add descuentos.py
git commit -m "feat(checkout): agrega cálculo de descuentos"
```

---

## Parte 5 — Integrar la feature (estilo GitHub Flow)

En un proyecto real esto sería un Pull Request revisado por alguien más. Aquí lo simulamos con un merge explícito que conserva el hecho de que fue una feature integrada (`--no-ff`).

> Usamos `--no-edit` para aceptar el mensaje que Git genera automáticamente (`Merge branch 'feature/...' into main`) en vez de escribir uno propio: el hook `commit-msg` exime específicamente esos mensajes autogenerados de Conventional Commits — un merge no es un cambio autoral, es la integración de commits que ya cuentan su propia historia.

```bash
git switch main
git merge --no-ff --no-edit feature/checkout-descuentos
git branch -d feature/checkout-descuentos
```

**Checkpoint:** `git log --graph --oneline` debe mostrar la bifurcación y el punto de fusión — no una línea recta (eso pasaría con un merge `--ff`, que borra la evidencia de que hubo una rama).

---

## Parte 6 — Preparar y taggear una release (SemVer)

Decide el número de versión mirando el historial desde el último tag (aquí no hay ninguno, así que empezamos en `1.0.0`):

```bash
git tag -a v1.0.0 -m "Release 1.0.0: carrito y checkout con descuentos"
```

Esto es lo que en producción real se despliega — no la punta de `main`, sino este punto exacto e inmutable.

---

## Parte 7 — una feature que NO debe salir todavía (se queda en su rama)

```bash
git switch -c feature/reportes-avanzados
echo "def reporte_mensual(): pass" > reportes.py
git add reportes.py
git commit -m "feat(reportes): wip de reportes mensuales, incompleto"
```

**A propósito, no la fusiones a `main` todavía.** Esta es la regla central de GitHub Flow: `main` siempre debe quedar en estado desplegable — un trabajo a medio terminar se queda viviendo en su propia rama hasta que esté listo, nunca se integra "temporalmente" a `main` para sacarlo después.

---

## Parte 8 — Bug crítico en producción → hotfix desde el TAG

Descubres que `calcular_total` explota si el carrito está vacío. Como está en producción (`v1.0.0`), el hotfix nace de ese tag — que en este punto es lo mismo que la punta de `main`, precisamente porque no le mezclamos nada más encima:

```bash
git switch main
git switch -c hotfix/carrito-vacio v1.0.0
```

Arregla el bug:

```bash
cat > carrito.py << 'EOF'
def agregar_item(carrito, item):
    """Agrega un item al carrito y lo retorna."""
    carrito.append(item)
    return carrito


def calcular_total(carrito):
    if not carrito:
        return 0
    return sum(item["precio"] for item in carrito)
EOF
git add carrito.py
git commit -m "fix(carrito): evita error cuando el carrito está vacío"
```

Cierra el hotfix en `main` y taggéalo como `1.0.1` (solo PATCH — es un fix, no rompe nada, no agrega funcionalidad):

```bash
git switch main
git merge --no-ff --no-edit hotfix/carrito-vacio
git tag -a v1.0.1 -m "Hotfix 1.0.1: corrige crash con carrito vacío"
git branch -d hotfix/carrito-vacio
```

**Checkpoint — el más importante de la práctica:**

```bash
git show v1.0.1:reportes.py 2>&1
```

Esto debe fallar (`fatal: path 'reportes.py' does not exist in 'v1.0.1'`) — el trabajo incompleto nunca llegó a producción, porque nunca se fusionó a `main` en primer lugar. Confirma que el trabajo sigue vivo y no se perdió:

```bash
git show feature/reportes-avanzados:reportes.py
```

Y que el fix sí llegó a producción:

```bash
git show v1.0.1:carrito.py | grep "if not carrito"
```

---

## Cierre — revisar la historia completa

```bash
git log --graph --oneline --all
git tag -l
```

Deberías poder señalar, sin ambigüedad:

- Qué commit corresponde a qué tipo de cambio (por el prefijo Conventional Commits).
- Dónde se integró cada feature (los puntos de merge `--no-ff`).
- Qué contiene exactamente cada versión publicada (`v1.0.0` vs `v1.0.1`).
- Por qué el hotfix no arrastró código incompleto.

## Preguntas de cierre (para discutir o responder por escrito)

1. En este ejercicio `main` y `v1.0.0` apuntan al mismo commit porque no fusionamos nada más encima. Imagina que en la Parte 7 SÍ hubieras fusionado `feature/reportes-avanzados` a `main` (rompiendo la regla de GitHub Flow) — ¿qué habría pasado si, en ese escenario, el hotfix se hubiera creado con `git switch -c hotfix/carrito-vacio main` en vez de `v1.0.0`?
2. ¿Por qué el tag de la release es `v1.0.1` y no `v1.1.0`?
3. Si en vez de un fix hubieras necesitado cambiar la firma de `calcular_total` de forma incompatible, ¿qué habría cambiado en el mensaje del commit y en el número de versión?
