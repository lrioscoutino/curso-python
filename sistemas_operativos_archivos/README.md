# Tarea Práctica: Administración de Sistemas de Archivos en Linux

## Objetivos
- Familiarizarse con los comandos básicos de gestión de archivos en Linux
- Comprender los permisos de archivos y directorios
- Aprender a montar y gestionar diferentes sistemas de archivos
- Realizar operaciones de respaldo y recuperación

## Requisitos
- Acceso a un sistema Linux (puede ser una máquina virtual o una distribución instalada)
- Privilegios de administrador (sudo)

## Parte 1: Comandos Básicos de Archivos

1. Crea una estructura de directorios para un proyecto ficticio:
   ```bash
   mkdir -p ~/proyecto/{docs,src,config,backup}
   ```

2. Crea varios archivos con diferentes contenidos:
   ```bash
   echo "Este es un archivo de configuración" > ~/proyecto/config/config.txt
   echo "// Código fuente de ejemplo" > ~/proyecto/src/main.c
   echo "Documentación del proyecto" > ~/proyecto/docs/manual.txt
   ```

3. Realiza las siguientes operaciones y anota el resultado:
   - Lista todos los archivos con detalles: `ls -la ~/proyecto`
   - Muestra el contenido de un archivo: `cat ~/proyecto/config/config.txt`
   - Busca un texto en los archivos: `grep "ejemplo" ~/proyecto/src/main.c`
   - Copia un archivo: `cp ~/proyecto/docs/manual.txt ~/proyecto/backup/`
   - Crea un enlace simbólico: `ln -s ~/proyecto/config/config.txt ~/config_link`

## Parte 2: Permisos de Archivos

1. Cambia los permisos de los archivos:
   ```bash
   chmod 644 ~/proyecto/config/config.txt
   chmod 755 ~/proyecto/src/main.c
   chmod 400 ~/proyecto/docs/manual.txt
   ```

2. Responde a las siguientes preguntas:
   - ¿Qué significan los permisos 644, 755 y 400?
   - ¿Puedes modificar el archivo manual.txt? ¿Por qué?
   - ¿Qué comando usarías para hacer ejecutable un script?

3. Cambia el propietario de un archivo (requiere sudo):
   ```bash
   sudo chown root:root ~/proyecto/config/config.txt
   ```
   - ¿Puedes modificar ahora el archivo config.txt? ¿Cómo podrías recuperar el acceso?

## Parte 3: Sistemas de Archivos y Particiones

1. Identifica las particiones y sistemas de archivos en tu sistema:
   ```bash
   df -Th
   sudo fdisk -l
   ```
   - Anota qué sistemas de archivos están en uso (ext4, xfs, btrfs, etc.)
   - ¿Cuánto espacio libre tienes en cada partición?

2. Si tienes una unidad USB disponible (reemplaza /dev/sdX con tu dispositivo):
   ```bash
   # PRECAUCIÓN: Asegúrate de identificar correctamente tu dispositivo
   sudo fdisk /dev/sdX   # Crea una nueva partición
   sudo mkfs.ext4 /dev/sdX1   # Formatea con sistema de archivos ext4
   sudo mkdir /mnt/usb
   sudo mount /dev/sdX1 /mnt/usb
   ```

3. Explora la información del sistema de archivos:
   ```bash
   sudo tune2fs -l /dev/sdX1   # Para sistemas ext2/3/4
   ```
   - ¿Cuántos inodos tiene tu sistema de archivos?
   - ¿Cuál es el tamaño de bloque?

## Parte 4: Respaldo y Recuperación

1. Crea un archivo tar de tu proyecto:
   ```bash
   tar -czvf ~/proyecto_backup.tar.gz ~/proyecto
   ```

2. Simula la pérdida de datos:
   ```bash
   rm -rf ~/proyecto/docs/*
   ```

3. Recupera desde el respaldo:
   ```bash
   mkdir -p ~/proyecto_recuperado
   tar -xzvf ~/proyecto_backup.tar.gz -C ~/proyecto_recuperado
   ```
   - Compara los directorios: `diff -r ~/proyecto ~/proyecto_recuperado`

## Parte 5: Uso Avanzado

1. Configura cuotas de disco (si tu sistema lo soporta):
   ```bash
   sudo apt-get install quota   # En sistemas basados en Debian
   # o
   sudo yum install quota   # En sistemas basados en Red Hat
   ```
   - Investiga cómo habilitar y configurar cuotas para un usuario

2. Verifica la integridad del sistema de archivos:
   ```bash
   sudo umount /dev/sdX1   # Desmonta primero
   sudo fsck /dev/sdX1
   ```
   - ¿Qué hace fsck? ¿Cuándo deberías usarlo?


## Evaluación

1. Documenta cada paso realizado con capturas de pantalla o salidas de comandos.
2. Explica cualquier error encontrado y cómo lo solucionaste.
3. Responde a todas las preguntas planteadas en cada sección.
