# Tutorial de Implementación de SAMBA en Ubuntu

## Interoperabilidad de Sistemas Operativos

---

## 1. Fundamentos Teóricos

### 1.1 ¿Qué es SAMBA?

SAMBA es una implementación libre del protocolo **SMB/CIFS** (Server Message Block / Common Internet File System) que permite compartir archivos, impresoras y otros recursos entre sistemas **Linux/Unix** y **Windows** en una misma red.

```
┌──────────────┐         Protocolo SMB/CIFS         ┌──────────────┐
│              │ ◄─────────────────────────────────► │              │
│  Ubuntu      │    Puerto 445 (TCP)                 │  Windows     │
│  (Servidor)  │    Puerto 139 (TCP)                 │  (Cliente)   │
│              │    Puerto 137-138 (UDP)             │              │
└──────────────┘                                     └──────────────┘
```

### 1.2 ¿Qué es el protocolo SMB/CIFS?

**SMB (Server Message Block)** es un protocolo de red de la capa de aplicación que permite:

| Función | Descripción |
|---------|-------------|
| Compartir archivos | Acceder a archivos remotos como si fueran locales |
| Compartir impresoras | Usar impresoras conectadas a otros equipos |
| Autenticación | Controlar quién accede a los recursos |
| Resolución de nombres | Identificar equipos en la red (NetBIOS) |

**Evolución del protocolo:**

```
SMB 1.0 (1983) → CIFS (1996) → SMB 2.0 (2006) → SMB 3.0 (2012) → SMB 3.1.1 (2015)
```

> **Nota:** SMB 1.0 está obsoleto y es inseguro. Las versiones modernas de SAMBA usan SMB 2.0+ por defecto.

### 1.3 ¿Por qué es importante la interoperabilidad?

En entornos reales, las redes suelen tener una mezcla de sistemas operativos:

- **Servidores:** Linux (Ubuntu, CentOS, Debian)
- **Estaciones de trabajo:** Windows 10/11, macOS
- **Dispositivos móviles:** Android, iOS

SAMBA permite que **todos estos sistemas compartan recursos** sin importar el sistema operativo, resolviendo el problema fundamental de la interoperabilidad.

### 1.4 Componentes de SAMBA

```
SAMBA
├── smbd          → Demonio principal (comparte archivos e impresoras)
├── nmbd          → Demonio de nombres NetBIOS (resolución de nombres)
├── smbclient     → Cliente de línea de comandos para acceder a recursos SMB
├── smbpasswd     → Gestión de contraseñas de usuarios SAMBA
├── testparm      → Validador de configuración (smb.conf)
└── smb.conf      → Archivo de configuración principal
```

### 1.5 Modelo de autenticación

SAMBA soporta dos modos de seguridad:

| Modo | Descripción | Caso de uso |
|------|-------------|-------------|
| `user` | Autenticación por usuario/contraseña | Redes pequeñas y medianas |
| `ads` | Integración con Active Directory | Entornos corporativos con AD |

---

## 2. Práctica: Instalación y Configuración

### 2.1 Requisitos previos

- Ubuntu 22.04 LTS o superior
- Acceso root o sudo
- Conexión a la red local
- Un cliente Windows/macOS/Linux para probar

### 2.2 Instalación de SAMBA

```bash
# Actualizar repositorios
sudo apt update

# Instalar SAMBA y utilidades
sudo apt install -y samba samba-common smbclient cifs-utils

# Verificar la instalación
samba --version

# Verificar que los servicios están activos
sudo systemctl status smbd
sudo systemctl status nmbd
```

**Verificación esperada:**

```
$ samba --version
Version 4.x.x

$ sudo systemctl status smbd
● smbd.service - Samba SMB Daemon
     Active: active (running) since ...
```

### 2.3 Configuración del firewall

```bash
# Permitir SAMBA a través del firewall
sudo ufw allow samba

# Verificar reglas
sudo ufw status
```

**Puertos que se abren:**

| Puerto | Protocolo | Servicio |
|--------|-----------|----------|
| 137 | UDP | NetBIOS Name Service |
| 138 | UDP | NetBIOS Datagram |
| 139 | TCP | NetBIOS Session |
| 445 | TCP | SMB directo |

---

## 3. Práctica: Carpeta Compartida Pública (Sin Autenticación)

### 3.1 Crear el directorio compartido

```bash
# Crear directorio para compartir
sudo mkdir -p /srv/samba/publico

# Dar permisos de lectura/escritura a todos
sudo chmod 777 /srv/samba/publico

# Cambiar el propietario a nobody (usuario genérico)
sudo chown nobody:nogroup /srv/samba/publico
```

### 3.2 Respaldar configuración original

