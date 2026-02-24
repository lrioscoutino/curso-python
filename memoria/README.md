# Unidad 4: Administración de Entrada/Salida

## Tutorial Teórico-Práctico basado en Linux/Ubuntu

> **Entorno de pruebas:** Ubuntu con kernel `6.14.0-37-generic`, SSD NVMe Micron 2210 512GB, AMD 16 cores.

---

## 4.1 Dispositivos y Manejadores de Dispositivos

### 4.1.1 Conceptos fundamentales

El **subsistema de E/S** es el intermediario entre el hardware (teclado, disco, red, etc.) y los procesos de usuario. Su objetivo principal es ofrecer una **interfaz uniforme** para que los programas accedan a dispositivos muy distintos de la misma forma.

El principio fundamental en Linux es: **"Todo es un archivo"**. Los dispositivos se representan como archivos especiales en `/dev` y se acceden con las mismas llamadas al sistema (`open`, `read`, `write`, `close`) que un archivo normal.

### 4.1.2 Clasificación de dispositivos

| Tipo | Descripción | Ejemplos | Acceso |
|------|-------------|----------|--------|
| **Bloque** | Datos en bloques de tamaño fijo, acceso aleatorio | Discos, SSDs, USBs | Buffered, cacheable |
| **Carácter** | Flujo de bytes secuencial, sin buffer del kernel | Teclado, mouse, terminales, puertos serie | Directo, sin cache |
| **Red** | Interfaz de red (no aparece en `/dev`) | eth0, wlan0 | Pila de red (sockets) |

### 4.1.3 Arquitectura por capas

```
+-----------------------------------+
|     Proceso de usuario            |  read(), write(), ioctl()
+-----------------------------------+
|     VFS (Virtual File System)     |  Interfaz uniforme
+-----------------------------------+
|     Driver del dispositivo        |  Codigo especifico del hardware
+-----------------------------------+
|     Controlador de hardware       |  Registros, DMA, interrupciones
+-----------------------------------+
|     Dispositivo fisico            |  El hardware real
+-----------------------------------+
```

**VFS (Virtual File System)** es la capa clave: permite que `read()` funcione igual para un archivo en disco, un teclado o un socket de red. El VFS traduce la llamada genérica a la función específica del driver correspondiente.

### 4.1.4 Identificación de dispositivos: Major y Minor numbers

Cada archivo de dispositivo en `/dev` tiene dos números:

- **Major number**: identifica al **driver** que maneja el dispositivo.
- **Minor number**: identifica al **dispositivo específico** dentro de ese driver.

```
Ejemplo:
  /dev/null  → major=1, minor=3  (driver "mem", dispositivo "null")
  /dev/zero  → major=1, minor=5  (driver "mem", dispositivo "zero")
  /dev/tty0  → major=4, minor=0  (driver "tty", terminal 0)
  /dev/tty1  → major=4, minor=1  (driver "tty", terminal 1)
```

Ambos comparten major=1 (mismo driver `mem`), pero distinto minor. Lo mismo con tty0 y tty1 (major=4).

### 4.1.5 Manejadores de dispositivos (Device Drivers)

Un **manejador de dispositivo** o **driver** es un módulo de software del kernel que:

1. Conoce los detalles de hardware específicos del dispositivo.
2. Exporta una interfaz estándar (`file_operations`) que el kernel invoca.
3. Se carga como módulo del kernel (`.ko`) o está compilado directamente en el kernel.

### 4.1.6 Practica: Explorar dispositivos del sistema

**Listar dispositivos de bloque:**

```bash
lsblk
```

Salida esperada:

```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0         7:0    0     4K  1 loop /snap/bare/5
nvme0n1     259:0    0 476,9G  0 disk
├─nvme0n1p1 259:1    0   512M  0 part /boot/efi
├─nvme0n1p2 259:2    0 475,5G  0 part /
└─nvme0n1p3 259:3    0   976M  0 part [SWAP]
```

Cada línea muestra el major:minor (`259:0`), tamaño y punto de montaje.

**Ver dispositivos de carácter importantes:**

```bash
ls -la /dev/null /dev/zero /dev/random /dev/urandom /dev/tty0
```

Salida esperada:

```
crw-rw-rw- 1 root root 1, 3 feb 24 08:18 /dev/null
crw-rw-rw- 1 root root 1, 8 feb 24 08:18 /dev/random
crw--w---- 1 root tty  4, 0 feb 24 08:18 /dev/tty0
crw-rw-rw- 1 root root 1, 9 feb 24 08:18 /dev/urandom
crw-rw-rw- 1 root root 1, 5 feb 24 08:18 /dev/zero
```

La primera letra indica el tipo: `c` = carácter, `b` = bloque. Los números después de `root` son major y minor.

**Dispositivos especiales importantes:**

```bash
# /dev/null - descarta todo lo que se escribe
echo "Hola mundo" > /dev/null   # nada se almacena

# /dev/zero - genera bytes nulos infinitos
dd if=/dev/zero bs=1 count=16 2>/dev/null | xxd
# 00000000: 0000 0000 0000 0000 0000 0000 0000 0000

# /dev/urandom - genera bytes aleatorios (nunca se bloquea)
dd if=/dev/urandom bs=1 count=16 2>/dev/null | xxd
# 00000000: 0df5 fc55 a1ed bfaf a2cc f11d 16fb e481
```

**Ver los módulos (drivers) cargados en el kernel:**

```bash
lsmod | head -20
```

Salida esperada:

```
Module                  Size  Used by
veth                   45056  0
nf_conntrack          200704  5 xt_conntrack,nf_nat,...
bridge                421888  0
e1000                 ...
```

**Ver información detallada de un driver:**

```bash
modinfo e1000
```

Salida:

```
filename:       /lib/modules/6.14.0-37-generic/kernel/drivers/net/ethernet/intel/e1000/e1000.ko.zst
license:        GPL v2
description:    Intel(R) PRO/1000 Network Driver
parm:           TxDescriptors:Number of transmit descriptors (array of int)
parm:           RxDescriptors:Number of receive descriptors (array of int)
parm:           Speed:Speed setting (array of int)
```

---

## 4.2 Mecanismos y Funciones de los Manejadores de Dispositivos

### 4.2.1 Mecanismos de E/S

Existen tres mecanismos fundamentales mediante los cuales la CPU se comunica con los dispositivos:

#### 1. E/S Programada (Polling)

```
+---------+           +------------+
|  CPU    |---lee---->| registro   |   La CPU pregunta constantemente:
|         |<--dato----| estado     |   "Ya hay dato? Ya hay dato?"
+---------+           +------------+   Desperdicia ciclos de CPU
```

- La CPU ejecuta un bucle verificando continuamente el registro de estado del dispositivo.
- **Ventaja**: implementación simple.
- **Desventaja**: desperdicia ciclos de CPU esperando (busy waiting).
- **Uso actual**: situaciones donde la espera es muy corta o en sistemas embebidos simples.

#### 2. E/S por Interrupciones

```
+---------+           +------------+
|  CPU    |<---IRQ----|  disposit  |   El dispositivo AVISA a la CPU
|         |---resp--->|            |   cuando tiene datos listos.
+---------+           +------------+   CPU libre entre interrupciones
```

- El dispositivo envía una señal de interrupción (IRQ) cuando necesita atención.
- La CPU ejecuta una **rutina de servicio de interrupción (ISR)** y luego retoma lo que estaba haciendo.
- **Ventaja**: la CPU no desperdicia ciclos esperando.
- **Desventaja**: hay overhead por cada interrupción (cambio de contexto).
- **Uso actual**: teclados, mouse, discos, tarjetas de red.

#### 3. DMA (Acceso Directo a Memoria)

```
+---------+  +-------+  +------------+
|  CPU    |  |  DMA  |--| dispositivo|  El controlador DMA transfiere
| (libre) |  |       |--|            |  datos directo a/desde RAM.
|         |  |       |--|            |  CPU solo configura y recibe
+---------+  +-------+  +------------+  una interrupcion al terminar
```

- Un controlador DMA dedicado realiza la transferencia de datos entre dispositivo y memoria RAM.
- La CPU solo configura la transferencia (dirección, tamaño) y recibe una interrupción al completarse.
- **Ventaja**: la CPU queda completamente libre durante la transferencia.
- **Desventaja**: requiere hardware DMA adicional.
- **Uso actual**: discos, tarjetas de red, GPU, audio, cualquier transferencia masiva de datos.

### 4.2.2 Funciones de un manejador de dispositivos

En Linux, un driver de carácter implementa la estructura `file_operations`:

```c
struct file_operations {
    int     (*open)    (struct inode *, struct file *);         // Abrir dispositivo
    int     (*release) (struct inode *, struct file *);         // Cerrar dispositivo
    ssize_t (*read)    (struct file *, char __user *, ...);     // Leer datos
    ssize_t (*write)   (struct file *, const char __user *, ...); // Escribir datos
    long    (*ioctl)   (struct file *, unsigned int, ...);      // Control especial
    loff_t  (*llseek)  (struct file *, loff_t, int);            // Mover posicion
    int     (*mmap)    (struct file *, struct vm_area_struct *);// Mapear a memoria
    unsigned int (*poll)(struct file *, struct poll_table_struct *); // Esperar eventos
};
```

Cada función tiene un rol específico:

| Funcion | Cuando se invoca | Qué hace |
|---------|-----------------|----------|
| `open` | Al hacer `open()` desde usuario | Inicializar dispositivo, asignar recursos |
| `release` | Al hacer `close()` | Liberar recursos, apagar dispositivo |
| `read` | Al hacer `read()` | Copiar datos del dispositivo al usuario |
| `write` | Al hacer `write()` | Copiar datos del usuario al dispositivo |
| `ioctl` | Al hacer `ioctl()` | Comandos especiales (ej: cambiar baudrate) |
| `llseek` | Al hacer `lseek()` | Cambiar posición de lectura (solo bloque) |
| `mmap` | Al hacer `mmap()` | Mapear memoria del dispositivo al proceso |
| `poll` | Al hacer `poll()`/`select()` | Verificar si hay datos disponibles |

### 4.2.3 Practica: Observar interrupciones del sistema

**Ver la tabla de interrupciones:**

```bash
cat /proc/interrupts | head -30
```

Salida esperada (fragmento):

```
            CPU0       CPU1       ...
   0:        138          0       IR-IO-APIC    2-edge      timer
   1:          0      12759       IR-IO-APIC    1-edge      i8042
  61:     103629          0       IR-PCI-MSIX   nvme0q1
  62:          0      79641       IR-PCI-MSIX   nvme0q2
```

Interpretación:
- **IRQ 0 (timer)**: reloj del sistema, 138 interrupciones en CPU0.
- **IRQ 1 (i8042)**: controlador de teclado, 12,759 interrupciones.
- **IRQ 61-64 (nvme)**: disco SSD NVMe, una cola por CPU (multiqueue).

**Observar interrupciones generadas por E/S real:**

```bash
# Conteo ANTES
grep nvme /proc/interrupts

# Generar E/S: escribir 10MB al disco
dd if=/dev/zero of=/tmp/test_io.bin bs=1M count=10
sync

# Conteo DESPUES
grep nvme /proc/interrupts

# Observar: los contadores de nvme incrementaron
```

Resultado real de la prueba:

```
ANTES: nvme0q1 → 103,629 interrupciones
DESPUES: nvme0q1 → 103,774 interrupciones
Diferencia: 145 interrupciones para escribir 10MB
```

El SSD NVMe usa **MSI-X** (Message Signaled Interrupts), una forma moderna de interrupciones que no usa líneas físicas sino escrituras a memoria.

**Ver puertos de E/S asignados:**

```bash
cat /proc/ioports | head -20
```

Salida:

```
0000-0000 : dma1
0000-0000 : pic1
0000-0000 : timer0
0000-0000 : keyboard
0000-0000 : rtc0
0000-0000 : dma2
```

**Ver uso de DMA:**

```bash
cat /proc/dma
```

> **Nota**: En hardware moderno, DMA se gestiona a través de IOMMU y no siempre aparece en `/proc/dma`.

---

## 4.3 Estructuras de Datos para Manejo de Dispositivos

### 4.3.1 Estructuras principales del kernel

El kernel de Linux mantiene varias estructuras de datos interconectadas para gestionar la E/S:

```
+-------------------------------------------------------------+
|                  ESTRUCTURAS PRINCIPALES                     |
+-------------------------------------------------------------+
|                                                              |
|  1. struct inode                                             |
|     +-- i_rdev         -> Major:Minor del dispositivo        |
|     +-- i_fop          -> Puntero a file_operations          |
|     +-- i_cdev/i_bdev  -> Puntero al device driver           |
|                                                              |
|  2. struct file  (una por cada open())                       |
|     +-- f_op           -> Operaciones del archivo/dispositivo|
|     +-- f_pos          -> Posicion actual de lectura/escrit. |
|     +-- f_flags        -> O_RDONLY, O_NONBLOCK, etc.         |
|     +-- private_data   -> Datos privados del driver          |
|                                                              |
|  3. struct cdev  (dispositivos de caracter)                  |
|     +-- ops            -> file_operations                    |
|     +-- dev            -> Numero major:minor                 |
|     +-- count          -> Cantidad de minor numbers          |
|                                                              |
|  4. struct gendisk  (dispositivos de bloque)                 |
|     +-- major, first_minor                                   |
|     +-- fops           -> block_device_operations            |
|     +-- queue          -> Cola de peticiones (request_queue)  |
|     +-- part[]         -> Tabla de particiones               |
|                                                              |
|  5. struct request_queue + struct request                    |
|     +-- Cola donde se encolan las peticiones de E/S          |
|         (el scheduler de E/S las reordena y fusiona)         |
|                                                              |
|  6. struct bio  (Block I/O)                                  |
|     +-- bi_sector      -> Sector destino en disco            |
|     +-- bi_size        -> Tamano de la transferencia         |
|     +-- bi_io_vec[]    -> Segmentos de memoria (scatter)     |
|                                                              |
+-------------------------------------------------------------+
```

### 4.3.2 Relación entre estructuras

Cuando un proceso hace `read()` a un archivo en disco, se activan estas estructuras en cadena:

```
Proceso -> read() -> VFS (struct file) -> Sistema de archivos (ext4)
    -> struct bio -> request_queue -> I/O Scheduler -> Driver -> Hardware
```

1. **struct file**: el proceso tiene un file descriptor que apunta a esta estructura.
2. **VFS**: consulta el inode para saber qué driver usar.
3. **struct bio**: describe la operación de E/S a nivel de bloques (sector, tamaño).
4. **request_queue**: encola y reordena las peticiones para optimizar acceso al disco.
5. **I/O Scheduler**: decide el orden de atención de las peticiones.
6. **Driver**: traduce la petición a comandos de hardware específicos.

### 4.3.3 Tabla de dispositivos registrados

El kernel mantiene tablas separadas para dispositivos de carácter y bloque:

```
  Tabla de Dispositivos de Caracter        Tabla de Dispositivos de Bloque
  (chrdevs[])                              (bdev_map[])
+--------+---------------+              +--------+---------------+
|Major 1 | mem driver    | -> null,zero |Major 7 | loop driver   |
|Major 4 | tty driver    | -> tty0,tty1 |Major 8 | sd driver     | -> sda
|Major 5 | console driver|              |Major259| nvme driver   | -> nvme0
|Major 10| misc driver   | -> varios    |  ...   |               |
+--------+---------------+              +--------+---------------+
```

### 4.3.4 Tabla de descriptores de archivo (por proceso)

Cada proceso tiene su propia tabla de file descriptors:

```
Proceso (PCB / task_struct)
  +-- files_struct
       +-- fd_array[]
            [0] -> struct file -> stdin  (teclado o pipe)
            [1] -> struct file -> stdout (terminal o archivo)
            [2] -> struct file -> stderr (terminal)
            [3] -> struct file -> /tmp/datos.txt
            [4] -> struct file -> socket TCP
            ...
```

Los file descriptors 0, 1 y 2 son estándar:
- **fd 0**: stdin (entrada estándar)
- **fd 1**: stdout (salida estándar)
- **fd 2**: stderr (salida de errores)

### 4.3.5 Buffer Cache

El kernel mantiene un **buffer cache** (page cache) en RAM que almacena copias de bloques del disco:

- Las lecturas primero buscan en cache; si no está, leen del disco y guardan en cache.
- Las escrituras van al cache y se sincronizan al disco periódicamente (`writeback`).
- Esto mejora drásticamente el rendimiento de E/S.

### 4.3.6 I/O Schedulers (Planificadores de E/S)

El I/O Scheduler reordena y fusiona peticiones en la `request_queue` para optimizar el acceso:

| Scheduler | Descripcion | Mejor para |
|-----------|-------------|------------|
| `none` (noop) | Sin reordenamiento | NVMe/SSD (acceso aleatorio rápido) |
| `mq-deadline` | Deadline por petición | SSD con requisitos de latencia |
| `bfq` | Budget Fair Queueing | HDD, escritorios interactivos |

### 4.3.7 Practica: Explorar las estructuras de datos

