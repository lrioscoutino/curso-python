# Modulo 4: Funciones del Sistema de Proteccion (Tema 6.3)

## 4.1 Teoria: Funciones Principales

El sistema de proteccion de un SO ejecuta varias funciones criticas:

```
┌─────────────────────────────────────────────────────────────────┐
│               FUNCIONES DEL SISTEMA DE PROTECCION               │
├─────────────────┬───────────────────────────────────────────────┤
│ 1. Autenticacion│ Verificar identidad del usuario               │
│                 │ "Eres quien dices ser?"                       │
├─────────────────┼───────────────────────────────────────────────┤
│ 2. Autorizacion │ Verificar permisos sobre recursos             │
│                 │ "Tienes permiso para hacer esto?"             │
├─────────────────┼───────────────────────────────────────────────┤
│ 3. Auditoria    │ Registrar acciones para revision posterior    │
│                 │ "Que hiciste y cuando?"                       │
├─────────────────┼───────────────────────────────────────────────┤
│ 4. Control de   │ Gestionar permisos de acceso a archivos,     │
│    Acceso       │ memoria, CPU, dispositivos I/O                │
├─────────────────┼───────────────────────────────────────────────┤
│ 5. Aislamiento  │ Separar procesos entre si y del kernel        │
│    de Procesos  │ Cada proceso en su espacio de direcciones     │
├─────────────────┼───────────────────────────────────────────────┤
│ 6. Mediacion    │ Toda solicitud de acceso pasa por un punto    │
│    Completa     │ de control (monitor de referencia)            │
└─────────────────┴───────────────────────────────────────────────┘
```

## 4.2 Funcion 1: Autenticacion

### Factores de autenticacion

```
Algo que SABES:     Password, PIN, pregunta secreta
Algo que TIENES:    Token fisico, celular (2FA), smart card
Algo que ERES:      Huella digital, iris, reconocimiento facial

Multi-factor (MFA): Combinar 2 o mas factores
  Ejemplo: Password (sabes) + Codigo SMS (tienes)
```

### Como Linux autentica usuarios

```
1. Login: usuario ingresa nombre y contrasena
2. El sistema busca al usuario en /etc/passwd
3. Compara el hash de la contrasena con /etc/shadow
4. Si coincide -> crea sesion con UID/GID del usuario
5. El proceso shell hereda ese dominio de proteccion

Flujo:
  usuario "luis" + password "abc123"
       │
       ▼
  /etc/passwd -> luis:x:1000:1000::/home/luis:/bin/bash
       │
       ▼
  /etc/shadow -> luis:$6$salt$hash...:19000:0:99999:7:::
       │
       ▼
  Comparar hash(password_ingresada + salt) == hash_almacenado
       │
       ▼
  MATCH -> Sesion creada con UID=1000, GID=1000
```

### PAM (Pluggable Authentication Modules)

```
Linux usa PAM para hacer la autenticacion modular y configurable:

  /etc/pam.d/          -> Configuracion por servicio
  /etc/pam.d/login     -> Reglas para login en terminal
  /etc/pam.d/sshd      -> Reglas para SSH
  /etc/pam.d/sudo      -> Reglas para sudo

Cada archivo define una "pila" de modulos:
  auth     required  pam_unix.so       # Verificar password Unix
  auth     required  pam_faillock.so   # Bloquear tras X intentos
  account  required  pam_unix.so       # Verificar cuenta activa
  session  required  pam_limits.so     # Aplicar limites de recursos
```

## 4.3 Funcion 2: Autorizacion (Control de Acceso)

### Permisos Unix tradicionales

```
  Tipo  Owner  Group  Others
   -    rwx    r-x    r--       = 754

  r (read)    = 4   -> Leer contenido
  w (write)   = 2   -> Modificar contenido
  x (execute) = 1   -> Ejecutar (archivo) o entrar (directorio)

  Para directorios:
    r = listar contenido (ls)
    w = crear/borrar archivos dentro
    x = entrar al directorio (cd)
```

### Bits especiales

