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
  /dev/null  -> major=1, minor=3  (driver "mem", dispositivo "null")
  /dev/zero  -> major=1, minor=5  (driver "mem", dispositivo "zero")
  /dev/tty0  -> major=4, minor=0  (driver "tty", terminal 0)
  /dev/tty1  -> major=4, minor=1  (driver "tty", terminal 1)
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

| Funcion | Cuando se invoca | Que hace |
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
ANTES: nvme0q1 -> 103,629 interrupciones
DESPUES: nvme0q1 -> 103,774 interrupciones
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
| `none` (noop) | Sin reordenamiento | NVMe/SSD (acceso aleatorio rapido) |
| `mq-deadline` | Deadline por peticion | SSD con requisitos de latencia |
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

**Explorar sysfs - arbol jerarquico de dispositivos:**

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

Los corchetes `[none]` indican el scheduler activo. Para NVMe, `none` es optimo porque el acceso aleatorio es tan rapido como el secuencial.

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

La columna `buf/cache` (2.8 GB) muestra la memoria usada como cache de E/S.

### 4.3.8 Tabla resumen de estructuras

| Estructura | Ubicacion en Linux | Proposito |
|---|---|---|
| Tabla de drivers | `/proc/devices` | Mapeo major -> driver |
| Arbol de dispositivos | `/sys/class/`, `/sys/block/` | Jerarquia completa de hw |
| File descriptors | `/proc/self/fd/` | Tabla de archivos abiertos por proceso |
| Tabla global de archivos | `/proc/sys/fs/file-nr` | Total de archivos abiertos en el sistema |
| Buffer cache | `free -h` (buff/cache) | Cache de E/S en RAM |
| Cola de E/S | `/sys/block/*/queue/scheduler` | Cola de reordenamiento de peticiones |
| Estadisticas de E/S | `/sys/block/*/stat` | Contadores de operaciones de E/S |

---

## 4.4 Operaciones de Entrada/Salida

### 4.4.1 Flujo de una operacion de E/S

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
- Retorna el numero de bytes leidos, 0 si llego al final (EOF), o -1 en error.
- Para dispositivos de bloque: los datos pueden venir del buffer cache.
- Para dispositivos de caracter: los datos vienen directamente del driver.

#### write() - Escribir datos

```c
ssize_t bytes = write(fd, datos, strlen(datos));
```

- Escribe N bytes del buffer del usuario al dispositivo.
- Para dispositivos de bloque: los datos van al buffer cache y se sincronizan despues.
- Para `/dev/null`: se aceptan pero se descartan.

#### lseek() - Cambiar posicion

```c
off_t pos = lseek(fd, 0, SEEK_SET);    // Ir al inicio
off_t pos = lseek(fd, 100, SEEK_CUR);  // Avanzar 100 bytes
off_t pos = lseek(fd, -10, SEEK_END);  // 10 bytes antes del final
```

- Solo tiene sentido para dispositivos de bloque y archivos regulares.
- Los dispositivos de caracter (teclado, terminal) no soportan `lseek`.

#### ioctl() - Comandos especiales

```c
unsigned long size;
ioctl(fd, BLKGETSIZE64, &size);  // Obtener tamano del disco en bytes
ioctl(fd, CDROM_EJECT, 0);       // Expulsar bandeja de CD
ioctl(fd, TCSETS, &termios);     // Configurar terminal (baudrate, etc.)
```

- Permite enviar comandos especificos que no encajan en read/write.
- Cada driver define sus propios codigos de ioctl.

#### close() - Cerrar y liberar

```c
int ret = close(fd);
```

- Libera la `struct file` y decrementa el contador de referencias del inode.
- Llama a `driver->release()` si es el ultimo fd abierto para ese dispositivo.

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
- **Asincrona**: el proceso inicia la operacion y continua; el kernel notifica cuando termina.

### 4.4.4 Redireccion de E/S en el shell

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

Interpretacion:
1. `openat()` abre el archivo, retorna fd=3.
2. `read(3, ...)` lee 25 bytes del archivo.
3. `write(1, ...)` escribe esos 25 bytes a stdout (fd=1 = terminal).
4. `read(3, ...)` retorna 0 = fin de archivo (EOF).
5. `close(3)` y `close(1)` liberan los file descriptors.

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

---

## Practicas Resueltas en Python

### Practica 1: Explorador de Dispositivos y Estructuras de E/S del Sistema

**Objetivo**: Escribir un programa en Python que inspeccione `/proc` y `/sys` para obtener
informacion en tiempo real sobre dispositivos, drivers, interrupciones, file descriptors
y el buffer cache del sistema, presentando un reporte completo.

**Conceptos que aplica**: Secciones 4.1 (tipos de dispositivos, major/minor),
4.2 (interrupciones), 4.3 (estructuras de datos: tabla de drivers, sysfs, fd table,
buffer cache, I/O scheduler).

#### Codigo fuente: `practica1_explorador_io.py`