```bash
# Siempre respaldar antes de editar
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.backup
```

### 3.3 Editar la configuración de SAMBA

```bash
sudo nano /etc/samba/smb.conf
```

Agregar al final del archivo:

```ini
[publico]
   comment = Carpeta Pública - Sin Autenticación
   path = /srv/samba/publico
   browseable = yes
   read only = no
   guest ok = yes
   create mask = 0666
   directory mask = 0777
   force user = nobody
```

**Explicación de cada parámetro:**

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| `comment` | texto | Descripción visible en la red |
| `path` | ruta | Directorio local a compartir |
| `browseable` | yes | Visible al explorar la red |
| `read only` | no | Permite escritura |
| `guest ok` | yes | No requiere autenticación |
| `create mask` | 0666 | Permisos para archivos nuevos (rw-rw-rw-) |
| `directory mask` | 0777 | Permisos para carpetas nuevas (rwxrwxrwx) |
| `force user` | nobody | Todos los accesos se hacen como "nobody" |

### 3.4 Validar y aplicar configuración

```bash
# Validar que no haya errores de sintaxis
testparm

# Reiniciar los servicios
sudo systemctl restart smbd nmbd
```

### 3.5 Probar desde Ubuntu (local)

```bash
# Listar los recursos compartidos
smbclient -L localhost -N

# Conectarse al recurso compartido
smbclient //localhost/publico -N

# Dentro de la sesión SMB:
smb: \> mkdir test_interop
smb: \> put /etc/hostname prueba.txt
smb: \> ls
smb: \> exit
```

---

## 4. Práctica: Carpeta Compartida Privada (Con Autenticación)

### 4.1 Crear usuario del sistema y de SAMBA

```bash
# Crear un usuario del sistema (sin acceso shell)
sudo useradd -M -s /usr/sbin/nologin samba_user

# Crear la contraseña de SAMBA para ese usuario
sudo smbpasswd -a samba_user
# Ingresa la contraseña dos veces

# Habilitar el usuario
sudo smbpasswd -e samba_user
```

> **Importante:** SAMBA mantiene su propia base de datos de contraseñas separada del sistema (`/var/lib/samba/private/passdb.tdb`). El usuario debe existir en ambos: sistema y SAMBA.

### 4.2 Crear directorio privado

```bash
sudo mkdir -p /srv/samba/privado
sudo chown samba_user:samba_user /srv/samba/privado
sudo chmod 770 /srv/samba/privado
```

### 4.3 Agregar configuración del recurso privado

Editar `/etc/samba/smb.conf` y agregar:

```ini
[privado]
   comment = Carpeta Privada - Requiere Autenticación
   path = /srv/samba/privado
   browseable = yes
   read only = no
   guest ok = no
   valid users = samba_user
   create mask = 0660
   directory mask = 0770
```

**Diferencias clave con la carpeta pública:**

| Parámetro | Público | Privado |
|-----------|---------|---------|
| `guest ok` | yes | **no** |
| `valid users` | (todos) | **samba_user** |
| `create mask` | 0666 | **0660** |

### 4.4 Aplicar y probar

```bash
# Validar configuración
testparm

# Reiniciar servicios
sudo systemctl restart smbd nmbd

# Probar con autenticación
smbclient //localhost/privado -U samba_user
# Ingresa la contraseña cuando se solicite
```

---

## 5. Práctica: Acceso desde Otros Sistemas Operativos

### 5.1 Obtener la IP del servidor SAMBA

```bash
# Obtener la dirección IP del servidor
ip addr show | grep "inet " | grep -v 127.0.0.1
# Ejemplo de resultado: 192.168.1.100
```

### 5.2 Acceso desde Windows

**Método 1: Explorador de archivos**

```
1. Abrir el Explorador de archivos
2. En la barra de dirección escribir: \\192.168.1.100
3. Presionar Enter
4. Aparecerán las carpetas: "publico" y "privado"
5. Para "privado" se pedirá usuario y contraseña
```

**Método 2: Línea de comandos (CMD)**

```cmd
:: Listar recursos compartidos
net view \\192.168.1.100

:: Mapear unidad de red
net use Z: \\192.168.1.100\publico

:: Mapear con autenticación
net use Y: \\192.168.1.100\privado /user:samba_user
```

**Método 3: PowerShell**

```powershell
# Listar recursos
Get-SmbConnection

# Mapear unidad
New-SmbMapping -LocalPath "Z:" -RemotePath "\\192.168.1.100\publico"

# Con credenciales
$cred = Get-Credential
New-SmbMapping -LocalPath "Y:" -RemotePath "\\192.168.1.100\privado" -UserName "samba_user"
```