```
  SUID (Set User ID):  El programa se ejecuta con permisos del OWNER
    chmod u+s programa  -> -rwsr-xr-x
    Ejemplo: /usr/bin/passwd ejecuta como root aunque lo use un usuario normal
    RIESGO: si el programa tiene un bug, el atacante obtiene permisos del owner

  SGID (Set Group ID):  El programa se ejecuta con permisos del GRUPO
    chmod g+s programa  -> -rwxr-sr-x
    En directorios: archivos nuevos heredan el grupo del directorio

  Sticky Bit:  Solo el owner puede borrar sus archivos en el directorio
    chmod +t directorio -> drwxrwxrwt
    Ejemplo: /tmp tiene sticky bit -> todos escriben pero solo borran lo suyo
```

### ACLs (Access Control Lists) - Permisos extendidos

```
Los permisos Unix son limitados: solo owner, grupo y otros.
ACLs permiten definir permisos para usuarios/grupos especificos:

  Permisos clasicos:
    archivo.txt  owner:luis  group:devs  permisos:640
    -> Luis lee/escribe, devs lee, otros nada

  Con ACL:
    archivo.txt + ACL: maria puede leer, pedro puede leer+escribir
    -> Permisos individuales sin cambiar owner o grupo
```

## 4.4 Funcion 3: Auditoria

```
Registrar TODAS las acciones relevantes de seguridad:
  - Intentos de login (exitosos y fallidos)
  - Acceso a archivos sensibles
  - Cambios de permisos
  - Comandos ejecutados con sudo
  - Instalacion/desinstalacion de paquetes

Archivos de log clave en Linux:
  /var/log/auth.log      -> Autenticacion (login, sudo, SSH)
  /var/log/syslog        -> Mensajes generales del sistema
  /var/log/kern.log      -> Mensajes del kernel
  /var/log/faillog       -> Intentos de login fallidos
  /var/log/audit/         -> Logs de auditd (si esta instalado)

La auditoria sirve para:
  1. Detectar intrusiones (actividad sospechosa)
  2. Investigar incidentes (que paso y cuando)
  3. Cumplimiento legal (GDPR, HIPAA, etc.)
  4. Rendicion de cuentas (quien hizo que)
```

## 4.5 Funcion 4: Aislamiento de Procesos

```
Cada proceso tiene su propio espacio de direcciones virtuales:

  Proceso A (PID 100)         Proceso B (PID 200)
  ┌──────────────────┐        ┌──────────────────┐
  │ Codigo            │        │ Codigo            │
  │ Datos             │        │ Datos             │
  │ Heap              │        │ Heap              │
  │ Stack             │        │ Stack             │
  └──────────────────┘        └──────────────────┘
         │                            │
         ▼                            ▼
  ┌─────────────────────────────────────────────┐
  │            Memoria Fisica (RAM)             │
  │  [A cod][B cod][A datos][B heap][A stack]   │
  └─────────────────────────────────────────────┘
  La MMU (Memory Management Unit) mapea direcciones virtuales
  a fisicas. Proceso A NO puede acceder a paginas de B.

  Si A intenta acceder a memoria de B -> SEGMENTATION FAULT
```

### Monitor de Referencia

```
Concepto teorico: TODO acceso a recursos debe pasar por el monitor de referencia.

  Proceso ──solicita acceso──> [Monitor de Referencia] ──> Recurso
                                       │
                                       ▼
                              ┌─────────────────┐
                              │ Verifica:        │
                              │ 1. Autenticado?  │
                              │ 2. Autorizado?   │
                              │ 3. Registrar log │
                              └─────────────────┘

  Propiedades del monitor de referencia:
    - No se puede evitar (todo pasa por el)
    - No se puede modificar (a prueba de manipulacion)
    - Suficientemente pequeno para ser verificable
```

## 4.6 Practica: Funciones de Proteccion en Accion

### Ejercicio 1: Autenticacion - Examinando /etc/shadow

```bash
# /etc/passwd es legible por todos (nombres de usuario)
ls -la /etc/passwd
cat /etc/passwd | head -5

# /etc/shadow tiene los hashes de passwords (solo root)
ls -la /etc/shadow
sudo cat /etc/shadow | head -3

# Anatomia de una linea de shadow:
# usuario:$tipo$salt$hash:dias_desde_epoch:min:max:warn:inactive:expire
#
# $tipo:
#   $1$ = MD5 (inseguro, obsoleto)
#   $5$ = SHA-256
#   $6$ = SHA-512 (recomendado)
#   $y$ = yescrypt (mas nuevo)
```