**Ver la tabla de drivers registrados:**

```bash
cat /proc/devices
```

Salida esperada:

```
Character devices:
  1 mem
  4 tty
  5 /dev/console
 10 misc
 13 input
180 usb
226 drm
240 nvme

Block devices:
  7 loop
  8 sd
252 device-mapper
259 blkext
```

Cada major number está vinculado a un driver. Múltiples minor numbers comparten el mismo major.

**Explorar sysfs - arbol jerárquico de dispositivos:**

```bash
# Clases de dispositivos
ls /sys/class/

# Dispositivos de bloque
ls /sys/block/

# Informacion del disco NVMe
cat /sys/block/nvme0n1/device/model
# Micron_2210_MTFDHBA512QFD
```

**Ver el I/O Scheduler actual:**

```bash
cat /sys/block/nvme0n1/queue/scheduler
# [none] mq-deadline
```

Los corchetes `[none]` indican el scheduler activo. Para NVMe, `none` es óptimo porque el acceso aleatorio es tan rápido como el secuencial.

**Estadísticas de E/S del disco:**

```bash
cat /sys/block/nvme0n1/stat
```

```
953781  406099  31782556  339678  639989  2048197  42108922  4466049  0  212610  4821606
```

Campos: reads_completed, reads_merged, sectors_read, ms_reading, writes_completed, writes_merged, sectors_written, ms_writing, ios_in_progress, ms_io, weighted_ms_io.

**Descriptores de archivo de un proceso:**

```bash
ls -la /proc/self/fd/
```

Salida:

```
lr-x------ 1 user user 64 ... 0 -> /dev/pts/0     (stdin)
l-wx------ 1 user user 64 ... 1 -> /dev/pts/0     (stdout)
l-wx------ 1 user user 64 ... 2 -> /dev/pts/0     (stderr)
```

**Tabla global de archivos abiertos:**

```bash
cat /proc/sys/fs/file-nr
# 18880    0    9223372036854775807
# abiertos  0    maximo
```

**Limite de archivos por proceso:**

```bash
ulimit -n
# 1048576
```

**Buffer cache del sistema:**

```bash
free -h
```

```
               total     usado     libre   compartido  buf/cache  disponible
Mem:            15Gi      12Gi     579Mi       220Mi      2,8Gi       3,0Gi
```

La columna `buf/cache` (2.8 GB) muestra la memoria usada como caché de E/S.

### 4.3.8 Tabla resumen de estructuras

| Estructura | Ubicacion en Linux | Proposito |
|---|---|---|
| Tabla de drivers | `/proc/devices` | Mapeo major -> driver |
| Arbol de dispositivos | `/sys/class/`, `/sys/block/` | Jerarquía completa de hw |
| File descriptors | `/proc/self/fd/` | FDs 0,1,2 + archivos abiertos |
| Tabla global de archivos | `/proc/sys/fs/file-nr` | Total de archivos abiertos en el sistema |
| Buffer cache | `free -h` (buff/cache) | Cache de E/S en RAM |
| Cola de E/S | `/sys/block/*/queue/scheduler` | Cola de reordenamiento de peticiones |
| Estadísticas de E/S | `/sys/block/*/stat` | Contadores de operaciones de E/S |

---

## 4.4 Operaciones de Entrada/Salida

### 4.4.1 Flujo de una operación de E/S

Cuando un proceso de usuario realiza una operación de E/S, esta atraviesa varias capas:

```
ESPACIO DE USUARIO                     ESPACIO DEL KERNEL
+----------------+                     +---------------------------------+
|                |   syscall           |                                 |
|  fd = open()   | ------------------> |  VFS: buscar inode              |
|                |                     |  -> asignar struct file         |
|                |                     |  -> llamar driver->open()       |
|                |                     |  -> retornar file descriptor    |
|                |   syscall           |                                 |
|  read(fd)      | ------------------> |  VFS: verificar permisos        |
|                |                     |  -> llamar driver->read()       |
|                |                     |    -> buffer cache (bloque)     |
|                |                     |    -> o directo (caracter)      |
|                |                     |  -> copiar datos a userspace    |
|                |   syscall           |                                 |
|  write(fd)     | ------------------> |  VFS: llamar driver->write()    |
|                |                     |  -> datos al buffer cache       |
|                |                     |  -> flush periodico a disco     |
|                |   syscall           |                                 |
|  ioctl(fd)     | ------------------> |  Comando especial al driver     |
|                |                     |  (ej: expulsar CD, baudrate)    |
|                |   syscall           |                                 |
|  close(fd)     | ------------------> |  Liberar struct file            |
|                |                     |  -> llamar driver->release()    |
+----------------+                     +---------------------------------+
```

