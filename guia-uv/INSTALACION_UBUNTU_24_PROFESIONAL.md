# Guía de Instalación Profesional: Ubuntu 24.04 LTS

Guía completa para instalación de Ubuntu 24.04 LTS con particionamiento manual y puntos de montaje optimizados para entornos de desarrollo y producción.

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Conceptos de Particionamiento](#conceptos-de-particionamiento)
3. [Tamaños Oficiales Recomendados](#tamaños-oficiales-recomendados)
4. [Esquemas de Particiones](#esquemas-de-particiones)
5. [Proceso de Instalación](#proceso-de-instalación)
6. [Configuración Post-Instalación](#configuración-post-instalación)

---

## Requisitos Previos

### Requisitos del sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Procesador | 2 GHz dual-core | 4+ núcleos |
| RAM | 4 GB | 16 GB+ |
| Disco | 25 GB | 256 GB+ SSD |
| USB | 4 GB | 8 GB+ |

### Preparación

1. **Descargar ISO** de [ubuntu.com/download](https://ubuntu.com/download/desktop)
2. **Crear USB booteable**:
   ```bash
   # Linux
   sudo dd bs=4M if=ubuntu-24.04-desktop-amd64.iso of=/dev/sdX status=progress oflag=sync
   ```
3. **Respaldar datos importantes**
4. **Configurar BIOS/UEFI** para arranque desde USB

---

## Conceptos de Particionamiento

### Tipos de Tabla de Particiones

| Tipo | Características | Uso |
|------|-----------------|-----|
| **GPT** | Soporta discos >2TB, hasta 128 particiones, requerido para UEFI | Sistemas modernos (recomendado) |
| **MBR** | Límite 2TB, máximo 4 primarias, compatible con BIOS legacy | Sistemas antiguos |

### Sistemas de Archivos

| Sistema | Uso Recomendado | Características |
|---------|-----------------|-----------------|
| **ext4** | `/`, `/home`, `/var`, `/boot` | Estable, journaling, predeterminado en Ubuntu |
| **XFS** | `/var`, datos grandes, bases de datos | Alto rendimiento para archivos grandes |
| **Btrfs** | `/`, `/home` | Snapshots, compresión, COW |
| **FAT32** | `/boot/efi` | Requerido para partición EFI |
| **swap** | Área de intercambio | Memoria virtual |

### Puntos de Montaje Principales

| Punto | Propósito |
|-------|-----------|
| `/` | Sistema raíz - Contiene todo si no se separan otros puntos |
| `/boot` | Kernel y archivos de arranque |
| `/boot/efi` | Arranque UEFI (ESP) - Obligatorio en sistemas UEFI |
| `/home` | Datos de usuarios - Separarlo facilita reinstalaciones |
| `/var` | Datos variables - Logs, Docker, bases de datos, caché |
| `/tmp` | Archivos temporales |
| `/opt` | Software de terceros |
| `/srv` | Datos de servicios (servidores) |
| `swap` | Memoria virtual / hibernación |

---

## Tamaños Oficiales Recomendados

Basado en la documentación oficial de Ubuntu: [DiskSpace Wiki](https://help.ubuntu.com/community/DiskSpace), [SwapFaq](https://help.ubuntu.com/community/SwapFaq), [PartitioningSchemes](https://help.ubuntu.com/community/PartitioningSchemes).

### Particiones del Sistema

| Partición | Mínimo | Recomendado | Uso Intensivo | Notas |
|-----------|--------|-------------|---------------|-------|
| `/boot/efi` | 100 MB | 500 MB | 1 GB | FAT32, obligatorio en UEFI. Ubuntu 24.04 usa 1 GB por defecto |
| `/boot` | 250 MB | 500 MB | 1 GB | ext4, necesario si `/` está en LVM o cifrado |
| `/` (root) | **8 GB** | **15-25 GB** | 30-50 GB | ext4, sistema base. Mínimo absoluto 8 GB |
| `/var` | 2 GB | 10 GB | **50-100 GB+** | Para Docker/contenedores se recomienda partición separada |
| `/home` | Variable | Resto del disco | Resto | Datos de usuario, proyectos, configuraciones |
| `/tmp` | - | Tamaño de swap | 4-8 GB | Opcional, puede montarse en RAM (tmpfs) |
| `/opt` | - | 500 MB - 5 GB | 20 GB | Solo si se instala software de terceros |

### Swap según RAM (Tabla Oficial Ubuntu)

Fuente: [SwapFaq - Ubuntu Community](https://help.ubuntu.com/community/SwapFaq)

| RAM | Sin Hibernación | Con Hibernación | Máximo |
|-----|-----------------|-----------------|--------|
| 1 GB | 1 GB | 2 GB | 2 GB |
| 2 GB | 1 GB | 3 GB | 4 GB |
| 4 GB | 2 GB | 6 GB | 8 GB |
| 8 GB | 3 GB | 11 GB | 16 GB |
| 16 GB | 4 GB | 20 GB | 32 GB |
| 32 GB | 6 GB | 38 GB | 64 GB |
| 64 GB | 8 GB | 72 GB | 128 GB |

**Fórmulas oficiales:**
- **Sin hibernación**: Mínimo = `round(sqrt(RAM))`, Máximo = `2 × RAM`
- **Con hibernación**: Al menos igual al tamaño de RAM

> **Nota**: Si necesitas swap mayor a `2 × RAM`, es mejor agregar más RAM física.

### /var para Docker y Contenedores

Fuente: [Docker Storage - Ubuntu Server](https://documentation.ubuntu.com/server/explanation/virtualisation/docker-storage-networking-and-logging/)

Docker almacena todo en `/var/lib/docker`. Recomendaciones:

| Uso | Tamaño /var |
|-----|-------------|
| Sin Docker | 10 GB |
| Docker básico (pocas imágenes) | 30-50 GB |
| Docker moderado | 50-100 GB |
| Docker intensivo + bases de datos | **100 GB+** (partición separada recomendada) |

---

## Esquemas de Particiones

### Esquema 1: Estación de Trabajo para Desarrollo (256 GB SSD)

Ideal para desarrolladores con Docker, bases de datos locales y múltiples proyectos.

```
┌─────────────────────────────────────────────────────────────┐
│                    DISCO: 256 GB SSD                        │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ Partición │ Montaje   │ Tamaño  │ FS     │ Propósito       │
├───────────┼───────────┼─────────┼────────┼─────────────────┤
│ /dev/sda1 │ /boot/efi │  512 MB │ FAT32  │ Arranque UEFI   │
│ /dev/sda2 │ /boot     │  512 MB │ ext4   │ Kernel/initramfs│
│ /dev/sda3 │ /         │   25 GB │ ext4   │ Sistema raíz    │
│ /dev/sda4 │ /var      │   50 GB │ ext4   │ Docker, logs    │
│ /dev/sda5 │ /home     │ ~176 GB │ ext4   │ Datos usuario   │
│ /dev/sda6 │ swap      │    4 GB │ swap   │ Intercambio     │
└───────────┴───────────┴─────────┴────────┴─────────────────┘
```

**Justificación de tamaños:**
- `/boot/efi`: 512 MB (>100 MB mínimo, espacio para actualizaciones)
- `/boot`: 512 MB (>250 MB mínimo, permite múltiples kernels)
- `/`: 25 GB (>15 GB recomendado, espacio para aplicaciones)
- `/var`: 50 GB (Docker moderado según documentación)
- `/home`: Resto (~176 GB para proyectos y datos)
- `swap`: 4 GB (para 16 GB RAM sin hibernación: `sqrt(16)` ≈ 4)

---

### Esquema 2: Servidor de Producción (500 GB SSD)

Para servidores web, aplicaciones y bases de datos.

```
┌─────────────────────────────────────────────────────────────┐
│                    DISCO: 500 GB SSD                        │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ Partición │ Montaje   │ Tamaño  │ FS     │ Propósito       │
├───────────┼───────────┼─────────┼────────┼─────────────────┤
│ /dev/sda1 │ /boot/efi │    1 GB │ FAT32  │ Arranque UEFI   │
│ /dev/sda2 │ /boot     │    1 GB │ ext4   │ Kernel          │
│ /dev/sda3 │ /         │   25 GB │ ext4   │ Sistema raíz    │
│ /dev/sda4 │ /var      │  150 GB │ XFS    │ Docker, logs, DB│
│ /dev/sda5 │ /srv      │  150 GB │ XFS    │ Datos servicios │
│ /dev/sda6 │ /home     │   50 GB │ ext4   │ Usuarios admin  │
│ /dev/sda7 │ /tmp      │    8 GB │ ext4   │ Temporales      │
│ /dev/sda8 │ swap      │    8 GB │ swap   │ Intercambio     │
└───────────┴───────────┴─────────┴────────┴─────────────────┘
```

**Justificación:**
- `/var`: 150 GB (uso intensivo de Docker + logs + bases de datos)
- `/srv`: 150 GB (datos de servicios web separados)
- `/home`: 50 GB (servidores tienen pocos usuarios interactivos)
- `/tmp`: 8 GB (igual a swap según recomendación)
- `swap`: 8 GB (para 32 GB RAM sin hibernación)

---

### Esquema 3: Laptop con Dual Boot (512 GB SSD)

Windows + Ubuntu con datos compartidos.

```
┌─────────────────────────────────────────────────────────────┐
│                    DISCO: 512 GB SSD                        │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ Partición │ Montaje   │ Tamaño  │ FS     │ Propósito       │
├───────────┼───────────┼─────────┼────────┼─────────────────┤
│ /dev/sda1 │ EFI       │  512 MB │ FAT32  │ Compartido W+U  │
│ /dev/sda2 │ MSR       │   16 MB │ -      │ Microsoft       │
│ /dev/sda3 │ C:        │  200 GB │ NTFS   │ Windows         │
│ /dev/sda4 │ /boot     │  512 MB │ ext4   │ Kernel Ubuntu   │
│ /dev/sda5 │ /         │   25 GB │ ext4   │ Sistema Ubuntu  │
│ /dev/sda6 │ /home     │  170 GB │ ext4   │ Datos Ubuntu    │
│ /dev/sda7 │ Datos     │  100 GB │ NTFS   │ Compartido      │
│ /dev/sda8 │ swap      │   11 GB │ swap   │ Con hibernación │
└───────────┴───────────┴─────────┴────────┴─────────────────┘
```

**Notas:**
- EFI compartido entre Windows y Ubuntu
- `swap`: 11 GB para 8 GB RAM con hibernación (tabla oficial)
- Partición NTFS compartida para documentos accesibles desde ambos SO

---

### Esquema 4: Con LVM (Volúmenes Lógicos) - 1 TB

Máxima flexibilidad para redimensionar particiones.

```
┌─────────────────────────────────────────────────────────────┐
│                PARTICIONES FÍSICAS                          │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ /dev/sda1 │ /boot/efi │    1 GB │ FAT32  │ ESP             │
│ /dev/sda2 │ /boot     │    1 GB │ ext4   │ Fuera de LVM    │
│ /dev/sda3 │ LVM PV    │  ~998 GB│ LVM    │ Physical Volume │
└───────────┴───────────┴─────────┴────────┴─────────────────┘

┌─────────────────────────────────────────────────────────────┐
│         VOLÚMENES LÓGICOS (VG: vg_ubuntu)                   │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ lv_root   │ /         │   25 GB │ ext4   │ Sistema raíz    │
│ lv_var    │ /var      │  100 GB │ ext4   │ Docker, logs    │
│ lv_home   │ /home     │  300 GB │ ext4   │ Usuarios        │
│ lv_swap   │ swap      │    6 GB │ swap   │ Para 32GB RAM   │
│ [libre]   │ -         │ ~566 GB │ -      │ Expansión futura│
└───────────┴───────────┴─────────┴────────┴─────────────────┘
```

**Ventaja principal**: Espacio libre para expandir cualquier volumen sin reparticionar.

**Comandos LVM útiles:**

```bash
# Ver volúmenes
sudo lvs && sudo vgs && sudo pvs

# Expandir volumen (ejemplo: agregar 50GB a /var)
sudo lvextend -L +50G /dev/vg_ubuntu/lv_var
sudo resize2fs /dev/vg_ubuntu/lv_var

# Crear nuevo volumen
sudo lvcreate -L 100G -n lv_datos vg_ubuntu
sudo mkfs.ext4 /dev/vg_ubuntu/lv_datos
```

---

### Esquema 5: Con Cifrado LUKS

Para laptops o datos sensibles.

```
┌─────────────────────────────────────────────────────────────┐
│                PARTICIONES FÍSICAS                          │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ /dev/sda1 │ /boot/efi │  512 MB │ FAT32  │ Sin cifrar      │
│ /dev/sda2 │ /boot     │    1 GB │ ext4   │ Sin cifrar      │
│ /dev/sda3 │ LUKS      │  Resto  │ LUKS2  │ Contenedor      │
└───────────┴───────────┴─────────┴────────┴─────────────────┘

┌─────────────────────────────────────────────────────────────┐
│     Dentro de LUKS → LVM (VG: vg_crypt)                     │
├───────────┬───────────┬─────────┬────────┬─────────────────┤
│ lv_root   │ /         │   25 GB │ ext4   │ Cifrado         │
│ lv_home   │ /home     │  Resto  │ ext4   │ Cifrado         │
│ lv_swap   │ swap      │ RAM+2GB │ swap   │ Cifrado         │
└───────────┴───────────┴─────────┴────────┴─────────────────┘
```

**Nota**: `/boot` y `/boot/efi` deben estar sin cifrar para el arranque.

---

## Proceso de Instalación

### Paso 1: Iniciar desde USB

1. Insertar USB booteable
2. Reiniciar y entrar al menú de boot (F12, F2, ESC según fabricante)
3. Seleccionar USB UEFI
4. Elegir "Try or Install Ubuntu"

### Paso 2: Configuración inicial

1. Seleccionar idioma: **Español**
2. Seleccionar distribución de teclado
3. Conectar a red WiFi/Ethernet
4. Elegir tipo de instalación:
   - **Normal**: Incluye navegador, utilidades, juegos
   - **Mínima**: Solo sistema base y navegador

### Paso 3: Tipo de instalación

Seleccionar: **"Algo más"** (particionamiento manual)

### Paso 4: Crear tabla de particiones

Si es disco nuevo:
1. Seleccionar disco (`/dev/sda`)
2. Click en **"Nueva tabla de particiones..."**
3. Confirmar (se crea GPT en modo UEFI)

### Paso 5: Crear particiones

Para cada partición, click en **"+"**:

| Orden | Tamaño | Tipo | Sistema | Montaje |
|-------|--------|------|---------|---------|
| 1 | 512 MB | EFI | FAT32 | /boot/efi |
| 2 | 512 MB | - | ext4 | /boot |
| 3 | 25000 MB | - | ext4 | / |
| 4 | 50000 MB | - | ext4 | /var |
| 5 | Resto-4096 | - | ext4 | /home |
| 6 | 4096 MB | - | swap | - |

### Paso 6: Configurar bootloader

- **Dispositivo de arranque**: `/dev/sda` (disco completo)

### Paso 7: Completar

1. Click en **"Instalar ahora"**
2. Confirmar cambios
3. Zona horaria
4. Crear usuario y contraseña
5. Esperar y reiniciar

---

## Configuración Post-Instalación

### Actualizar sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

### Instalar drivers

```bash
sudo ubuntu-drivers autoinstall
```

### Optimizar swap (si RAM ≥ 8GB)

```bash
# Reducir swappiness (valor 10-20 para SSD)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Habilitar TRIM para SSD

```bash
sudo systemctl enable fstrim.timer
sudo systemctl start fstrim.timer
```

### Verificar montajes

```bash
df -h          # Ver espacio usado
lsblk          # Ver estructura de discos
cat /etc/fstab # Ver configuración de montaje
```

### Opciones de montaje recomendadas (/etc/fstab)

```bash
# Opciones optimizadas para SSD
UUID=xxx  /         ext4  defaults,noatime,errors=remount-ro  0  1
UUID=xxx  /var      ext4  defaults,noatime                    0  2
UUID=xxx  /home     ext4  defaults,noatime                    0  2
UUID=xxx  /tmp      ext4  defaults,noatime,nosuid,noexec      0  2
```

| Opción | Descripción |
|--------|-------------|
| `noatime` | No actualiza tiempo de acceso (mejora rendimiento SSD) |
| `noexec` | Prohibe ejecución de binarios (seguridad para /tmp) |
| `nosuid` | Ignora bits SUID/SGID (seguridad) |
| `errors=remount-ro` | Remonta solo lectura si hay errores |

---

## Referencias

- [Ubuntu DiskSpace Wiki](https://help.ubuntu.com/community/DiskSpace)
- [Ubuntu SwapFaq](https://help.ubuntu.com/community/SwapFaq)
- [Ubuntu PartitioningSchemes](https://help.ubuntu.com/community/PartitioningSchemes)
- [Docker Storage - Ubuntu Server](https://documentation.ubuntu.com/server/explanation/virtualisation/docker-storage-networking-and-logging/)
- [Ubuntu 24.04 Installation Guide](https://ubuntuhandbook.org/index.php/2024/04/install-ubuntu-24-04-desktop/)

---

*Guía basada en documentación oficial de Ubuntu para versión 24.04 LTS (Noble Numbat)*