### Ejercicio 2: Autorizacion - Permisos y ACLs

```bash
# Crear estructura de prueba
mkdir -p /tmp/proteccion_funciones
cd /tmp/proteccion_funciones

# Demostrar SUID
echo '#!/bin/bash
echo "Ejecutando como: $(whoami) (UID: $(id -u))"' > script_suid.sh
chmod 755 script_suid.sh

# Sin SUID: ejecuta como tu usuario
./script_suid.sh

# Demostrar ACLs
echo "datos del proyecto" > proyecto.txt
chmod 600 proyecto.txt  # Solo owner

# Dar acceso de lectura a un usuario especifico con ACL
# (requiere paquete acl instalado)
sudo apt install acl -y 2>/dev/null

# Agregar ACL: www-data puede leer
setfacl -m u:www-data:r proyecto.txt

# Ver ACLs del archivo
getfacl proyecto.txt
# Salida incluira: user:www-data:r--

# Listar archivos con ACL (note el + al final de permisos)
ls -la proyecto.txt
# -rw-------+ 1 luis luis ... proyecto.txt  (el + indica ACL)

# Remover ACL
setfacl -x u:www-data proyecto.txt
```

### Ejercicio 3: Auditoria - Revisando logs

```bash
# Ultimos intentos de login (exitosos y fallidos)
sudo journalctl -u systemd-logind --since "1 hour ago" --no-pager | tail -20

# Todos los comandos sudo ejecutados hoy
sudo journalctl _COMM=sudo --since today --no-pager | tail -20

# Intentos de autenticacion SSH (si SSH esta activo)
sudo journalctl -u ssh --since today --no-pager | tail -20

# Buscar intentos fallidos de login
sudo grep "Failed" /var/log/auth.log 2>/dev/null | tail -10

# Ver quien inicio sesion recientemente
last | head -10

# Intentos fallidos de login
sudo faillog -a 2>/dev/null | head -20
```

### Ejercicio 4: Script completo de funciones de proteccion

