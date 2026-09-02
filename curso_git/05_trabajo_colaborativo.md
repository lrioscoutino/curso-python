# 5. Trabajo colaborativo

## Repositorios remotos

```bash
git remote -v                      # ver repositorios remotos configurados
git remote add origin <url>        # añadir un remoto llamado "origin"
git remote remove origin           # eliminar un remoto
```

## Subir cambios (push)

```bash
git push origin main               # subir la rama main al remoto
git push -u origin nueva-rama      # subir y "trackear" — liga la rama local con la remota
git push --all                     # subir todas las ramas locales
```

`-u` (o `--set-upstream`) solo hace falta la primera vez que subes una rama; después basta con `git push` a secas, porque Git ya sabe a dónde debe ir.

## Descargar cambios (fetch/pull)

```bash
git fetch                          # descarga cambios del remoto SIN fusionarlos
git pull                           # descarga y fusiona (equivale a fetch + merge)
git pull origin main               # pull específico de una rama
```

## Práctica 4 — Trabajo remoto

1. Crea un repositorio **propio** en GitHub (vacío, tú eres el dueño).
2. Conecta tu repositorio local con el remoto.
3. Sube tu código con `git push`.
4. Haz un cambio desde la interfaz web de GitHub (edita un archivo directo en el navegador).
5. Descarga ese cambio con `git pull`.

**Solución:**

```bash
# 1. Crear repositorio en GitHub (interfaz web)
#    New repository -> nombre: mi-proyecto-remoto -> Create (sin README, para que quede vacío)

# 2. Conectar el repositorio local (el de la Práctica 2, por ejemplo) con el remoto
git remote add origin https://github.com/TU-USUARIO/mi-proyecto-remoto.git
git remote -v

# 3. Subir código
git push -u origin main

# 4. Hacer cambios desde GitHub
#    Ir al repo en GitHub -> abrir README.md -> lápiz de editar -> agregar una línea -> Commit changes

# 5. Descargar cambios
git pull origin main
# o simplemente: git pull   (ya hay tracking establecido desde el push -u)

git log --oneline
```

> **Nota:** siempre usa un repositorio que **tú creaste**, nunca un repositorio de otra persona u organización — no vas a tener permiso de escritura ahí, y `git push` fallará con `403 Permission denied` sin importar qué tan bien esté tu código.

### Comandos adicionales útiles

```bash
git branch -a                # ver ramas locales y remotas
git fetch origin              # descargar referencias sin fusionar
git diff origin/main           # comparar tu rama local contra la remota
git push origin nombre-rama      # subir una rama específica
```

---

**Anterior:** [04_ramas.md](04_ramas.md) · **Siguiente:** [06_comandos_intermedios.md](06_comandos_intermedios.md)
