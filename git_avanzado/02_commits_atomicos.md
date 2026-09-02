# 2. Commits atómicos

## Definición

Un commit **atómico** contiene un único cambio lógico, completo y autocontenido. "Atómico" en el mismo sentido que en bases de datos: o el commit representa la unidad de cambio completa, o no debería existir todavía.

**No es lo mismo que "commit pequeño".** Un commit atómico puede tocar 10 archivos si los 10 son necesarios para completar esa única intención (ej. renombrar una función y todos sus usos). Lo que lo hace atómico no es el tamaño, es que **no se puede dividir más sin dejar el proyecto en un estado incoherente o roto**.

## Señales de que un commit NO es atómico

- El mensaje usa "y" para conectar dos cosas no relacionadas: "corrige bug de login y actualiza el README".
- Si tuvieras que revertir el commit, perderías algo que no querías perder (ej. el fix de un bug crítico junto con un refactor cosmético no relacionado).
- Mezclas cambios de formato/estilo (espacios, imports reordenados) con cambios de lógica — hace el `diff` ilegible en code review.
- El commit "no compila si lo aplicas solo" en medio de una serie (rompe `git bisect`).

## Por qué importa: `git bisect`

```bash
git bisect start
git bisect bad                 # el commit actual tiene el bug
git bisect good v1.2.0          # esta versión anterior no lo tenía
# Git recorre el historial en binario, marcando good/bad en cada punto
```

`git bisect` encuentra el commit exacto que introdujo un bug **dividiendo el historial a la mitad repetidamente** — pero solo funciona si cada commit intermedio compila y es funcional. Una serie de commits atómicos hace que un bug se aísle en minutos; un historial de commits gigantes y mezclados hace que ese mismo proceso sea inútil.

## Técnica: `git add -p` (staging parcial)

Cuando ya hiciste varios cambios de una sentada y necesitas separarlos en commits atómicos retroactivamente, `git add -p` permite elegir **qué fragmentos** (hunks) de un archivo modificado entran al próximo commit:

```bash
git add -p archivo.py
```

Por cada fragmento, Git pregunta:

```
Stage this hunk [y,n,q,a,d,s,e,?]?
```

- `y` — sí, agregar este fragmento
- `n` — no, dejarlo fuera (para un commit posterior)
- `s` — dividir el fragmento en partes más pequeñas (split)
- `e` — editar manualmente qué líneas exactas entran

Esto permite escribir código de corrido y luego reconstruir una historia atómica y clara al momento de commitear, sin tener que planear cada línea de antemano.

## Ejemplo práctico

**Mal (un commit hace tres cosas distintas):**

```bash
git add .
git commit -m "fix login bug, update deps, format code"
```

**Bien (tres commits atómicos, cada uno revertible de forma independiente):**

```bash
git add -p src/auth.py          # solo el fix del bug
git commit -m "fix: valida el token expirado antes de autorizar"

git add requirements.txt
git commit -m "build: actualiza cryptography a 42.0.5 por CVE-2024-XXXX"

git add -p src/                  # solo el reformateo, nada de lógica
git commit -m "style: aplica black al módulo de autenticación"
```

## Práctica

1. Modifica dos funciones distintas y sin relación en un mismo archivo.
2. Usa `git add -p` para commitear solo los cambios de una función.
3. Haz un segundo commit con los cambios de la otra función.
4. Verifica con `git log -p` que cada commit contiene exactamente lo que pretendías, ni más ni menos.