```python
#!/usr/bin/env python3
"""
Practica 1: Explorador de Dispositivos y Estructuras de E/S del Sistema
=========================================================================
Inspecciona /proc y /sys para generar un reporte completo del subsistema
de E/S del sistema operativo Linux.

Conceptos demostrados:
  - 4.1: Clasificacion de dispositivos (bloque vs caracter), major/minor numbers
  - 4.2: Tabla de interrupciones, mecanismos de E/S (IRQ, MSI-X)
  - 4.3: Tabla de drivers (/proc/devices), sysfs (/sys/block),
          file descriptors (/proc/self/fd), buffer cache, I/O scheduler
"""

import os
import stat


def separador(titulo):
    """Imprime un separador visual con titulo."""
    ancho = 70
    print("\n" + "=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)


# =========================================================================
# SECCION 1: Dispositivos en /dev (tema 4.1)
# =========================================================================
# En Linux cada dispositivo tiene un archivo especial en /dev.
# La funcion os.stat() retorna el campo st_rdev que contiene
# el major y minor number empaquetados. Con os.major() y os.minor()
# los extraemos. El tipo se determina con stat.S_ISBLK / stat.S_ISCHR.
# =========================================================================

def explorar_dispositivos():
    """Lee /dev y clasifica dispositivos en bloque y caracter."""
    separador("1. DISPOSITIVOS EN /dev (tema 4.1)")
    print("Cada dispositivo tiene un major:minor number.")
    print("Major = driver, Minor = dispositivo especifico.\n")

    dispositivos_bloque = []
    dispositivos_caracter = []

    # Dispositivos representativos para no listar los cientos que hay
    nombres_interes = [
        "null", "zero", "random", "urandom",       # Caracter - memoria
        "tty0", "tty1", "console",                  # Caracter - terminales
        "sda", "sda1", "sda2",                      # Bloque - disco SCSI/SATA
        "nvme0n1", "nvme0n1p1", "nvme0n1p2",        # Bloque - disco NVMe
        "loop0", "loop1",                            # Bloque - loop devices
    ]

    for nombre in nombres_interes:
        ruta = f"/dev/{nombre}"
        if not os.path.exists(ruta):
            continue
        try:
            info = os.stat(ruta)
            modo = info.st_mode
            major = os.major(info.st_rdev)
            minor = os.minor(info.st_rdev)

            if stat.S_ISBLK(modo):
                dispositivos_bloque.append((nombre, major, minor))
            elif stat.S_ISCHR(modo):
                dispositivos_caracter.append((nombre, major, minor))
        except PermissionError:
            continue

    print(f"{'Dispositivo':<20} {'Tipo':<12} {'Major':<8} {'Minor':<8}")
    print("-" * 48)

    for nombre, major, minor in dispositivos_caracter:
        print(f"/dev/{nombre:<16} {'Caracter':<12} {major:<8} {minor:<8}")

    for nombre, major, minor in dispositivos_bloque:
        print(f"/dev/{nombre:<16} {'Bloque':<12} {major:<8} {minor:<8}")

    print(f"\nTotal: {len(dispositivos_caracter)} de caracter, "
          f"{len(dispositivos_bloque)} de bloque")

    # Explicacion de lo observado
    print("\n--- Analisis ---")
    # Agrupar por major para mostrar que comparten driver
    majors_car = {}
    for nombre, major, minor in dispositivos_caracter:
        majors_car.setdefault(major, []).append(nombre)
    for major, nombres in majors_car.items():
        if len(nombres) > 1:
            print(f"  Major {major} agrupa a: {', '.join(nombres)} (mismo driver)")


# =========================================================================
# SECCION 2: Tabla de drivers registrados /proc/devices (tema 4.3)
# =========================================================================
# /proc/devices es la tabla que el kernel expone con todos los drivers
# registrados. Cada linea tiene el major number y el nombre del driver.
# Esta es la estructura chrdevs[] y bdev_map[] del kernel.
# =========================================================================

def explorar_drivers():
    """Parsea /proc/devices para mostrar la tabla de drivers."""
    separador("2. TABLA DE DRIVERS REGISTRADOS /proc/devices (tema 4.3)")
    print("El kernel mantiene tablas separadas para drivers de bloque y caracter.\n")

    drivers_caracter = []
    drivers_bloque = []
    seccion = None

    with open("/proc/devices", "r") as f:
        for linea in f:
            linea = linea.strip()
            if linea == "Character devices:":
                seccion = "caracter"
                continue
            elif linea == "Block devices:":
                seccion = "bloque"
                continue
            elif not linea:
                continue

            partes = linea.split(None, 1)
            if len(partes) == 2:
                major, nombre = int(partes[0]), partes[1]
                if seccion == "caracter":
                    drivers_caracter.append((major, nombre))
                elif seccion == "bloque":
                    drivers_bloque.append((major, nombre))

    print(f"  Drivers de CARACTER registrados: {len(drivers_caracter)}")
    print(f"  Drivers de BLOQUE registrados:   {len(drivers_bloque)}")

    print(f"\n  {'Major':<8} {'Driver':<25} {'Tipo'}")
    print("  " + "-" * 45)
    # Mostrar algunos representativos
    for major, nombre in drivers_caracter[:10]:
        print(f"  {major:<8} {nombre:<25} {'Caracter'}")
    if len(drivers_caracter) > 10:
        print(f"  ... y {len(drivers_caracter) - 10} mas")

    print()
    for major, nombre in drivers_bloque[:8]:
        print(f"  {major:<8} {nombre:<25} {'Bloque'}")
    if len(drivers_bloque) > 8:
        print(f"  ... y {len(drivers_bloque) - 8} mas")


# =========================================================================
# SECCION 3: Interrupciones /proc/interrupts (tema 4.2)
# =========================================================================
# Las interrupciones son el mecanismo principal de E/S en Linux moderno.
# Cada linea de /proc/interrupts muestra: numero IRQ, conteo por CPU,
# tipo de controlador (IO-APIC, PCI-MSI, etc.) y el dispositivo.
# =========================================================================

def explorar_interrupciones():
    """Lee /proc/interrupts y muestra las mas activas."""
    separador("3. INTERRUPCIONES DEL SISTEMA /proc/interrupts (tema 4.2)")
    print("Las interrupciones (IRQ) permiten que los dispositivos avisen a la CPU")
    print("cuando tienen datos listos, sin que la CPU haga polling.\n")

    interrupciones = []

    with open("/proc/interrupts", "r") as f:
        encabezado = f.readline()  # Linea con nombres de CPUs
        num_cpus = len(encabezado.split())

        for linea in f:
            partes = linea.split()
            if not partes:
                continue

            irq = partes[0].rstrip(":")

            # Extraer conteos por CPU (son los numeros despues del IRQ)
            conteos = []
            for p in partes[1:]:
                if p.isdigit():
                    conteos.append(int(p))
                else:
                    break

            total = sum(conteos)
            # El resto de la linea es la descripcion (tipo + nombre)
            descripcion = " ".join(partes[1 + len(conteos):])
            interrupciones.append((irq, total, descripcion))

    # Ordenar por total de interrupciones (mas activas primero)
    interrupciones.sort(key=lambda x: x[1], reverse=True)

    print(f"  CPUs detectadas: {num_cpus}")
    print(f"  Total de lineas IRQ: {len(interrupciones)}\n")
    print(f"  {'IRQ':<8} {'Total':<15} {'Dispositivo/Tipo'}")
    print("  " + "-" * 60)

    for irq, total, desc in interrupciones[:15]:
        if total > 0:
            print(f"  {irq:<8} {total:<15,} {desc}")

    total_global = sum(t for _, t, _ in interrupciones)
    print(f"\n  Total de interrupciones en el sistema: {total_global:,}")


# =========================================================================
# SECCION 4: Dispositivos de bloque y su I/O Scheduler (tema 4.3)
# =========================================================================
# /sys/block/ contiene un directorio por cada dispositivo de bloque.
# Dentro de cada uno, queue/scheduler muestra el planificador de E/S
# y stat muestra las estadisticas de operaciones de lectura/escritura.
# =========================================================================

def explorar_bloques_sysfs():
    """Explora /sys/block para obtener info de dispositivos de bloque."""
    separador("4. DISPOSITIVOS DE BLOQUE - sysfs (tema 4.3)")
    print("sysfs (/sys) expone la jerarquia de dispositivos del kernel.")
    print("Aqui vemos el I/O scheduler y estadisticas de cada disco.\n")

    try:
        dispositivos = sorted(os.listdir("/sys/block"))
    except FileNotFoundError:
        print("  /sys/block no disponible")
        return

    # Filtrar solo discos reales (no loop)
    discos = [d for d in dispositivos if not d.startswith("loop")]

    for disco in discos:
        ruta_base = f"/sys/block/{disco}"
        print(f"  Dispositivo: /dev/{disco}")

        # Modelo
        ruta_modelo = f"{ruta_base}/device/model"
        if os.path.exists(ruta_modelo):
            with open(ruta_modelo) as f:
                print(f"    Modelo: {f.read().strip()}")

        # Tamano (en sectores de 512 bytes)
        ruta_size = f"{ruta_base}/size"
        if os.path.exists(ruta_size):
            with open(ruta_size) as f:
                sectores = int(f.read().strip())
                gb = (sectores * 512) / (1024 ** 3)
                print(f"    Tamano: {gb:.1f} GB ({sectores:,} sectores)")

        # I/O Scheduler
        ruta_sched = f"{ruta_base}/queue/scheduler"
        if os.path.exists(ruta_sched):
            with open(ruta_sched) as f:
                sched = f.read().strip()
                print(f"    I/O Scheduler: {sched}")

        # Estadisticas de E/S
        ruta_stat = f"{ruta_base}/stat"
        if os.path.exists(ruta_stat):
            with open(ruta_stat) as f:
                campos = f.read().split()
                if len(campos) >= 11:
                    reads = int(campos[0])
                    sectors_read = int(campos[2])
                    writes = int(campos[4])
                    sectors_written = int(campos[6])
                    mb_read = (sectors_read * 512) / (1024 ** 2)
                    mb_written = (sectors_written * 512) / (1024 ** 2)
                    print(f"    Lecturas completadas:  {reads:>10,}  ({mb_read:,.0f} MB)")
                    print(f"    Escrituras completadas: {writes:>9,}  ({mb_written:,.0f} MB)")

        print()

    # Mostrar cuantos loop devices hay
    loops = [d for d in dispositivos if d.startswith("loop")]
    print(f"  Ademas hay {len(loops)} dispositivos loop (para snaps, imagenes ISO, etc.)")


# =========================================================================
# SECCION 5: File descriptors del proceso actual (tema 4.3)
# =========================================================================
# Cada proceso tiene su tabla de file descriptors en /proc/self/fd/.
# Cada entrada es un symlink al archivo/dispositivo/socket abierto.
# fd 0=stdin, 1=stdout, 2=stderr son siempre los primeros tres.
# =========================================================================

def explorar_file_descriptors():
    """Muestra los file descriptors abiertos por este proceso."""
    separador("5. FILE DESCRIPTORS DEL PROCESO ACTUAL (tema 4.3)")
    print("Cada proceso tiene una tabla de file descriptors (fd).")
    print("fd 0=stdin, 1=stdout, 2=stderr son estandar.\n")

    ruta_fd = "/proc/self/fd"
    fds = []

    for entrada in sorted(os.listdir(ruta_fd), key=lambda x: int(x)):
        try:
            destino = os.readlink(f"{ruta_fd}/{entrada}")
            fds.append((int(entrada), destino))
        except OSError:
            fds.append((int(entrada), "(no se pudo leer)"))

    print(f"  {'FD':<6} {'Destino'}")
    print("  " + "-" * 50)
    for fd_num, destino in fds:
        etiqueta = ""
        if fd_num == 0:
            etiqueta = " <- stdin"
        elif fd_num == 1:
            etiqueta = " <- stdout"
        elif fd_num == 2:
            etiqueta = " <- stderr"
        print(f"  {fd_num:<6} {destino}{etiqueta}")

    print(f"\n  Total de file descriptors abiertos: {len(fds)}")

    # Limite por proceso
    try:
        import resource
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(f"  Limite de fd por proceso: {soft:,} (soft) / {hard:,} (hard)")
    except ImportError:
        pass

    # Tabla global del sistema
    try:
        with open("/proc/sys/fs/file-nr") as f:
            partes = f.read().split()
            print(f"  Archivos abiertos en TODO el sistema: {int(partes[0]):,}")
    except FileNotFoundError:
        pass


# =========================================================================
# SECCION 6: Buffer Cache - memoria usada como cache de E/S (tema 4.3)
# =========================================================================
# /proc/meminfo tiene las estadisticas de memoria del kernel.
# Buffers = cache de metadatos de bloque
# Cached  = page cache (datos de archivos leidos/escritos)
# Juntos forman el "buffer cache" que acelera la E/S.
# =========================================================================

def explorar_buffer_cache():
    """Muestra el estado del buffer cache del sistema."""
    separador("6. BUFFER CACHE DEL SISTEMA (tema 4.3)")
    print("El kernel usa RAM libre como cache de E/S para acelerar lecturas")
    print("y escrituras a disco.\n")

    meminfo = {}
    with open("/proc/meminfo") as f:
        for linea in f:
            partes = linea.split(":")
            if len(partes) == 2:
                clave = partes[0].strip()
                valor = partes[1].strip().split()[0]  # Solo el numero
                meminfo[clave] = int(valor)  # En kB

    total = meminfo.get("MemTotal", 0) / (1024 * 1024)
    libre = meminfo.get("MemFree", 0) / (1024 * 1024)
    disponible = meminfo.get("MemAvailable", 0) / (1024 * 1024)
    buffers = meminfo.get("Buffers", 0) / 1024
    cached = meminfo.get("Cached", 0) / 1024
    dirty = meminfo.get("Dirty", 0)  # kB

    print(f"  Memoria total:       {total:.1f} GB")
    print(f"  Memoria libre:       {libre:.1f} GB")
    print(f"  Memoria disponible:  {disponible:.1f} GB")
    print(f"  Buffers (metadatos): {buffers:.0f} MB")
    print(f"  Cached (page cache): {cached:.0f} MB")
    print(f"  Total buffer+cache:  {buffers + cached:.0f} MB")
    print(f"  Dirty (sin sync):    {dirty} kB")

    if total > 0:
        pct = ((buffers + cached) / (total * 1024)) * 100
        print(f"\n  El {pct:.1f}% de la RAM se usa como cache de E/S.")
        print("  Esto acelera las lecturas repetidas (no van a disco).")


# =========================================================================
# MAIN - Ejecutar todas las secciones
# =========================================================================

def main():
    print("+" + "=" * 68 + "+")
    print("|  PRACTICA 1: Explorador de Dispositivos y Estructuras de E/S     |")
    print("|  Sistemas Operativos - Unidad 4                                  |")
    print("+" + "=" * 68 + "+")

    explorar_dispositivos()        # 4.1
    explorar_drivers()             # 4.3
    explorar_interrupciones()      # 4.2
    explorar_bloques_sysfs()       # 4.3
    explorar_file_descriptors()    # 4.3
    explorar_buffer_cache()        # 4.3

    separador("FIN DEL REPORTE")
    print("Todos los datos fueron leidos directamente de /proc y /sys.")
    print("Estas son las mismas estructuras que el kernel usa internamente")
    print("para administrar la E/S del sistema.\n")


if __name__ == "__main__":
    main()
```