```python
#!/usr/bin/env python3
"""
Demuestra las funciones principales del sistema de proteccion
interactuando con el SO real.
"""
import os
import pwd
import grp
import stat
import subprocess
import tempfile

def banner(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")

def demo_autenticacion():
    """Muestra informacion de autenticacion del usuario actual."""
    banner("FUNCION 1: AUTENTICACION")

    uid = os.getuid()
    user_info = pwd.getpwuid(uid)

    print(f"  Usuario:     {user_info.pw_name}")
    print(f"  UID:         {user_info.pw_uid}")
    print(f"  GID:         {user_info.pw_gid}")
    print(f"  Home:        {user_info.pw_dir}")
    print(f"  Shell:       {user_info.pw_shell}")

    # Verificar metodo de hash de password
    try:
        with open("/etc/shadow") as f:
            for line in f:
                if line.startswith(f"{user_info.pw_name}:"):
                    hash_field = line.split(":")[1]
                    if hash_field.startswith("$6$"):
                        print(f"  Hash tipo:   SHA-512 (seguro)")
                    elif hash_field.startswith("$y$"):
                        print(f"  Hash tipo:   yescrypt (muy seguro)")
                    elif hash_field.startswith("$5$"):
                        print(f"  Hash tipo:   SHA-256")
                    break
    except PermissionError:
        print("  Hash tipo:   (requiere root para verificar)")

def demo_autorizacion():
    """Demuestra control de acceso con archivos temporales."""
    banner("FUNCION 2: AUTORIZACION")

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("datos sensibles")
        archivo = f.name

    # Mostrar permisos actuales
    st = os.stat(archivo)
    modo = stat.filemode(st.st_mode)
    print(f"  Archivo: {archivo}")
    print(f"  Permisos: {modo}")
    print(f"  Owner: {pwd.getpwuid(st.st_uid).pw_name}")

    # Cambiar permisos
    os.chmod(archivo, 0o600)
    modo_nuevo = stat.filemode(os.stat(archivo).st_mode)
    print(f"  Permisos despues de chmod 600: {modo_nuevo}")

    # Verificar acceso
    print(f"  Lectura permitida:    {os.access(archivo, os.R_OK)}")
    print(f"  Escritura permitida:  {os.access(archivo, os.W_OK)}")

    # Verificar acceso a archivos del sistema
    print(f"\n  Acceso a /etc/passwd: {os.access('/etc/passwd', os.R_OK)}")
    print(f"  Acceso a /etc/shadow: {os.access('/etc/shadow', os.R_OK)}")

    os.unlink(archivo)

def demo_aislamiento():
    """Muestra aislamiento de procesos."""
    banner("FUNCION 4: AISLAMIENTO DE PROCESOS")

    pid = os.getpid()
    print(f"  PID actual: {pid}")

    # Mostrar mapa de memoria del proceso
    try:
        with open(f"/proc/{pid}/maps") as f:
            maps = f.readlines()
        print(f"  Regiones de memoria: {len(maps)}")
        print(f"  Primeras 3 regiones:")
        for line in maps[:3]:
            parts = line.strip().split()
            addr_range = parts[0]
            perms = parts[1]
            print(f"    {addr_range} [{perms}]")
    except PermissionError:
        print("  (requiere permisos para leer mapas de memoria)")

    # Mostrar limites del proceso
    try:
        with open(f"/proc/{pid}/limits") as f:
            limits = f.readlines()
        print(f"\n  Limites del proceso:")
        for line in limits[1:5]:  # Primeros 4 limites
            print(f"    {line.strip()}")
    except PermissionError:
        print("  (requiere permisos)")

def demo_bits_especiales():
    """Encuentra archivos con SUID/SGID en el sistema."""
    banner("BITS ESPECIALES: SUID/SGID")

    # Buscar archivos SUID comunes
    suid_comunes = [
        "/usr/bin/passwd",
        "/usr/bin/sudo",
        "/usr/bin/su",
        "/usr/bin/newgrp",
        "/usr/bin/chfn",
    ]

    print("  Archivos SUID del sistema (ejecutan como root):")
    for path in suid_comunes:
        if os.path.exists(path):
            st = os.stat(path)
            modo = stat.filemode(st.st_mode)
            es_suid = bool(st.st_mode & stat.S_ISUID)
            print(f"    {modo} {path} {'<-- SUID' if es_suid else ''}")

def main():
    print("=" * 60)
    print("  FUNCIONES DEL SISTEMA DE PROTECCION EN LINUX")
    print("=" * 60)

    demo_autenticacion()
    demo_autorizacion()
    demo_aislamiento()
    demo_bits_especiales()

    banner("RESUMEN")
    print("  1. Autenticacion: /etc/passwd + /etc/shadow + PAM")
    print("  2. Autorizacion:  chmod/chown + ACLs + capabilities")
    print("  3. Auditoria:     /var/log/auth.log + journalctl")
    print("  4. Aislamiento:   Espacios de direcciones virtuales")
    print("  5. Mediacion:     Todo pasa por el kernel (monitor ref)")

if __name__ == "__main__":
    main()
```

Guarda como `funciones_proteccion.py` y ejecuta:

```bash
python3 funciones_proteccion.py

# Para ver info completa (incluye hash type)
sudo python3 funciones_proteccion.py
```

## 4.7 Resumen del Modulo

```
Funciones del sistema de proteccion:

  AUTENTICACION  -> Verificar identidad (passwords, tokens, biometria)
                    En Linux: /etc/shadow + PAM

  AUTORIZACION   -> Verificar permisos (rwx, ACLs, capabilities)
                    En Linux: chmod, chown, setfacl

  AUDITORIA      -> Registrar acciones (/var/log/auth.log, journalctl)
                    Esencial para detectar y investigar incidentes

  AISLAMIENTO    -> Separar procesos (memoria virtual, MMU)
                    Cada proceso en su espacio de direcciones

  MEDIACION      -> Todo acceso pasa por el kernel
                    Monitor de referencia: no evitable, no modificable

  Bits especiales: SUID, SGID, Sticky Bit
  ACLs: permisos granulares mas alla de owner/group/others
```

## 4.8 Preguntas de Repaso

1. Que tres factores de autenticacion existen? Da un ejemplo de cada uno.
2. Que es PAM y por que es importante para la seguridad?
3. Que es SUID y por que puede ser un riesgo de seguridad?
4. Que diferencia hay entre permisos Unix clasicos y ACLs?
5. Que es el monitor de referencia y cuales son sus propiedades?
