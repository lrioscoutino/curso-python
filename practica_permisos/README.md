# Practica: Usuarios, Permisos y Sistema de Archivos en Ubuntu

## Objetivo

Aprender a administrar usuarios, grupos y permisos en Linux. Al finalizar, sabras controlar **quien puede acceder a que** en un sistema Ubuntu.

---

## Teoria: Como funciona la seguridad en Linux?

Linux controla el acceso a archivos y directorios con **tres conceptos**:

| Concepto | Que es? | Ejemplo |
|---|---|---|
| **Usuario (user)** | La persona que ejecuta comandos | `luiscoutino`, `root` |
| **Grupo (group)** | Un conjunto de usuarios | `developers`, `sudo` |
| **Permisos (permissions)** | Que puede hacer cada quien con un archivo | leer, escribir, ejecutar |

Cada archivo tiene **un dueno** (user) y **un grupo**. Los permisos se definen para tres niveles:

```
  dueno     grupo     otros
   rwx       rwx       rwx
```

| Letra | Significado | En archivos | En directorios |
|---|---|---|---|
| `r` | read (leer) | Ver el contenido | Listar los archivos (`ls`) |
| `w` | write (escribir) | Modificar el contenido | Crear/eliminar archivos dentro |
| `x` | execute (ejecutar) | Ejecutar como programa | Entrar al directorio (`cd`) |
| `-` | sin permiso | No puede hacer esa accion | No puede hacer esa accion |

### Ejemplo real:

```
-rwxr-xr-- 1 mario developers 1024 mar 3 10:00 script.sh
```

Lectura de izquierda a derecha:

```
-        rwx        r-x        r--
|         |          |          |
tipo    dueno      grupo      otros
(archivo) mario puede  developers   cualquier
         leer,      pueden leer   otro solo
         escribir   y ejecutar    puede leer
         y ejecutar
```

---

## Paso 1: Ver tu usuario actual y sus grupos

Antes de crear usuarios nuevos, entiende quien eres ahora:

```bash
# Quien soy?
whoami

# A que grupos pertenezco?
groups

# Informacion detallada de mi usuario
id
```

**Que veras:**

```
uid=1000(luiscoutino) gid=1000(luiscoutino) groups=1000(luiscoutino),27(sudo),999(docker)
```

### Teoria:

- **uid** — User ID. Cada usuario tiene un numero unico. `root` siempre es `0`.
- **gid** — Group ID. El grupo principal del usuario.
- **groups** — Todos los grupos a los que perteneces. Si ves `sudo`, puedes ejecutar comandos como administrador. Si ves `docker`, puedes usar Docker sin `sudo`.

---

## Paso 2: Crear usuarios nuevos

Vamos a crear dos usuarios que simulan miembros de un equipo:

```bash
# Crear usuario "ana" con su directorio home
sudo useradd -m -s /bin/bash ana

# Crear usuario "carlos" con su directorio home
sudo useradd -m -s /bin/bash carlos

# Asignar contrasena a cada usuario
sudo passwd ana
sudo passwd carlos
```

**Verifica que se crearon:**

```bash
# Ver los usuarios en el sistema (ultimas 5 lineas)
tail -5 /etc/passwd
```

Veras algo como:

```
ana:x:1001:1001::/home/ana:/bin/bash
carlos:x:1002:1002::/home/carlos:/bin/bash
```

### Teoria - las opciones de useradd:

| Opcion | Que hace? |
|---|---|
| `-m` | Crea el directorio `/home/ana` automaticamente |
| `-s /bin/bash` | Asigna bash como shell del usuario (sin esto, podria no tener shell) |

### Teoria - el archivo /etc/passwd:

Cada linea tiene 7 campos separados por `:`:

```
ana  : x    : 1001 : 1001 :      : /home/ana : /bin/bash
 |     |       |      |      |        |           |
user  pass   uid    gid   info    home dir     shell
      (en
      shadow)
```