#### Ejecucion

```bash
python3 practica1_explorador_io.py
```

#### Salida esperada

```
+====================================================================+
|  PRACTICA 1: Explorador de Dispositivos y Estructuras de E/S       |
|  Sistemas Operativos - Unidad 4                                    |
+====================================================================+

======================================================================
  1. DISPOSITIVOS EN /dev (tema 4.1)
======================================================================
Cada dispositivo tiene un major:minor number.
Major = driver, Minor = dispositivo especifico.

Dispositivo          Tipo         Major    Minor
------------------------------------------------
/dev/null            Caracter     1        3
/dev/zero            Caracter     1        5
/dev/random          Caracter     1        8
/dev/urandom         Caracter     1        9
/dev/tty0            Caracter     4        0
/dev/tty1            Caracter     4        1
/dev/console         Caracter     5        1
/dev/nvme0n1         Bloque       259      0
/dev/nvme0n1p1       Bloque       259      1
/dev/nvme0n1p2       Bloque       259      2
/dev/loop0           Bloque       7        0
/dev/loop1           Bloque       7        1

Total: 7 de caracter, 5 de bloque

--- Analisis ---
  Major 1 agrupa a: null, zero, random, urandom (mismo driver)
  Major 4 agrupa a: tty0, tty1 (mismo driver)

======================================================================
  2. TABLA DE DRIVERS REGISTRADOS /proc/devices (tema 4.3)
======================================================================
El kernel mantiene tablas separadas para drivers de bloque y caracter.

  Drivers de CARACTER registrados: 38
  Drivers de BLOQUE registrados:   15

  Major    Driver                    Tipo
  ---------------------------------------------
  1        mem                       Caracter
  4        /dev/vc/0                 Caracter
  4        tty                       Caracter
  5        /dev/tty                  Caracter
  5        /dev/console              Caracter
  10       misc                      Caracter
  13       input                     Caracter
  ...

======================================================================
  3. INTERRUPCIONES DEL SISTEMA /proc/interrupts (tema 4.2)
======================================================================
Las interrupciones (IRQ) permiten que los dispositivos avisen a la CPU
cuando tienen datos listos, sin que la CPU haga polling.

  CPUs detectadas: 16
  Total de lineas IRQ: 68

  IRQ      Total           Dispositivo/Tipo
  ------------------------------------------------------------
  131      4,582,901       IR-PCI-MSIX-0000:04:00.0 amdgpu
  61       103,774         IR-PCI-MSIX-0000:02:00.0 nvme0q1
  62       79,669          IR-PCI-MSIX-0000:02:00.0 nvme0q2
  1        12,769          IR-IO-APIC 1-edge i8042
  ...

  Total de interrupciones en el sistema: 5,234,021

======================================================================
  4. DISPOSITIVOS DE BLOQUE - sysfs (tema 4.3)
======================================================================
  Dispositivo: /dev/nvme0n1
    Modelo: Micron_2210_MTFDHBA512QFD
    Tamano: 476.9 GB (1,000,215,216 sectores)
    I/O Scheduler: [none] mq-deadline
    Lecturas completadas:     953,781  (15,518 MB)
    Escrituras completadas:   639,989  (20,565 MB)

======================================================================
  5. FILE DESCRIPTORS DEL PROCESO ACTUAL (tema 4.3)
======================================================================
  FD     Destino
  --------------------------------------------------
  0      /dev/pts/0 <- stdin
  1      /dev/pts/0 <- stdout
  2      /dev/pts/0 <- stderr

  Total de file descriptors abiertos: 3
  Limite de fd por proceso: 1,048,576 (soft)
  Archivos abiertos en TODO el sistema: 18,880

======================================================================
  6. BUFFER CACHE DEL SISTEMA (tema 4.3)
======================================================================
  Memoria total:       15.5 GB
  Memoria libre:       0.6 GB
  Memoria disponible:  3.0 GB
  Buffers (metadatos): 198 MB
  Cached (page cache): 2,605 MB
  Total buffer+cache:  2,803 MB
  Dirty (sin sync):    48 kB

  El 17.6% de la RAM se usa como cache de E/S.
```