### 5.3 Acceso desde macOS

```
1. Abrir Finder
2. Menú: Ir → Conectar al servidor (Cmd + K)
3. Escribir: smb://192.168.1.100/publico
4. Conectar
```

### 5.4 Acceso desde otro Linux

```bash
# Instalar cliente
sudo apt install cifs-utils smbclient

# Explorar recursos disponibles
smbclient -L 192.168.1.100 -N

# Montar carpeta pública
sudo mkdir -p /mnt/samba_publico
sudo mount -t cifs //192.168.1.100/publico /mnt/samba_publico -o guest

# Montar carpeta privada
sudo mkdir -p /mnt/samba_privado
sudo mount -t cifs //192.168.1.100/privado /mnt/samba_privado -o username=samba_user

# Verificar montaje
df -h | grep samba
ls /mnt/samba_publico
```

**Montaje permanente (fstab):**

```bash
# Agregar a /etc/fstab para montaje automático al arrancar
# Carpeta pública:
//192.168.1.100/publico  /mnt/samba_publico  cifs  guest,uid=1000  0  0

# Carpeta privada (usando archivo de credenciales):
//192.168.1.100/privado  /mnt/samba_privado  cifs  credentials=/etc/samba/creds,uid=1000  0  0
```

Crear archivo de credenciales:

```bash
sudo nano /etc/samba/creds
```

```
username=samba_user
password=tu_contraseña
```

```bash
sudo chmod 600 /etc/samba/creds
```

---

## 6. Diagrama de la Arquitectura Completa

```
                        RED LOCAL (192.168.1.0/24)
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ┌─────────────────────────────┐                               │
│   │  SERVIDOR UBUNTU            │                               │
│   │  192.168.1.100              │                               │
│   │                             │                               │
│   │  smbd ◄──── Puerto 445 ────┼──────┐                        │
│   │  nmbd ◄──── Puerto 137-139 ┼──────┤                        │
│   │                             │      │                        │
│   │  /srv/samba/                │      │                        │
│   │  ├── publico/  (guest ok)   │      │                        │
│   │  └── privado/  (auth req)   │      │                        │
│   └─────────────────────────────┘      │                        │
│                                        │                        │
│   ┌──────────────┐  ┌──────────────┐  ┌┴─────────────┐         │
│   │  Windows 11  │  │   macOS      │  │  Linux       │         │
│   │  .101        │  │   .102       │  │  .103        │         │
│   │              │  │              │  │              │         │
│   │  \\IP\pub   │  │  smb://IP    │  │  mount -t    │         │
│   │  Explorador  │  │  Finder      │  │  cifs        │         │
│   └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Administración y Monitoreo

### 7.1 Comandos de administración

```bash
# Ver usuarios SAMBA registrados
sudo pdbedit -L

# Ver usuarios con detalle
sudo pdbedit -Lv

# Cambiar contraseña de usuario SAMBA
sudo smbpasswd samba_user

# Eliminar usuario SAMBA
sudo smbpasswd -x samba_user

# Ver conexiones activas
sudo smbstatus

# Ver archivos abiertos
sudo smbstatus -S

# Ver configuración efectiva
testparm -s
```

### 7.2 Logs y diagnóstico

```bash
# Ver logs de SAMBA
sudo tail -f /var/log/samba/log.smbd
sudo tail -f /var/log/samba/log.nmbd

# Aumentar nivel de log para depuración (en smb.conf)
# log level = 3
# max log size = 5000

# Probar conectividad
smbclient -L localhost -U samba_user

# Verificar puertos abiertos
sudo ss -tlnp | grep -E '(445|139|138|137)'
```

### 7.3 Solución de problemas comunes

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| No se ve el servidor en la red | Firewall bloqueando | `sudo ufw allow samba` |
| "Access denied" en carpeta pública | Permisos del directorio | `sudo chmod 777 /srv/samba/publico` |
| "NT_STATUS_LOGON_FAILURE" | Contraseña SAMBA incorrecta | `sudo smbpasswd -a usuario` |
| Carpeta no aparece al explorar | `browseable = no` | Cambiar a `browseable = yes` |
| No se puede escribir | `read only = yes` | Cambiar a `read only = no` |
| Error de conexión desde Windows | Protocolo SMB1 deshabilitado | Verificar `server min protocol = SMB2` |

---

## 8. Seguridad: Buenas Prácticas

### 8.1 Configuración recomendada para producción

Agregar en la sección `[global]` de `smb.conf`:

```ini
[global]
   workgroup = WORKGROUP
   server string = Servidor SAMBA Ubuntu

   # Seguridad
   server min protocol = SMB2
   server max protocol = SMB3
   security = user
   encrypt passwords = yes

   # Restringir acceso por subred
   hosts allow = 192.168.1.0/24 127.0.0.1
   hosts deny = 0.0.0.0/0

   # Logging
   log file = /var/log/samba/log.%m
   max log size = 1000
   log level = 1

   # Deshabilitar impresoras si no se necesitan
   load printers = no
   printing = bsd
   printcap name = /dev/null
   disable spoolss = yes