- La `x` en password significa que la contrasena real esta en `/etc/shadow` (archivo protegido).
- **Nunca** se guardan contrasenas en texto plano en Linux. Se almacenan como hash en `/etc/shadow`.

---

## Paso 3: Crear un grupo

Creamos un grupo llamado `equipo` para simular un equipo de trabajo:

```bash
# Crear el grupo
sudo groupadd equipo

# Agregar ana y carlos al grupo
sudo usermod -aG equipo ana
sudo usermod -aG equipo carlos

# Verificar quienes estan en el grupo
getent group equipo
```

Veras:

```
equipo:x:1003:ana,carlos
```

### Teoria:

- **`groupadd`** — Crea un grupo nuevo.
- **`usermod -aG equipo ana`** — Modifica el usuario `ana`:
  - `-a` = append (agregar, sin quitar los grupos que ya tiene)
  - `-G equipo` = al grupo `equipo`
- **CUIDADO**: Si usas `-G` sin `-a`, **reemplaza** todos los grupos del usuario. Siempre usa `-aG` juntos.

---

## Paso 4: Crear el directorio compartido del equipo

```bash
# Crear directorio de proyecto
sudo mkdir -p /proyecto/compartido

# Cambiar el grupo dueno del directorio
sudo chgrp equipo /proyecto/compartido

# Ver como quedo
ls -la /proyecto/
```

Veras:

```
drwxr-xr-x 2 root equipo 4096 mar 3 10:00 compartido
```

### Teoria - chgrp:

- `chgrp equipo /proyecto/compartido` — Cambia el **grupo** del directorio a `equipo`.
- El **dueno** sigue siendo `root` (quien lo creo con `sudo`).
- Aun no funciona del todo: el grupo solo tiene permiso `r-x` (leer y entrar, pero NO escribir). Lo arreglaremos en el siguiente paso.

---

## Paso 5: Asignar permisos con chmod

Ahora le damos permiso de escritura al grupo:

```bash
# Dar permisos: dueno=rwx, grupo=rwx, otros=sin acceso
sudo chmod 770 /proyecto/compartido

# Verificar
ls -la /proyecto/
```

Veras:

```
drwxrwx--- 2 root equipo 4096 mar 3 10:00 compartido
```

### Teoria - chmod con numeros (notacion octal):

Cada permiso tiene un valor numerico:

```
r = 4
w = 2
x = 1
```

Se suman para cada nivel:

```
  7     7     0
  |     |     |
dueno grupo  otros
r+w+x r+w+x  ---
4+2+1 4+2+1   0
```

### Tabla de referencia de combinaciones comunes:

| Numero | Permisos | Significado |
|---|---|---|
| `7` | `rwx` | Todo permitido |
| `6` | `rw-` | Leer y escribir, no ejecutar |
| `5` | `r-x` | Leer y ejecutar, no escribir |
| `4` | `r--` | Solo leer |
| `0` | `---` | Sin acceso |

### Ejemplos comunes:

| Comando | Resultado | Uso tipico |
|---|---|---|
| `chmod 755` | `rwxr-xr-x` | Scripts, programas |
| `chmod 644` | `rw-r--r--` | Archivos de texto, configs |
| `chmod 700` | `rwx------` | Directorio privado |
| `chmod 770` | `rwxrwx---` | Directorio compartido por grupo |

### Forma alternativa - chmod con letras:

```bash
# Es equivalente a chmod 770:
sudo chmod u=rwx,g=rwx,o= /proyecto/compartido

# Agregar permiso de escritura al grupo (sin tocar los demas):
sudo chmod g+w /proyecto/compartido

# Quitar permiso de ejecucion a otros:
sudo chmod o-x archivo.txt
```

| Simbolo | Significado |
|---|---|
| `u` | user (dueno) |
| `g` | group (grupo) |
| `o` | others (otros) |
| `a` | all (todos) |
| `+` | agregar permiso |
| `-` | quitar permiso |
| `=` | establecer exactamente |