---

### Practica 2: Operaciones de E/S con Dispositivos y Benchmark de Rendimiento

**Objetivo**: Realizar operaciones reales de E/S sobre archivos y dispositivos de Linux
(`/dev/null`, `/dev/zero`, `/dev/urandom`), medir el rendimiento de E/S secuencial vs
aleatoria, demostrar E/S bloqueante vs no bloqueante, y verificar el efecto del buffer
cache comparando lecturas en frio y en caliente.

**Conceptos que aplica**: Seccion 4.1 (dispositivos de caracter),
4.2 (polling vs interrupciones, DMA), 4.3 (buffer cache, I/O scheduler),
4.4 (open, read, write, lseek, close, modos de E/S bloqueante/no bloqueante).

#### Codigo fuente: `practica2_operaciones_io.py`

```python
#!/usr/bin/env python3
"""
Practica 2: Operaciones de E/S con Dispositivos y Benchmark de Rendimiento
===========================================================================
Realiza operaciones de E/S sobre archivos y dispositivos reales de Linux,
midiendo rendimiento y demostrando los conceptos de la Unidad 4.

Conceptos demostrados:
  - 4.1: Lectura/escritura a dispositivos de caracter (/dev/null, /dev/zero, /dev/urandom)
  - 4.2: Comparacion de mecanismos - E/S secuencial vs aleatoria
  - 4.3: Efecto del buffer cache (lectura fria vs caliente)
  - 4.4: Syscalls (open, read, write, lseek, close),
         E/S bloqueante vs no bloqueante, redireccion con dup2
"""

import os
import time
import fcntl
import errno
import tempfile


def separador(titulo):
    """Imprime un separador visual con titulo."""
    ancho = 70
    print("\n" + "=" * ancho)
    print(f"  {titulo}")
    print("=" * ancho)


# =========================================================================
# SECCION 1: Operaciones basicas sobre dispositivos (tema 4.1 y 4.4)
# =========================================================================
# Usamos os.open/os.read/os.write/os.close que son wrappers directos
# de las syscalls del kernel (open, read, write, close).
# Esto es diferente a open() de Python que agrega buffering en userspace.
# =========================================================================

def operaciones_dispositivos():
    """Demuestra open, read, write, close sobre dispositivos reales."""
    separador("1. OPERACIONES BASICAS SOBRE DISPOSITIVOS (tema 4.1 / 4.4)")
    print("Usamos os.open/read/write/close = syscalls directas del kernel.\n")

    # --- /dev/zero: dispositivo de caracter que genera bytes nulos ---
    print("--- Leer de /dev/zero (genera ceros infinitos) ---")
    fd = os.open("/dev/zero", os.O_RDONLY)
    print(f"  os.open('/dev/zero', O_RDONLY) -> fd = {fd}")

    datos = os.read(fd, 16)
    print(f"  os.read(fd, 16) -> {len(datos)} bytes: {datos.hex()}")
    print(f"  Todos son 00 porque /dev/zero siempre retorna ceros.")

    os.close(fd)
    print(f"  os.close({fd}) -> recurso liberado")

    # --- /dev/urandom: dispositivo de caracter con bytes aleatorios ---
    print("\n--- Leer de /dev/urandom (genera bytes aleatorios) ---")
    fd = os.open("/dev/urandom", os.O_RDONLY)
    print(f"  os.open('/dev/urandom', O_RDONLY) -> fd = {fd}")

    datos = os.read(fd, 16)
    print(f"  os.read(fd, 16) -> {len(datos)} bytes: {datos.hex()}")
    print(f"  Bytes aleatorios generados por el CSPRNG del kernel.")

    os.close(fd)

    # --- /dev/null: dispositivo que descarta todo ---
    print("\n--- Escribir a /dev/null (descarta todo) ---")
    fd = os.open("/dev/null", os.O_WRONLY)
    print(f"  os.open('/dev/null', O_WRONLY) -> fd = {fd}")

    mensaje = b"Estos datos seran descartados por el kernel"
    escritos = os.write(fd, mensaje)
    print(f"  os.write(fd, '{mensaje.decode()}') -> {escritos} bytes")
    print(f"  El driver de /dev/null acepta los bytes pero no los almacena.")

    os.close(fd)

    # --- Archivo regular: open, write, lseek, read, close ---
    print("\n--- Ciclo completo en archivo regular ---")
    ruta = tempfile.mktemp(prefix="practica2_", suffix=".txt")

    # Crear y escribir
    fd = os.open(ruta, os.O_CREAT | os.O_RDWR | os.O_TRUNC, 0o644)
    print(f"  os.open('{ruta}', O_CREAT|O_RDWR) -> fd = {fd}")

    texto = b"Hola desde las syscalls de E/S!\n"
    escritos = os.write(fd, texto)
    print(f"  os.write(fd, ...) -> {escritos} bytes escritos")

    # lseek al inicio
    pos = os.lseek(fd, 0, os.SEEK_SET)
    print(f"  os.lseek(fd, 0, SEEK_SET) -> posicion = {pos}")

    # Leer lo escrito
    leido = os.read(fd, 256)
    print(f"  os.read(fd, 256) -> {len(leido)} bytes: '{leido.decode().strip()}'")

    # Obtener metadatos con fstat
    info = os.fstat(fd)
    print(f"  os.fstat(fd) -> tamano={info.st_size}, inode={info.st_ino}, "
          f"device=({os.major(info.st_dev)},{os.minor(info.st_dev)})")

    os.close(fd)
    os.unlink(ruta)
    print(f"  os.close({fd}) + os.unlink() -> archivo cerrado y eliminado")


# =========================================================================
# SECCION 2: Benchmark de rendimiento de E/S (tema 4.2 y 4.3)
# =========================================================================
# Comparamos el rendimiento de:
# - Escritura secuencial vs lectura secuencial
# - Lectura secuencial vs lectura aleatoria (efecto del I/O scheduler)
# - Diferentes tamanos de bloque (efecto del DMA y buffering)
# =========================================================================

def benchmark_rendimiento():
    """Mide el rendimiento de distintos patrones de E/S."""
    separador("2. BENCHMARK DE RENDIMIENTO DE E/S (tema 4.2 / 4.3)")
    print("Comparamos patrones de acceso para ver el efecto del")
    print("buffer cache, DMA y el I/O scheduler.\n")

    tamano_archivo = 50 * 1024 * 1024  # 50 MB
    ruta = tempfile.mktemp(prefix="bench_io_", suffix=".bin")

    # --- Benchmark de escritura secuencial ---
    print("--- Escritura secuencial (50 MB) ---")
    tamanos_bloque = [4096, 65536, 1048576]  # 4KB, 64KB, 1MB

    for bs in tamanos_bloque:
        fd = os.open(ruta, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
        bloque = b'\x00' * bs
        iteraciones = tamano_archivo // bs

        inicio = time.perf_counter()
        for _ in range(iteraciones):
            os.write(fd, bloque)
        os.fsync(fd)  # Forzar escritura a disco (no solo buffer cache)
        duracion = time.perf_counter() - inicio

        os.close(fd)
        velocidad = (tamano_archivo / (1024 * 1024)) / duracion
        print(f"  Bloque {bs//1024:>5} KB: {duracion:.3f}s -> {velocidad:>8.1f} MB/s")

    # --- Benchmark de lectura secuencial ---
    print("\n--- Lectura secuencial (50 MB) ---")

    # Primero limpiar el cache (drop_caches requiere root, asi que
    # usamos O_DIRECT si es posible, o medimos con cache caliente)
    for bs in tamanos_bloque:
        fd = os.open(ruta, os.O_RDONLY)
        iteraciones = tamano_archivo // bs

        inicio = time.perf_counter()
        for _ in range(iteraciones):
            datos = os.read(fd, bs)
            if not datos:
                break
        duracion = time.perf_counter() - inicio

        os.close(fd)
        velocidad = (tamano_archivo / (1024 * 1024)) / duracion
        print(f"  Bloque {bs//1024:>5} KB: {duracion:.3f}s -> {velocidad:>8.1f} MB/s")

    # --- Comparacion: lectura secuencial vs aleatoria ---
    print("\n--- Secuencial vs Aleatoria (lectura de 10,000 bloques de 4KB) ---")
    num_lecturas = 10000
    bs = 4096
    max_offset = tamano_archivo - bs

    import random
    # Generar offsets aleatorios alineados a 4KB
    offsets_aleatorios = [random.randint(0, max_offset // bs) * bs
                         for _ in range(num_lecturas)]

    # Secuencial
    fd = os.open(ruta, os.O_RDONLY)
    inicio = time.perf_counter()
    for i in range(num_lecturas):
        os.read(fd, bs)
    dur_seq = time.perf_counter() - inicio
    os.close(fd)

    # Aleatoria (con lseek)
    fd = os.open(ruta, os.O_RDONLY)
    inicio = time.perf_counter()
    for offset in offsets_aleatorios:
        os.lseek(fd, offset, os.SEEK_SET)
        os.read(fd, bs)
    dur_rand = time.perf_counter() - inicio
    os.close(fd)

    vel_seq = (num_lecturas * bs / (1024 * 1024)) / dur_seq
    vel_rand = (num_lecturas * bs / (1024 * 1024)) / dur_rand

    print(f"  Secuencial: {dur_seq:.3f}s -> {vel_seq:.1f} MB/s")
    print(f"  Aleatoria:  {dur_rand:.3f}s -> {vel_rand:.1f} MB/s")
    if dur_rand > 0:
        factor = dur_rand / dur_seq
        print(f"  La lectura aleatoria es {factor:.1f}x mas lenta")
        print("  (En HDD seria 100x+ mas lenta por el movimiento del cabezal)")

    os.unlink(ruta)


# =========================================================================
# SECCION 3: Efecto del Buffer Cache (tema 4.3)
# =========================================================================
# Demostramos que la primera lectura de un archivo es mas lenta (va a
# disco) y las siguientes son mas rapidas (servidas desde RAM/cache).
# =========================================================================

def efecto_buffer_cache():
    """Demuestra la diferencia entre lectura fria y caliente."""
    separador("3. EFECTO DEL BUFFER CACHE (tema 4.3)")
    print("La primera lectura va a disco fisico (fria).")
    print("Las siguientes se sirven desde el page cache en RAM (caliente).\n")

    tamano = 20 * 1024 * 1024  # 20 MB
    ruta = tempfile.mktemp(prefix="cache_test_", suffix=".bin")

    # Crear archivo de prueba
    fd = os.open(ruta, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
    bloque = os.urandom(1024 * 1024)  # 1MB de datos aleatorios
    for _ in range(tamano // (1024 * 1024)):
        os.write(fd, bloque)
    os.fsync(fd)
    os.close(fd)

    # Leer multiples veces y medir
    tiempos = []
    for intento in range(5):
        fd = os.open(ruta, os.O_RDONLY)
        inicio = time.perf_counter()
        while True:
            datos = os.read(fd, 65536)
            if not datos:
                break
        duracion = time.perf_counter() - inicio
        os.close(fd)
        tiempos.append(duracion)
        velocidad = (tamano / (1024 * 1024)) / duracion
        etiqueta = "(puede ser fria)" if intento == 0 else "(caliente - cache)"
        print(f"  Lectura {intento+1}: {duracion:.4f}s -> {velocidad:>8.1f} MB/s {etiqueta}")

    if tiempos[0] > 0 and tiempos[-1] > 0:
        mejora = tiempos[0] / tiempos[-1]
        print(f"\n  La lectura en cache es hasta {mejora:.1f}x mas rapida.")
        print("  Esto es porque el kernel guarda los bloques leidos en RAM")
        print("  (page cache) y las lecturas siguientes no necesitan ir a disco.")

    os.unlink(ruta)


# =========================================================================
# SECCION 4: E/S Bloqueante vs No Bloqueante (tema 4.4)
# =========================================================================
# Demostramos la diferencia usando un pipe:
# - Sin O_NONBLOCK: read() bloquea al proceso hasta que hay datos
# - Con O_NONBLOCK: read() retorna inmediatamente con errno=EAGAIN
# =========================================================================

def io_bloqueante_vs_no_bloqueante():
    """Demuestra E/S bloqueante vs no bloqueante con un pipe."""
    separador("4. E/S BLOQUEANTE VS NO BLOQUEANTE (tema 4.4)")
    print("Usamos un pipe (os.pipe) para demostrar la diferencia.\n")

    # Crear un pipe: r_fd para leer, w_fd para escribir
    r_fd, w_fd = os.pipe()
    print(f"  os.pipe() -> lectura=fd {r_fd}, escritura=fd {w_fd}")

    # --- Modo NO BLOQUEANTE ---
    print("\n--- Modo NO BLOQUEANTE (O_NONBLOCK) ---")
    # Activar O_NONBLOCK en el fd de lectura
    flags = fcntl.fcntl(r_fd, fcntl.F_GETFL)
    fcntl.fcntl(r_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    print("  Activado O_NONBLOCK en el fd de lectura.")

    # Intentar leer del pipe vacio
    print("  Intentando leer del pipe vacio...")
    try:
        datos = os.read(r_fd, 1024)
        print(f"  Resultado: se leyeron {len(datos)} bytes")
    except BlockingIOError as e:
        print(f"  Resultado: BlockingIOError (errno={e.errno} EAGAIN)")
        print("  El proceso NO se bloqueo, recibio un error inmediato.")
        print("  Puede hacer otra cosa y reintentar despues.")

    # --- Ahora escribir datos y leer ---
    print("\n--- Escribir al pipe y luego leer ---")
    mensaje = b"Datos disponibles en el pipe"
    os.write(w_fd, mensaje)
    print(f"  os.write(w_fd, '{mensaje.decode()}') -> {len(mensaje)} bytes")

    try:
        datos = os.read(r_fd, 1024)
        print(f"  os.read(r_fd, 1024) -> {len(datos)} bytes: '{datos.decode()}'")
        print("  Esta vez si habia datos, la lectura fue exitosa.")
    except BlockingIOError:
        print("  Error inesperado")

    # --- Modo BLOQUEANTE (explicacion teorica, no bloquear el programa) ---
    print("\n--- Modo BLOQUEANTE (comportamiento por defecto) ---")
    print("  Sin O_NONBLOCK, read() en un pipe vacio SUSPENDERIA")
    print("  al proceso hasta que otro proceso escriba datos.")
    print("  El kernel pone al proceso en estado SLEEPING.")
    print("  Esto es eficiente (no gasta CPU) pero bloquea el hilo.")

    os.close(r_fd)
    os.close(w_fd)


# =========================================================================
# SECCION 5: Redireccion de E/S con dup2 (tema 4.4)
# =========================================================================
# dup2() es la syscall que el shell usa internamente para implementar
# redirecciones como "comando > archivo" o "cmd1 | cmd2".
# dup2(fd_origen, fd_destino) hace que fd_destino apunte al mismo
# archivo/dispositivo que fd_origen.
# =========================================================================

def redireccion_con_dup2():
    """Demuestra redireccion de E/S usando dup2 (como hace el shell)."""
    separador("5. REDIRECCION DE E/S CON dup2 (tema 4.4)")
    print("dup2() es la syscall que el shell usa para '>' y '|'.\n")

    ruta = tempfile.mktemp(prefix="redir_", suffix=".txt")

    # Guardar stdout original
    stdout_backup = os.dup(1)

    # Abrir archivo destino
    fd_archivo = os.open(ruta, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)

    # Redirigir stdout (fd 1) al archivo
    os.dup2(fd_archivo, 1)
    os.close(fd_archivo)

    # Todo lo que se escriba a stdout ahora va al archivo
    # Usamos os.write directamente a fd 1
    os.write(1, b"Linea 1: Esta salida fue redirigida con dup2()\n")
    os.write(1, b"Linea 2: Equivalente a 'programa > archivo' en el shell\n")
    os.write(1, b"Linea 3: El proceso no sabe que stdout cambio\n")

    # Restaurar stdout original
    os.dup2(stdout_backup, 1)
    os.close(stdout_backup)

    # Ahora stdout vuelve a la terminal
    print("  stdout fue redirigido a un archivo y luego restaurado.")
    print(f"  Contenido del archivo '{ruta}':\n")

    # Leer y mostrar el archivo
    fd = os.open(ruta, os.O_RDONLY)
    contenido = os.read(fd, 4096)
    os.close(fd)

    for linea in contenido.decode().strip().split("\n"):
        print(f"    {linea}")

    print("\n  Asi es como el shell implementa '>' internamente:")
    print("    1. fork() para crear proceso hijo")
    print("    2. En el hijo: open() el archivo destino")
    print("    3. dup2(fd_archivo, 1) para redirigir stdout")
    print("    4. exec() para ejecutar el comando")

    os.unlink(ruta)


# =========================================================================
# SECCION 6: Estadisticas de E/S del proceso (tema 4.4)
# =========================================================================
# /proc/self/io contiene las estadisticas de E/S del proceso actual.
# Leemos antes y despues de generar E/S para ver la diferencia.
# =========================================================================

def estadisticas_io_proceso():
    """Muestra las estadisticas de E/S antes y despues de generar carga."""
    separador("6. ESTADISTICAS DE E/S DEL PROCESO (tema 4.4)")
    print("Linux cuenta cada byte y cada syscall de E/S por proceso.\n")

    def leer_io_stats():
        """Lee /proc/self/io y retorna un diccionario."""
        stats = {}
        try:
            with open("/proc/self/io", "r") as f:
                for linea in f:
                    clave, valor = linea.strip().split(": ")
                    stats[clave] = int(valor)
        except PermissionError:
            pass
        return stats

    # Estadisticas ANTES
    antes = leer_io_stats()
    if not antes:
        print("  No se pudo leer /proc/self/io (requiere permisos)")
        return

    print("  Estadisticas ANTES de generar E/S:")
    for clave, valor in antes.items():
        print(f"    {clave:<30} = {valor:>15,}")

    # Generar E/S: escribir y leer 5 MB
    print("\n  Generando E/S: escribir y leer 5 MB...")
    ruta = tempfile.mktemp(prefix="stats_", suffix=".bin")
    fd = os.open(ruta, os.O_CREAT | os.O_RDWR | os.O_TRUNC, 0o644)
    datos = b'\xAB' * (5 * 1024 * 1024)
    os.write(fd, datos)
    os.fsync(fd)
    os.lseek(fd, 0, os.SEEK_SET)
    _ = os.read(fd, 5 * 1024 * 1024)
    os.close(fd)
    os.unlink(ruta)

    # Estadisticas DESPUES
    despues = leer_io_stats()

    print("\n  Estadisticas DESPUES de generar E/S:")
    print(f"  {'Campo':<30} {'Antes':>15} {'Despues':>15} {'Diferencia':>15}")
    print("  " + "-" * 78)

    campos_desc = {
        "rchar":                   "Bytes leidos (con cache)",
        "wchar":                   "Bytes escritos (con cache)",
        "syscr":                   "Syscalls read()",
        "syscw":                   "Syscalls write()",
        "read_bytes":              "Bytes leidos de disco real",
        "write_bytes":             "Bytes escritos a disco real",
        "cancelled_write_bytes":   "Escrituras canceladas",
    }

    for clave in antes:
        diff = despues.get(clave, 0) - antes[clave]
        desc = campos_desc.get(clave, "")
        valor_antes = antes[clave]
        valor_despues = despues.get(clave, 0)
        signo = "+" if diff > 0 else ""
        print(f"  {clave:<30} {valor_antes:>15,} {valor_despues:>15,} {signo}{diff:>14,}")

    print(f"\n  Nota: 'rchar' y 'wchar' incluyen datos servidos desde cache.")
    print(f"  'read_bytes' y 'write_bytes' son E/S real a disco.")
    print(f"  La diferencia muestra cuanto ahorró el buffer cache.")


# =========================================================================
# MAIN - Ejecutar todas las secciones
# =========================================================================

def main():
    print("+" + "=" * 68 + "+")
    print("|  PRACTICA 2: Operaciones de E/S y Benchmark de Rendimiento       |")
    print("|  Sistemas Operativos - Unidad 4                                  |")
    print("+" + "=" * 68 + "+")

    operaciones_dispositivos()          # 4.1, 4.4
    benchmark_rendimiento()             # 4.2, 4.3
    efecto_buffer_cache()               # 4.3
    io_bloqueante_vs_no_bloqueante()    # 4.4
    redireccion_con_dup2()              # 4.4
    estadisticas_io_proceso()           # 4.4

    separador("FIN DE LA PRACTICA")
    print("Se demostraron todas las operaciones de E/S de la Unidad 4:")
    print("  - Syscalls: open, read, write, lseek, close, dup2, fstat, fsync")
    print("  - Dispositivos: /dev/null, /dev/zero, /dev/urandom, pipes, archivos")
    print("  - Rendimiento: secuencial vs aleatorio, tamanos de bloque")
    print("  - Buffer cache: lectura fria vs caliente")
    print("  - Modos: bloqueante vs no bloqueante (O_NONBLOCK + EAGAIN)")
    print("  - Redireccion: dup2() como lo usa el shell internamente\n")


if __name__ == "__main__":
    main()
```