```

### 8.2 Lista de verificación de seguridad

- [ ] Deshabilitar SMB 1.0 (`server min protocol = SMB2`)
- [ ] Restringir acceso por IP (`hosts allow`)
- [ ] Usar contraseñas fuertes para usuarios SAMBA
- [ ] No compartir el directorio raíz `/`
- [ ] Usar `valid users` en carpetas privadas
- [ ] Revisar logs periódicamente
- [ ] Mantener SAMBA actualizado (`sudo apt upgrade samba`)
- [ ] Usar permisos mínimos necesarios (no `777` en producción)

---

## 9. Script de Instalación Automatizada

```bash
#!/bin/bash
# install_samba.sh - Script de instalación rápida de SAMBA
# Uso: sudo bash install_samba.sh

set -e

echo "=== Instalación de SAMBA en Ubuntu ==="

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Ejecutar con sudo"
    exit 1
fi

# Instalar paquetes
echo "[1/6] Instalando paquetes..."
apt update && apt install -y samba samba-common smbclient cifs-utils

# Respaldar configuración
echo "[2/6] Respaldando configuración..."
cp /etc/samba/smb.conf /etc/samba/smb.conf.backup.$(date +%Y%m%d)

# Crear directorios
echo "[3/6] Creando directorios..."
mkdir -p /srv/samba/publico
mkdir -p /srv/samba/privado
chmod 777 /srv/samba/publico
chown nobody:nogroup /srv/samba/publico

# Configurar SAMBA
echo "[4/6] Configurando SAMBA..."
cat >> /etc/samba/smb.conf << 'SAMBA_EOF'

# === Configuración agregada por script ===
[publico]
   comment = Carpeta Publica
   path = /srv/samba/publico
   browseable = yes
   read only = no
   guest ok = yes
   create mask = 0666
   directory mask = 0777
   force user = nobody

[privado]
   comment = Carpeta Privada
   path = /srv/samba/privado
   browseable = yes
   read only = no
   guest ok = no
   valid users = samba_user
   create mask = 0660
   directory mask = 0770
SAMBA_EOF

# Crear usuario
echo "[5/6] Creando usuario samba_user..."
useradd -M -s /usr/sbin/nologin samba_user 2>/dev/null || true
chown samba_user:samba_user /srv/samba/privado
chmod 770 /srv/samba/privado
echo "Establece la contraseña de SAMBA para samba_user:"
smbpasswd -a samba_user

# Reiniciar servicios
echo "[6/6] Reiniciando servicios..."
systemctl restart smbd nmbd
ufw allow samba

# Validar
testparm -s 2>/dev/null

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "=== Instalación completada ==="
echo "Servidor SAMBA: $IP"
echo "Recurso público:  \\\\$IP\\publico"
echo "Recurso privado:  \\\\$IP\\privado  (usuario: samba_user)"
echo ""
echo "Probar: smbclient -L localhost -N"
```

---

## 10. Resumen Conceptual

```
INTEROPERABILIDAD CON SAMBA
═══════════════════════════

        Problema                          Solución
  ┌─────────────────┐             ┌─────────────────────┐
  │ Windows usa SMB  │             │                     │
  │ Linux usa NFS    │ ──────────► │  SAMBA implementa   │
  │ macOS usa AFP    │             │  SMB en Linux       │
  │ ¡No se entienden!│             │  ¡Todos se conectan!│
  └─────────────────┘             └─────────────────────┘

  Conceptos clave:
  ─────────────────
  • SMB/CIFS    = Protocolo de comunicación (el "idioma")
  • SAMBA       = Software que "habla" SMB en Linux
  • smbd        = Proceso que comparte archivos
  • nmbd        = Proceso que resuelve nombres en la red
  • smb.conf    = Archivo donde se define qué compartir
  • smbpasswd   = Herramienta para gestionar contraseñas
  • smbclient   = Cliente para probar conexiones
  • testparm    = Validador de configuración
```

---

## Referencias

- [Documentación oficial de SAMBA](https://www.samba.org/samba/docs/)
- [Wiki de SAMBA](https://wiki.samba.org/)
- [Ubuntu Server Guide - SAMBA](https://ubuntu.com/server/docs/samba-introduction)
- [man smb.conf](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html)