---

## Paso 6: Probar los permisos (cambiar de usuario)

Ahora probamos que los permisos funcionan. Usa `su` (switch user) para cambiar de usuario:

### Prueba con ana (miembro del grupo):

```bash
# Cambiar al usuario ana
su - ana

# Intentar entrar al directorio
cd /proyecto/compartido

# Crear un archivo
echo "Hola, soy ana" > archivo_ana.txt

# Ver el archivo creado
ls -la

# Salir de ana
exit
```

**Resultado esperado:** Funciona sin errores. `ana` pertenece al grupo `equipo` y el directorio tiene permisos `rwx` para el grupo.

### Prueba con un usuario fuera del grupo:

```bash
# Crear un usuario que NO esta en el grupo
sudo useradd -m -s /bin/bash invitado
sudo passwd invitado

# Cambiar al usuario invitado
su - invitado

# Intentar entrar al directorio
cd /proyecto/compartido
```

**Resultado esperado:** Error de permiso.

```
bash: cd: /proyecto/compartido: Permission denied
```

**Por que?** El usuario `invitado` no es el dueno (`root`) ni pertenece al grupo (`equipo`), y los permisos para "otros" son `---` (cero).

```bash
# Salir de invitado
exit
```

---

## Paso 7: Cambiar dueno de archivos con chown

```bash
# Ver quien es dueno del archivo que creo ana
ls -la /proyecto/compartido/

# Cambiar el dueno a carlos
sudo chown carlos /proyecto/compartido/archivo_ana.txt

# Cambiar dueno Y grupo al mismo tiempo
sudo chown carlos:equipo /proyecto/compartido/archivo_ana.txt

# Verificar
ls -la /proyecto/compartido/
```

### Teoria:

| Comando | Que cambia? |
|---|---|
| `chown carlos archivo.txt` | Solo el dueno |
| `chown carlos:equipo archivo.txt` | Dueno y grupo |
| `chown :equipo archivo.txt` | Solo el grupo (equivale a `chgrp`) |
| `chown -R carlos:equipo /directorio/` | Dueno y grupo de todo el directorio recursivamente |

---

## Paso 8: Permisos especiales - el bit SGID

Hay un problema con el directorio compartido: cuando `ana` crea un archivo, el grupo del archivo es `ana`, no `equipo`. Esto significa que `carlos` podria no tener acceso.

El **bit SGID** en un directorio resuelve esto: todos los archivos creados dentro heredan el grupo del directorio.

```bash
# Activar SGID en el directorio compartido
sudo chmod g+s /proyecto/compartido

# Verificar (nota la "s" en los permisos del grupo)
ls -la /proyecto/
```

Veras:

```
drwxrws--- 2 root equipo 4096 mar 3 10:00 compartido
```

La `s` en la posicion de `x` del grupo significa que el bit SGID esta activo.

**Prueba:**

```bash
su - ana
cd /proyecto/compartido
echo "archivo nuevo" > prueba_sgid.txt
ls -la prueba_sgid.txt
exit
```

Ahora el archivo tiene grupo `equipo` en vez de `ana`:

```
-rw-rw-r-- 1 ana equipo 14 mar 3 10:30 prueba_sgid.txt
```

---

## Paso 9: Links simbolicos vs Hard links

### Link simbolico (symlink):

Es un **acceso directo**. Apunta al nombre del archivo original.

```bash
# Crear un archivo de prueba
echo "contenido original" > /tmp/original.txt

# Crear un link simbolico
ln -s /tmp/original.txt /tmp/acceso_directo.txt

# Ver que apunta al original
ls -la /tmp/acceso_directo.txt
```

Veras:

```
lrwxrwxrwx 1 luiscoutino luiscoutino 20 mar 3 10:00 /tmp/acceso_directo.txt -> /tmp/original.txt
```

La `l` al inicio indica que es un link simbolico.

