# 1. Buenas prácticas generales

## Un commit, una intención

Cada commit debería responder a una sola pregunta: "¿qué cambió y por qué?". Si para explicarlo necesitas la palabra "y" dos veces ("arreglé el bug Y actualicé las dependencias Y renombré una variable"), son al menos dos commits.

## El historial es documentación, no un log de guardado automático

`git log` de un buen repositorio se lee como una narrativa: cada línea es una decisión con propósito. Un mal hábito común es commitear cada vez que "algo funciona" (`wip`, `arreglo`, `cambios`, `asdf`) — eso convierte el historial en ruido que nadie puede usar para entender por qué el código es como es.

## Nunca commitear código roto en ramas compartidas

Un commit en una rama que otras personas usan (`main`, `develop`) debe dejar el proyecto en un estado funcional: que compile, que pasen los tests. Si necesitas guardar progreso a medio terminar, usa una rama personal o `git stash` — no contamines el historial compartido.

## Revisa antes de confirmar

```bash
git diff --staged      # qué se va a commitear, exactamente
git status              # qué archivos entran, cuáles no
```

Correr esto antes de cada `git commit` evita dos errores comunes: colar archivos que no debían ir (`.env`, `node_modules`, credenciales) y commitear cambios de más que no pertenecen a esta intención.

## `.gitignore` desde el primer commit

Configurar `.gitignore` **antes** de hacer el primer `git add .`, no después. Si un archivo sensible ya se subió, agregarlo a `.gitignore` no lo borra del historial — hace falta reescribir el historial (`git filter-repo`, `BFG Repo-Cleaner`), algo que se evita por completo si el ignore está desde el día uno.

## No reescribas historial ya compartido

`git rebase`, `git commit --amend`, `git push --force` sobre commits que **ya subiste y que otra persona pudo haber descargado** rompe el repositorio de esa persona. Regla práctica:

| Situación | ¿Es seguro reescribir? |
|---|---|
| Commits solo en tu rama local, nunca pusheados | Sí, libremente |
| Commits pusheados a tu propia rama de feature, nadie más la usa | Sí, con `git push --force-with-lease` (nunca `--force` a secas) |
| Commits en `main`/`develop` o cualquier rama compartida | No — usa `git revert` en su lugar |

## Un Pull Request pequeño se revisa mejor que uno grande

Un PR de 50 líneas se revisa en minutos y con atención real; uno de 2,000 líneas se aprueba "de confianza" sin leerlo — que es exactamente cuando se cuelan los bugs. Si una tarea es grande, se puede seguir dividiendo en PRs incrementales (ver [`incremental-implementation`](../../curso_git/README.md) como filosofía general).

## Firma tus commits si el equipo lo requiere

```bash
git config --global commit.gpgsign true
git config --global user.signingkey <tu-key-id>
```

En equipos con exigencias de seguridad/compliance, cada commit debe poder verificarse criptográficamente como proveniente de quien dice ser.