### 4.4.2 Llamadas al sistema de E/S

#### open() - Abrir un dispositivo o archivo

```c
int fd = open("/dev/sda", O_RDONLY);
int fd = open("/tmp/datos.txt", O_CREAT | O_RDWR | O_TRUNC, 0644);
```

- Retorna un **file descriptor** (entero no negativo) o -1 en error.
- El kernel crea una `struct file`, la asocia al inode del dispositivo y llama a `driver->open()`.
- Flags comunes: `O_RDONLY`, `O_WRONLY`, `O_RDWR`, `O_CREAT`, `O_TRUNC`, `O_APPEND`, `O_NONBLOCK`.

#### read() - Leer datos

```c
ssize_t bytes = read(fd, buffer, 4096);
```

- Lee hasta N bytes del dispositivo al buffer del usuario.
- Retorna el número de bytes leídos, 0 si llegó al final (EOF), o -1 en error.
- Para dispositivos de bloque: los datos pueden venir del buffer cache.
- Para dispositivos de carácter: los datos vienen directamente del driver.

#### write() - Escribir datos

```c
ssize_t bytes = write(fd, datos, strlen(datos));
```

- Escribe N bytes del buffer del usuario al dispositivo.
- Para dispositivos de bloque: los datos van al buffer cache y se sincronizan después.
- Para `/dev/null`: se aceptan pero se descartan.

#### lseek() - Cambiar posición

```c
off_t pos = lseek(fd, 0, SEEK_SET);    // Ir al inicio
off_t pos = lseek(fd, 100, SEEK_CUR);  // Avanzar 100 bytes
off_t pos = lseek(fd, -10, SEEK_END);  // 10 bytes antes del final
```

- Solo tiene sentido para dispositivos de bloque y archivos regulares.
- Los dispositivos de carácter (teclado, terminal) no soportan `lseek`.

#### ioctl() - Comandos especiales

```c
unsigned long size;
ioctl(fd, BLKGETSIZE64, &size);  // Obtener tamano del disco en bytes
ioctl(fd, CDROM_EJECT, 0);       // Expulsar bandeja de CD
ioctl(fd, TCSETS, &termios);     // Configurar terminal (baudrate, etc.)
```

- Permite enviar comandos específicos que no encajan en read/write.
- Cada driver define sus propios códigos de ioctl.

#### close() - Cerrar y liberar

```c
int ret = close(fd);
```

- Libera la `struct file` y decrementa el contador de referencias del inode.
- Llama a `driver->release()` si es el último fd abierto para ese dispositivo.

### 4.4.3 Modos de E/S

```
+--------------------+  +--------------------+  +---------------------+
|  E/S BLOQUEANTE    |  | E/S NO BLOQUEANTE  |  |  E/S ASINCRONA      |
|  (por defecto)     |  |  (O_NONBLOCK)      |  |  (aio / io_uring)   |
|                    |  |                    |  |                     |
| read() espera      |  | read() retorna     |  | read() retorna      |
| hasta tener datos. |  | -EAGAIN si no hay  |  | inmediatamente.     |
|                    |  | datos disponibles. |  | Kernel notifica     |
| El proceso duerme. |  | El proceso debe    |  | cuando completa.    |
|                    |  | reintentar.        |  |                     |
| Simple pero puede  |  | Util con select()  |  | Ideal para alto     |
| desperdiciar CPU.  |  | o poll().          |  | rendimiento.        |
+--------------------+  +--------------------+  +---------------------+
```

- **Bloqueante**: el proceso se suspende hasta que hay datos. Es el comportamiento por defecto.
- **No bloqueante**: el proceso recibe un error `EAGAIN` si no hay datos y puede hacer otra cosa.
- **Asíncrona**: el proceso inicia la operación y continúa; el kernel notifica cuando termina.

### 4.4.4 Redirección de E/S en el shell

El shell manipula los file descriptors para redirigir E/S entre procesos y archivos:

```bash
comando > archivo       # stdout (fd 1) va al archivo
comando 2> archivo      # stderr (fd 2) va al archivo
comando < archivo       # stdin (fd 0) viene del archivo
comando 2>&1            # stderr va donde va stdout
comando | comando2      # pipe: stdout de cmd1 -> stdin de cmd2
```

Internamente, el shell usa las syscalls `dup2()` y `pipe()` para mover file descriptors.

### 4.4.5 Practica: Rastrear syscalls de E/S con strace

`strace` intercepta y muestra las llamadas al sistema que un proceso realiza:

```bash
strace -e trace=openat,read,write,close cat /tmp/test.txt
```

Salida:

```
openat(AT_FDCWD, "/tmp/test.txt", O_RDONLY) = 3
read(3, "Hola Sistemas Operativos\n", 131072) = 25
write(1, "Hola Sistemas Operativos\n", 25) = 25
read(3, "", 131072)                     = 0        # EOF
close(3)                                = 0
close(1)                                = 0
```

Interpretación:
1. `openat()` abre el archivo, retorna fd=3.
2. `read(3, ...)` lee 25 bytes del archivo.
3. `write(1, ...)` escribe esos 25 bytes a stdout (fd=1 = terminal).
4. `read(3, ...)` retorna 0 = fin de archivo (EOF).
5. `close(3)` y `close(1)` liberan los file descriptors.

### 4.4.6 Practica: Programa en C con todas las operaciones de E/S

```c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

int main() {
    int fd;
    char buffer[256];
    ssize_t bytes;
    struct stat st;

    // 1. OPEN - Abrir un archivo
    fd = open("/tmp/demo_io.txt", O_CREAT | O_RDWR | O_TRUNC, 0644);
    if (fd < 0) { perror("open"); return 1; }
    printf("open() -> fd = %d\n", fd);

    // 2. WRITE - Escribir datos
    const char *msg = "Hola desde la syscall write()!\n";
    bytes = write(fd, msg, strlen(msg));
    printf("write() -> %zd bytes escritos\n", bytes);

    // 3. LSEEK - Mover cursor al inicio
    lseek(fd, 0, SEEK_SET);
    printf("lseek() -> posicion = 0\n");

    // 4. READ - Leer datos
    memset(buffer, 0, sizeof(buffer));
    bytes = read(fd, buffer, sizeof(buffer) - 1);
    printf("read() -> %zd bytes: \"%s\"\n", bytes, buffer);

    // 5. FSTAT - Obtener metadatos
    fstat(fd, &st);
    printf("fstat() -> tamano=%ld, inode=%ld, device=(%d,%d)\n",
           (long)st.st_size, (long)st.st_ino,
           (int)(st.st_dev >> 8), (int)(st.st_dev & 0xFF));

    // 6. CLOSE - Cerrar
    close(fd);
    printf("close() -> recurso liberado\n");

    // 7. E/S con dispositivos
    fd = open("/dev/urandom", O_RDONLY);
    read(fd, buffer, 8);
    printf("read(/dev/urandom) -> ");
    for (int i = 0; i < 8; i++) printf("%02x", (unsigned char)buffer[i]);
    printf("\n");
    close(fd);

    fd = open("/dev/null", O_WRONLY);
    bytes = write(fd, "datos descartados", 17);
    printf("write(/dev/null) -> %zd bytes aceptados y descartados\n", bytes);
    close(fd);

    unlink("/tmp/demo_io.txt");
    return 0;
}
```

**Compilar y ejecutar:**

```bash
gcc -o io_operations io_operations.c
./io_operations
```

Salida esperada:

```
open() -> fd = 3
write() -> 31 bytes escritos
lseek() -> posicion = 0
read() -> 31 bytes: "Hola desde la syscall write()!
"
fstat() -> tamano=31, inode=6816316, device=(259,2)
close() -> recurso liberado
read(/dev/urandom) -> da1377908846bb4b
write(/dev/null) -> 17 bytes aceptados y descartados
```