#### Ejecucion

```bash
python3 practica2_operaciones_io.py
```

#### Salida esperada

```
+====================================================================+
|  PRACTICA 2: Operaciones de E/S y Benchmark de Rendimiento         |
|  Sistemas Operativos - Unidad 4                                    |
+====================================================================+

======================================================================
  1. OPERACIONES BASICAS SOBRE DISPOSITIVOS (tema 4.1 / 4.4)
======================================================================
Usamos os.open/read/write/close = syscalls directas del kernel.

--- Leer de /dev/zero (genera ceros infinitos) ---
  os.open('/dev/zero', O_RDONLY) -> fd = 3
  os.read(fd, 16) -> 16 bytes: 00000000000000000000000000000000
  Todos son 00 porque /dev/zero siempre retorna ceros.
  os.close(3) -> recurso liberado

--- Leer de /dev/urandom (genera bytes aleatorios) ---
  os.open('/dev/urandom', O_RDONLY) -> fd = 3
  os.read(fd, 16) -> 16 bytes: a3f7c91d2e4b8a0f6c5d3e2a1b9f7c8d
  Bytes aleatorios generados por el CSPRNG del kernel.

--- Escribir a /dev/null (descarta todo) ---
  os.open('/dev/null', O_WRONLY) -> fd = 3
  os.write(fd, 'Estos datos seran descartados...') -> 44 bytes
  El driver de /dev/null acepta los bytes pero no los almacena.

--- Ciclo completo en archivo regular ---
  os.open('/tmp/practica2_xyz.txt', O_CREAT|O_RDWR) -> fd = 3
  os.write(fd, ...) -> 31 bytes escritos
  os.lseek(fd, 0, SEEK_SET) -> posicion = 0
  os.read(fd, 256) -> 31 bytes: 'Hola desde las syscalls de E/S!'
  os.fstat(fd) -> tamano=31, inode=6816400, device=(259,2)
  os.close(3) + os.unlink() -> archivo cerrado y eliminado

======================================================================
  2. BENCHMARK DE RENDIMIENTO DE E/S (tema 4.2 / 4.3)
======================================================================
--- Escritura secuencial (50 MB) ---
  Bloque     4 KB: 0.182s ->    274.7 MB/s
  Bloque    64 KB: 0.045s ->   1111.1 MB/s
  Bloque  1024 KB: 0.038s ->   1315.8 MB/s

--- Lectura secuencial (50 MB) ---
  Bloque     4 KB: 0.028s ->   1785.7 MB/s
  Bloque    64 KB: 0.005s ->  10000.0 MB/s
  Bloque  1024 KB: 0.004s ->  12500.0 MB/s

--- Secuencial vs Aleatoria ---
  Secuencial: 0.031s -> 1254.2 MB/s
  Aleatoria:  0.042s ->  926.1 MB/s
  La lectura aleatoria es 1.4x mas lenta

======================================================================
  3. EFECTO DEL BUFFER CACHE (tema 4.3)
======================================================================
  Lectura 1: 0.0089s ->  2247.2 MB/s (puede ser fria)
  Lectura 2: 0.0031s ->  6451.6 MB/s (caliente - cache)
  Lectura 3: 0.0030s ->  6666.7 MB/s (caliente - cache)
  Lectura 4: 0.0030s ->  6666.7 MB/s (caliente - cache)
  Lectura 5: 0.0030s ->  6666.7 MB/s (caliente - cache)

  La lectura en cache es hasta 3.0x mas rapida.

======================================================================
  4. E/S BLOQUEANTE VS NO BLOQUEANTE (tema 4.4)
======================================================================
  os.pipe() -> lectura=fd 3, escritura=fd 4

--- Modo NO BLOQUEANTE (O_NONBLOCK) ---
  Activado O_NONBLOCK en el fd de lectura.
  Intentando leer del pipe vacio...
  Resultado: BlockingIOError (errno=11 EAGAIN)
  El proceso NO se bloqueo, recibio un error inmediato.

--- Escribir al pipe y luego leer ---
  os.write(w_fd, 'Datos disponibles en el pipe') -> 28 bytes
  os.read(r_fd, 1024) -> 28 bytes: 'Datos disponibles en el pipe'
  Esta vez si habia datos, la lectura fue exitosa.

======================================================================
  5. REDIRECCION DE E/S CON dup2 (tema 4.4)
======================================================================
  stdout fue redirigido a un archivo y luego restaurado.

    Linea 1: Esta salida fue redirigida con dup2()
    Linea 2: Equivalente a 'programa > archivo' en el shell
    Linea 3: El proceso no sabe que stdout cambio

======================================================================
  6. ESTADISTICAS DE E/S DEL PROCESO (tema 4.4)
======================================================================
  Campo                          Antes         Despues      Diferencia
  ----------------------------------------------------------------
  rchar                        240,128      10,725,376     +10,485,248
  wchar                        102,400       5,345,280      +5,242,880
  syscr                             48             130             +82
  syscw                             25              27              +2
  read_bytes                         0       5,242,880      +5,242,880
  write_bytes                  102,400       5,345,280      +5,242,880
```