```bash
# Leer a traves del link
cat /tmp/acceso_directo.txt

# Borrar el original
rm /tmp/original.txt

# Intentar leer el link (falla: apunta a algo que ya no existe)
cat /tmp/acceso_directo.txt
```

**Resultado:** Error. El link simbolico queda "roto" (dangling symlink).

### Hard link:

Es **otro nombre para el mismo archivo** en disco. Comparten los mismos datos.

```bash
# Crear un archivo de prueba
echo "contenido original" > /tmp/original2.txt

# Crear un hard link
ln /tmp/original2.txt /tmp/otro_nombre.txt

# Ambos apuntan al mismo contenido
cat /tmp/original2.txt
cat /tmp/otro_nombre.txt

# Ver que comparten el mismo inode (numero de archivo en disco)
ls -li /tmp/original2.txt /tmp/otro_nombre.txt
```

Veras que ambos tienen el **mismo inode** (primer numero):

```
1234567 -rw-rw-r-- 2 luiscoutino luiscoutino 20 mar 3 10:00 /tmp/original2.txt
1234567 -rw-rw-r-- 2 luiscoutino luiscoutino 20 mar 3 10:00 /tmp/otro_nombre.txt
```

```bash
# Borrar el "original"
rm /tmp/original2.txt

# El hard link SIGUE funcionando (los datos existen mientras quede al menos un nombre)
cat /tmp/otro_nombre.txt
```

**Resultado:** Funciona. El hard link no depende del nombre original.

### Comparacion:

| Aspecto | Link simbolico (`ln -s`) | Hard link (`ln`) |
|---|---|---|
| Es un... | Acceso directo | Otro nombre para el mismo archivo |
| Si borras el original | Se rompe | Sigue funcionando |
| Puede cruzar particiones | Si | No |
| Puede apuntar a directorios | Si | No |
| Uso comun | Accesos directos, versiones | Backups eficientes |

---

## Paso 10: El comando sudo y /etc/sudoers

### Que es sudo?

`sudo` = **S**uper **U**ser **DO**. Permite ejecutar un comando como `root` (administrador).

```bash
# Sin sudo: falla si no eres root
useradd prueba

# Con sudo: funciona
sudo useradd prueba
```

### Ver la configuracion de sudo:

```bash
# Ver el archivo sudoers de forma segura
sudo cat /etc/sudoers
```

Veras lineas como:

```
root    ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL
```

### Teoria - formato de sudoers:

```
quien    donde=(como_quien) que_comandos
root     ALL=(ALL:ALL)      ALL
```

| Campo | Significado |
|---|---|
| `root` | El usuario `root` |
| `%sudo` | El `%` indica un grupo. Todos los miembros del grupo `sudo` |
| `ALL=(ALL:ALL)` | Desde cualquier host, como cualquier usuario y grupo |
| `ALL` | Puede ejecutar cualquier comando |

### Dar sudo limitado a un usuario:

```bash
# Editar sudoers de forma segura (usa visudo, nunca edites directamente)
sudo visudo
```

Agrega al final del archivo:

```
carlos  ALL=(ALL) /usr/sbin/useradd, /usr/sbin/usermod
```

Esto le da a `carlos` permiso de usar **solo** `useradd` y `usermod` con `sudo`. No puede hacer `sudo rm -rf /` ni ningun otro comando como root.

```bash
# Probar como carlos
su - carlos
sudo useradd prueba123     # Funciona
sudo rm /etc/passwd        # Falla: no tiene permiso
exit
```

---

## Paso 11: Limpieza

Al terminar la practica, elimina los usuarios y archivos de prueba:

```bash
# Eliminar usuarios y sus directorios home
sudo userdel -r ana
sudo userdel -r carlos
sudo userdel -r invitado

# Eliminar el grupo
sudo groupdel equipo

# Eliminar el directorio del proyecto
sudo rm -rf /proyecto

# Eliminar archivos temporales
rm -f /tmp/original.txt /tmp/acceso_directo.txt /tmp/original2.txt /tmp/otro_nombre.txt

# Verificar que se limpio todo
getent group equipo        # No deberia devolver nada
id ana                     # Deberia dar error
ls /proyecto               # No deberia existir
```