### 4.4.7 Practica: E/S Bloqueante vs No Bloqueante en C

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main() {
    char buffer[256];
    int flags, n;

    // Activar modo NO BLOQUEANTE en stdin
    flags = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);

    printf("E/S No Bloqueante (O_NONBLOCK activado en stdin):\n");
    n = read(STDIN_FILENO, buffer, sizeof(buffer));

    if (n == -1 && errno == EAGAIN) {
        printf("read() retorno -1 con errno=EAGAIN (%s)\n", strerror(errno));
        printf("Significado: no hay datos, intenta despues.\n");
        printf("El proceso NO se bloqueo.\n");
    } else if (n > 0) {
        printf("Se leyeron %d bytes\n", n);
    }

    // Restaurar stdin
    fcntl(STDIN_FILENO, F_SETFL, flags);
    return 0;
}
```

### 4.4.8 Practica: Monitoreo de E/S en tiempo real

**Con iostat:**

```bash
iostat -x 1 3
```

Muestra estadísticas extendidas de E/S por dispositivo cada segundo, 3 veces.

**Con /proc/self/io (por proceso):**

```bash
cat /proc/self/io
```

```
rchar: 4092           # bytes leidos (incluye cache)
wchar: 0              # bytes escritos (incluye cache)
syscr: 9              # llamadas read()
syscw: 0              # llamadas write()
read_bytes: 0         # bytes realmente leidos de disco
write_bytes: 0        # bytes realmente escritos a disco
```

La diferencia entre `rchar` y `read_bytes` muestra cuánto se sirvió desde el cache.

---

## Resumen General

### 4.1 - Dispositivos y Manejadores

| Concepto | Comando para explorar | Que aprendimos |
|---|---|---|
| Tipos de dispositivo | `ls -la /dev/` | `b` = bloque, `c` = caracter |
| Major:Minor numbers | `ls -la /dev/null /dev/zero` | Major identifica al driver, minor al dispositivo |
| Drivers cargados | `lsmod` | Modulos del kernel activos |
| Info de un driver | `modinfo e1000` | Licencia, parametros, alias PCI |

### 4.2 - Mecanismos y Funciones

| Mecanismo | Caracteristicas | Ejemplo en el sistema |
|---|---|---|
| **Polling** | CPU pregunta constantemente | Poco usado en Linux moderno |
| **Interrupciones** | Dispositivo avisa a la CPU | `/proc/interrupts` -> nvme, i8042 |
| **DMA** | Transferencia directa HW<->RAM | Discos, tarjetas de red, GPU |
| **file_operations** | Interfaz del driver | open, read, write, ioctl, close |

### 4.3 - Estructuras de Datos

| Estructura | Ubicacion real | Proposito |
|---|---|---|
| Tabla de drivers | `/proc/devices` | Mapeo major -> driver |
| sysfs | `/sys/class/`, `/sys/block/` | Arbol jerarquico de dispositivos |
| File descriptors | `/proc/self/fd/` | Tabla de archivos abiertos por proceso |
| Buffer cache | `free -h` (buff/cache) | Cache de E/S en RAM |
| I/O scheduler | `/sys/block/*/queue/scheduler` | Cola de reordenamiento de peticiones |

### 4.4 - Operaciones de E/S

| Syscall | Funcion | Ejemplo |
|---|---|---|
| `open()` | Abrir dispositivo/archivo -> retorna fd | `fd = open("/dev/sda", O_RDONLY)` |
| `read()` | Leer bytes del dispositivo | `read(fd, buffer, 4096)` |
| `write()` | Escribir bytes al dispositivo | `write(fd, datos, len)` |
| `lseek()` | Mover posicion (solo bloque) | `lseek(fd, 0, SEEK_SET)` |
| `ioctl()` | Comando especial al driver | `ioctl(fd, BLKGETSIZE64, &size)` |
| `close()` | Liberar el file descriptor | `close(fd)` |
| `mmap()` | Mapear dispositivo a memoria | Usado por GPU, framebuffer |

### Comandos clave para explorar E/S en Ubuntu

```bash
lsblk                              # Dispositivos de bloque
ls -la /dev/                       # Todos los dispositivos
cat /proc/devices                  # Tabla major -> driver
cat /proc/interrupts               # Interrupciones por CPU
lsmod                              # Drivers cargados
modinfo <driver>                   # Info de un driver
cat /sys/block/<dev>/queue/scheduler  # I/O Scheduler
cat /sys/block/<dev>/stat          # Estadisticas de E/S
ls -la /proc/self/fd/              # File descriptors del proceso
cat /proc/self/io                  # E/S del proceso actual
cat /proc/sys/fs/file-nr           # Archivos abiertos en el sistema
free -h                            # Buffer cache
iostat -x 1                        # Monitoreo de E/S en tiempo real
strace -e trace=read,write <cmd>   # Rastrear syscalls de E/S
```
