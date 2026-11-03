# Trabajo final — Sistemas Operativos: material base por equipo

Carpetas organizadas con el material ya elaborado en prácticas anteriores, listo para que cada equipo lo use como punto de partida al grabar su video de demostración.

Importante: este material es **base teórica y código de referencia**, no el video terminado. Lo que aparece en el video debe volver a ejecutarse en cámara — correr el código o los comandos de verdad frente a la grabación, no leer el markdown en voz alta.

## Mapeo por equipo

| Equipo | Tema | Carpeta | Qué tiene ya | Qué falta para el video |
|---|---|---|---|---|
| 1 | Estructura y núcleo del sistema operativo | *(sin material base — parte de cero)* | — | `uname -a`, `lsmod`, `/proc/version`, diagrama de capas/niveles de diseño |
| 2 | Procesos: estados, transiciones y planificación | [`equipo2_procesos/`](equipo2_procesos/) | `process_manager.py` + `main.py`: administrador de procesos real en Python que monitorea procesos del sistema y muestra los que más CPU usan | Correr el script en cámara, y agregar la parte de **forzar una transición de estado** (`kill -STOP`/`kill -CONT`) que el script actual no cubre — revisarlo con `ps -eo pid,stat,cmd` antes/después |
| 3 | Hilos, concurrencia y sincronización | [`equipo3_hilos_concurrencia/`](equipo3_hilos_concurrencia/) | `README_hilos.md`: tutorial completo con ejemplo en Python de condición de carrera SIN sincronización y la versión CON sincronización (mutex), ya resuelto. `README_concurrencia.md`: concurrencia vs. paralelismo con ejemplos de `threading` | Ya está prácticamente listo — solo falta correr ambas versiones (SIN/CON sincronización) en cámara y mostrar el resultado incorrecto vs. el corregido |
| 4 | Memoria real y memoria virtual | [`equipo4_memoria/`](equipo4_memoria/) | `README_administracion_memoria.md`: tutorial extenso ya alineado al tema. `README_politicas_memoria.md`: resumen de políticas de administración de memoria | Verificar qué tan ejecutable es el contenido (revisar si trae scripts Python o solo teoría) y preparar la demo de `free -h` / `vmstat` / `/proc/meminfo` + presión de memoria en vivo |
| 5 | Entrada/salida y manejadores de dispositivos | [`equipo5_entrada_salida/`](equipo5_entrada_salida/) | `README.md`: tutorial extenso con entorno de pruebas documentado (Ubuntu, SSD NVMe) | Revisar si ya incluye `lsblk` / `lsusb` / `lspci -k` / `dmesg` o si hay que agregarlos; planear el momento de conectar un USB en vivo para capturar `dmesg` |
| 6 | Sistemas de archivos | [`equipo6_sistemas_archivos/`](equipo6_sistemas_archivos/) | `README_archivos.md`: comandos básicos de gestión de archivos. `README_permisos.md`: usuarios, grupos y permisos en Ubuntu | Falta crear un sistema de archivos real con `dd` + `mkfs.ext4` sobre loopback, montarlo, e inspeccionar inodos con `stat`/`debugfs` — no está en este material, hay que agregarlo |
| 7 | Protección y seguridad | [`equipo7_seguridad/`](equipo7_seguridad/) | El más completo: 8 archivos numerados que cubren introducción, conceptos, clasificación, funciones del sistema de protección, matrices de acceso, protección basada en lenguaje, validación de amenazas y cifrado | Elegir qué subset cabe en 6-10 minutos (no hay tiempo para los 8 archivos), priorizando matrices de acceso + cifrado por ser los más demostrables en pantalla |

## Material disponible pero no asignado a ningún equipo

Dentro de `curso-python/` hay más material de apoyo general que no corresponde a un tema específico:

- `mandatos_basicos/`, `programacion-shell/`: comandos básicos de terminal y shell scripting — prerequisito útil para cualquier equipo.
- `python-sockets/`, `sockets-vpn/`, `samba/`, `cron/`: redes/interoperabilidad/automatización — disponibles como profundización opcional, no obligatoria.

## Siguiente paso sugerido

1. Cada equipo revisa su carpeta aquí como punto de partida.
2. Antes del checkpoint intermedio, cada equipo debe haber corrido al menos una vez, en su propia máquina, el código/los comandos de su carpeta.
