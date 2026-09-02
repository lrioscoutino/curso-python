# Ejemplos ejecutables

Scripts bash que crean un repositorio temporal (`mktemp -d`) y reproducen en vivo cada concepto del curso — corren de principio a fin sin intervención manual, y al final imprimen la ruta del repo de ejemplo para que lo inspecciones con `git log`, `git show`, etc.

## Scripts

| Script | Qué demuestra | Corresponde a |
|---|---|---|
| `01_commits_atomicos_demo.sh` | Separar dos cambios mezclados en dos commits atómicos | [02_commits_atomicos.md](../02_commits_atomicos.md) |
| `02_conventional_commits_demo.sh` | Historial con Conventional Commits + filtrado con `--grep` | [03_mensajes_de_commit.md](../03_mensajes_de_commit.md) |
| `03_github_flow_demo.sh` | Feature branches cortas fusionadas directo a `main` | [04_flujos_de_ramas.md](../04_flujos_de_ramas.md) |
| `04_gitflow_demo.sh` | `main` + `develop` + `release/*` + `hotfix/*` completo | [04_flujos_de_ramas.md](../04_flujos_de_ramas.md) |
| `05_despliegues_semver_demo.sh` | Dos versiones en soporte + `cherry-pick` de un fix de seguridad | [06_multiples_despliegues.md](../06_multiples_despliegues.md) |

Correr cualquiera:

```bash
bash 01_commits_atomicos_demo.sh
```

## `hooks/` — hooks de Git reutilizables

| Hook | Qué hace | Corresponde a |
|---|---|---|
| `commit-msg` | Rechaza un commit si el mensaje no sigue Conventional Commits | [03_mensajes_de_commit.md](../03_mensajes_de_commit.md) |
| `pre-push` | Rechaza el push si el nombre de rama no sigue la convención `tipo/descripcion` | [05_nombres_de_ramas.md](../05_nombres_de_ramas.md) |

Instalar en un proyecto real:

```bash
cp ejemplos/hooks/commit-msg .git/hooks/commit-msg
cp ejemplos/hooks/pre-push .git/hooks/pre-push
chmod +x .git/hooks/commit-msg .git/hooks/pre-push
```

A partir de ahí, cualquier commit o push que rompa la convención se rechaza automáticamente con un mensaje explicando por qué.
