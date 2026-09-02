# 2. Configuración inicial

## Configuración de identidad

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

Esta identidad queda grabada en cada commit que hagas — es lo que aparece en `git log` junto a cada cambio.

## Configuración del editor

```bash
git config --global core.editor "code --wait"   # VS Code
git config --global core.editor "vim"            # Vim
git config --global core.editor "nano"            # Nano (más simple para empezar)
```

Git abre este editor cuando necesita un mensaje de commit y no se le dio uno con `-m` (por ejemplo, al completar un merge o un `git revert` sin `-m`).

## Nombre de la rama principal por defecto

```bash
git config --global init.defaultBranch main
```

Sin esto, `git init` puede crear la rama inicial como `master` en vez de `main` dependiendo de la versión/configuración de tu sistema — y los ejercicios de este curso (y de cualquier repo que clones de GitHub, que usa `main` por defecto) esperan que la rama principal se llame `main`. Configurarlo una sola vez aquí evita ese problema en todo lo que sigue.

## Verificar configuración

```bash
git config --list           # toda la configuración activa
git config user.name         # un valor específico
git config user.email
```

## Práctica 1 — Configuración inicial

1. Configura tu nombre y email globalmente.
2. Establece tu editor preferido.
3. Verifica que la configuración se aplicó correctamente.

**Solución:**

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
git config --global core.editor "code --wait"
git config --global init.defaultBranch main

git config --list
git config user.name
git config user.email
```

---

**Anterior:** [01_introduccion_y_conceptos.md](01_introduccion_y_conceptos.md) · **Siguiente:** [03_comandos_basicos.md](03_comandos_basicos.md)