---

## Resumen de comandos aprendidos

| Comando | Para que sirve |
|---|---|
| `whoami` | Ver tu usuario actual |
| `id` | Ver uid, gid y grupos |
| `groups` | Ver tus grupos |
| `useradd -m -s /bin/bash` | Crear usuario con home y shell |
| `passwd` | Cambiar contrasena de un usuario |
| `userdel -r` | Eliminar usuario y su home |
| `groupadd` | Crear grupo |
| `groupdel` | Eliminar grupo |
| `usermod -aG` | Agregar usuario a un grupo |
| `chmod` | Cambiar permisos (numeros u letras) |
| `chown` | Cambiar dueno y/o grupo |
| `chgrp` | Cambiar grupo |
| `ln -s` | Crear link simbolico |
| `ln` | Crear hard link |
| `su - usuario` | Cambiar de usuario |
| `sudo` | Ejecutar como administrador |
| `visudo` | Editar sudoers de forma segura |

---

## Ejercicios extra (para reforzar)

### Ejercicio 1: Directorio privado
Crea un directorio `/home/ana/privado` donde **solo ana** pueda leer, escribir y entrar. Nadie mas debe poder acceder.

<details>
<summary>Solucion</summary>

```bash
su - ana
mkdir ~/privado
chmod 700 ~/privado
exit
```
</details>

### Ejercicio 2: Archivo de solo lectura
Crea un archivo `/proyecto/compartido/reglas.txt` que **todos** puedan leer pero **solo root** pueda modificar.

<details>
<summary>Solucion</summary>

```bash
sudo bash -c 'echo "No borrar archivos ajenos" > /proyecto/compartido/reglas.txt'
sudo chown root:equipo /proyecto/compartido/reglas.txt
sudo chmod 644 /proyecto/compartido/reglas.txt
```
</details>

### Ejercicio 3: Investigar permisos
Usa `ls -la` para ver los permisos de estos archivos del sistema y explica por que tienen esos permisos:

```bash
ls -la /etc/passwd
ls -la /etc/shadow
ls -la /usr/bin/sudo
```

<details>
<summary>Solucion</summary>

- `/etc/passwd` (`-rw-r--r--`): Todos pueden leerlo (necesario para ver nombres de usuario), solo root puede escribirlo.
- `/etc/shadow` (`-rw-r-----`): Solo root y el grupo shadow pueden leerlo. Contiene los hashes de contrasenas.
- `/usr/bin/sudo` (`-rwsr-xr-x`): La `s` en la posicion del dueno es el **bit SUID**. Significa que al ejecutar `sudo`, se ejecuta como root sin importar quien lo invoque.
</details>

### Ejercicio 4: Conexion con Docker
Si ya hiciste la practica de Docker, responde:

1. Cuando usas `docker run -u 1000:1000 ...`, que significan esos numeros?
2. Por que necesitas `sudo` para ejecutar Docker (a menos que tu usuario este en el grupo `docker`)?
3. Que relacion tiene el `USER` del Dockerfile con los permisos del sistema?

<details>
<summary>Solucion</summary>

1. Son el **uid** y **gid** con los que corre el proceso dentro del container. Es el mismo concepto de `id` que vimos.
2. El daemon de Docker (`dockerd`) corre como root. El socket `/var/run/docker.sock` tiene permisos `srw-rw----` con grupo `docker`. Solo root o miembros del grupo `docker` pueden comunicarse con el daemon.
3. La instruccion `USER` en un Dockerfile establece con que usuario/grupo se ejecutan los comandos siguientes y el proceso final del container. Usa el mismo sistema de permisos de Linux que practicamos aqui.
</details>
