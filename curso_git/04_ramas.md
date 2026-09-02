# 4. Trabajo con ramas (branches)

## ¿Por qué usar ramas?

- Desarrollo de características en paralelo, sin pisarse el trabajo.
- Experimentación sin afectar el código principal.
- Colaboración organizada — cada persona/tarea en su propia línea de trabajo.
- Aislamiento de cambios hasta que estén listos para integrarse.

## Comandos de ramas

```bash
git branch                   # listar ramas locales
git branch -a                # listar todas las ramas (locales y remotas)
git branch nueva-rama        # crear una rama nueva (sin cambiarte a ella)

# Cambiar de rama — comando moderno (Git 2.23+), preferido:
git switch nueva-rama        # cambiar a una rama existente
git switch -c nueva-rama     # crear y cambiar en un solo paso

# Comando clásico (sigue funcionando, más antiguo y más "sobrecargado"):
git checkout nueva-rama
git checkout -b nueva-rama
```

> **Por qué `switch` sobre `checkout`:** `checkout` hace demasiadas cosas distintas (cambiar de rama, descartar cambios de un archivo, poner el repo en detached HEAD) — es fácil confundir un uso con otro. `git switch` (para ramas) y `git restore` (para archivos, ver [06_comandos_intermedios.md](06_comandos_intermedios.md)) separan esas responsabilidades. Este curso usa los comandos modernos; verás `checkout` en proyectos y tutoriales antiguos, y sigue siendo válido.

## Fusionar ramas (merge)

```bash
git switch main
git merge nueva-rama         # fusiona nueva-rama EN main (main se actualiza, nueva-rama no)
```

## Eliminar ramas

```bash
git branch -d rama-terminada    # eliminar rama local (seguro: solo si ya está fusionada)
git branch -D rama-terminada    # eliminar rama local (forzado, aunque no esté fusionada)
git push origin --delete rama   # eliminar rama remota
```

## Práctica 3 — Trabajo con ramas

1. Crea una nueva rama llamada `feature-login`.
2. Cambia a esa rama y crea un archivo `login.js`.
3. Haz commit de los cambios.
4. Vuelve a la rama `main`.
5. Fusiona la rama `feature-login`.
6. Elimina la rama `feature-login`.

**Solución:**

```bash
git switch -c feature-login

echo "function login() {" > login.js
echo "  console.log('Función de login');" >> login.js
echo "}" >> login.js
git add login.js
git commit -m "Añade función de login"

git switch main
git merge feature-login
git branch -d feature-login

git log --oneline
```

---

**Anterior:** [03_comandos_basicos.md](03_comandos_basicos.md) · **Siguiente:** [05_trabajo_colaborativo.md](05_trabajo_colaborativo.md)
