# Manual de Comandos Básicos de Terminal Ubuntu

## Introducción

El terminal de Ubuntu es una herramienta poderosa que te permite interactuar directamente con el sistema operativo mediante comandos de texto. Este manual te enseñará los comandos fundamentales para navegar y administrar tu sistema.

## ¿Cómo abrir el terminal?

- **Atajo de teclado**: `Ctrl + Alt + T`
- **Desde el menú**: Buscar "Terminal" en las aplicaciones
- **Clic derecho**: En cualquier carpeta → "Abrir en terminal"

---

## 1. Navegación y Exploración del Sistema

### `pwd` - Mostrar directorio actual
```bash
pwd
```
**¿Qué hace?**: Muestra la ruta completa del directorio donde te encuentras actualmente.

### `ls` - Listar contenido
```bash
ls                    # Lista archivos y carpetas
ls -l                 # Lista detallada (permisos, tamaño, fecha)
ls -la                # Incluye archivos ocultos
ls -lh                # Tamaños en formato legible (KB, MB, GB)
ls /ruta/específica   # Lista contenido de otra carpeta
```

### `cd` - Cambiar directorio
```bash
cd /home/usuario      # Ir a directorio específico
cd ..                 # Subir un nivel
cd ~                  # Ir al directorio home del usuario
cd -                  # Volver al directorio anterior
cd                    # Sin argumentos, va al home
```

### `tree` - Vista en árbol
```bash
tree                  # Muestra estructura de carpetas en árbol
tree -L 2             # Limita a 2 niveles de profundidad
```

---

## 2. Gestión de Archivos y Carpetas

### `mkdir` - Crear carpetas
```bash
mkdir nueva_carpeta           # Crear una carpeta
mkdir -p ruta/completa/nueva  # Crear carpetas padre si no existen
mkdir carpeta1 carpeta2       # Crear múltiples carpetas
```

### `touch` - Crear archivos vacíos
```bash
touch archivo.txt             # Crear archivo vacío
touch archivo1.txt archivo2.txt  # Crear múltiples archivos
```

### `cp` - Copiar archivos/carpetas
```bash
cp archivo.txt copia.txt      # Copiar archivo
cp archivo.txt /otra/ruta/    # Copiar a otro directorio
cp -r carpeta/ nueva_carpeta/ # Copiar carpeta completa (-r = recursivo)
cp *.txt /destino/            # Copiar todos los archivos .txt
```

### `mv` - Mover/renombrar
```bash
mv archivo.txt nuevo_nombre.txt   # Renombrar archivo
mv archivo.txt /otra/carpeta/     # Mover archivo
mv carpeta/ /nuevo/lugar/         # Mover carpeta
```

### `rm` - Eliminar archivos/carpetas
```bash
rm archivo.txt        # Eliminar archivo
rm -r carpeta/        # Eliminar carpeta y contenido
rm -rf carpeta/       # Forzar eliminación sin confirmación
rm *.tmp              # Eliminar archivos con patrón
```

**⚠️ CUIDADO**: `rm` elimina permanentemente. No hay papelera de reciclaje.

---

## 3. Visualización y Edición de Archivos

### `cat` - Mostrar contenido completo
```bash
cat archivo.txt       # Mostrar todo el contenido
cat archivo1.txt archivo2.txt  # Mostrar múltiples archivos
```

### `less` y `more` - Visualización paginada
```bash
less archivo.txt      # Navegar con flechas, 'q' para salir
more archivo.txt      # Similar a less, menos funciones
```

### `head` y `tail` - Primeras/últimas líneas
```bash
head archivo.txt      # Primeras 10 líneas
head -n 5 archivo.txt # Primeras 5 líneas
tail archivo.txt      # Últimas 10 líneas
tail -f log.txt       # Seguir archivo en tiempo real
```

### `nano` - Editor de texto simple
```bash
nano archivo.txt      # Abrir/crear archivo en nano
```
**Controles en nano**:
- `Ctrl + O`: Guardar
- `Ctrl + X`: Salir
- `Ctrl + K`: Cortar línea
- `Ctrl + U`: Pegar

---

## 4. Búsqueda y Filtros

### `find` - Buscar archivos/carpetas
```bash
find . -name "archivo.txt"        # Buscar por nombre exacto
find . -name "*.txt"              # Buscar archivos .txt
find /home -type d -name "Music"  # Buscar carpetas llamadas "Music"
find . -size +100M                # Archivos mayores a 100MB
```

### `grep` - Buscar texto dentro de archivos
```bash
grep "texto" archivo.txt          # Buscar texto en archivo
grep -r "palabra" .               # Buscar recursivamente en carpeta
grep -i "TEXTO" archivo.txt       # Búsqueda insensible a mayúsculas
grep -n "error" log.txt           # Mostrar números de línea
```

### `locate` - Búsqueda rápida
```bash
locate archivo.txt                # Buscar en base de datos del sistema
sudo updatedb                     # Actualizar base de datos
```

---

## 5. Información del Sistema

### `df` - Espacio en disco
```bash
df -h                 # Espacio en discos (formato legible)
df -h /               # Espacio específico del disco raíz
```

### `du` - Uso de espacio por carpetas
```bash
du -h carpeta/        # Tamaño de carpeta
du -sh carpeta/       # Solo total de la carpeta
du -h --max-depth=1   # Un nivel de profundidad
```

### `free` - Memoria RAM
```bash
free -h               # Uso de memoria RAM
```

### `ps` - Procesos en ejecución
```bash
ps aux                # Todos los procesos
ps aux | grep firefox # Buscar procesos específicos
```

### `top` - Monitor de procesos en tiempo real
```bash
top                   # Vista dinámica de procesos
htop                  # Versión mejorada (si está instalada)
```

---

## 6. Permisos y Usuarios

### `chmod` - Cambiar permisos
```bash
chmod 755 archivo.txt     # Permisos: rwxr-xr-x
chmod +x script.sh        # Hacer ejecutable
chmod -w archivo.txt      # Quitar permisos de escritura
```

**Números de permisos**:
- 7 = rwx (lectura, escritura, ejecución)
- 6 = rw- (lectura, escritura)
- 5 = r-x (lectura, ejecución)
- 4 = r-- (solo lectura)

### `chown` - Cambiar propietario
```bash
sudo chown usuario:grupo archivo.txt   # Cambiar propietario y grupo
sudo chown -R usuario carpeta/         # Recursivo para carpeta
```

### `whoami` - Usuario actual
```bash
whoami                # Muestra tu nombre de usuario
```

---

## 7. Gestión de Paquetes (apt)

### Actualizar sistema
```bash
sudo apt update           # Actualizar lista de paquetes
sudo apt upgrade          # Actualizar paquetes instalados
sudo apt full-upgrade     # Actualización completa
```

### Instalar/desinstalar software
```bash
sudo apt install nombre-paquete    # Instalar paquete
sudo apt remove nombre-paquete     # Desinstalar paquete
sudo apt autoremove                # Limpiar dependencias no usadas
```

### Buscar paquetes
```bash
apt search palabra-clave           # Buscar paquetes
apt show nombre-paquete            # Información del paquete
```

---

## 8. Redirección y Tuberías

### Redirección de salida
```bash
ls > lista.txt            # Guardar salida en archivo
ls >> lista.txt           # Agregar al final del archivo
comando 2> errores.txt    # Guardar errores en archivo
```

### Tuberías (pipes)
```bash
ls -l | grep ".txt"       # Filtrar salida de ls
cat archivo.txt | wc -l   # Contar líneas
ps aux | grep firefox     # Buscar proceso
```

---

## 9. Compresión y Archivos

### `tar` - Comprimir/descomprimir
```bash
tar -czf archivo.tar.gz carpeta/     # Comprimir carpeta
tar -xzf archivo.tar.gz              # Descomprimir
tar -tzf archivo.tar.gz              # Ver contenido sin extraer
```

### `zip` y `unzip`
```bash
zip -r archivo.zip carpeta/          # Comprimir en ZIP
unzip archivo.zip                    # Descomprimir ZIP
unzip -l archivo.zip                 # Ver contenido
```

---

## 10. Comandos de Red

### `wget` y `curl` - Descargar archivos
```bash
wget https://ejemplo.com/archivo.txt # Descargar archivo
curl -O https://ejemplo.com/archivo  # Descargar con curl
```

### `ping` - Probar conectividad
```bash
ping google.com          # Probar conexión
ping -c 4 google.com     # Solo 4 pings
```

---

## Consejos y Trucos

### Autocompletado
- Presiona `Tab` para autocompletar nombres de archivos/comandos
- Presiona `Tab` dos veces para ver opciones disponibles

### Historial de comandos
```bash
history                  # Ver historial de comandos
!número                  # Ejecutar comando del historial
!!                       # Repetir último comando
```

### Atajos de teclado útiles
- `Ctrl + C`: Cancelar comando actual
- `Ctrl + L`: Limpiar pantalla
- `Ctrl + A`: Ir al inicio de línea
- `Ctrl + E`: Ir al final de línea
- `Ctrl + U`: Borrar línea completa
- `Ctrl + R`: Buscar en historial

### Wildcards (comodines)
```bash
*                        # Cualquier secuencia de caracteres
?                        # Un solo carácter
[abc]                    # Uno de los caracteres a, b, o c
[0-9]                    # Cualquier dígito
```

### Comando `man` - Manual
```bash
man comando              # Ver manual del comando
man ls                   # Manual de ls
```

---

## Ejercicios Prácticos

### Ejercicio 1: Navegación básica
1. Abre el terminal
2. Verifica en qué directorio estás con `pwd`
3. Lista el contenido con `ls -la`
4. Ve a tu directorio home con `cd ~`
5. Crea una carpeta llamada "practica" con `mkdir practica`

### Ejercicio 2: Gestión de archivos
1. Entra a la carpeta practica: `cd practica`
2. Crea tres archivos: `touch archivo1.txt archivo2.txt archivo3.txt`
3. Lista los archivos: `ls -l`
4. Copia archivo1.txt como respaldo: `cp archivo1.txt backup.txt`
5. Renombra archivo2.txt: `mv archivo2.txt nuevo_nombre.txt`

### Ejercicio 3: Búsqueda y filtros
1. Busca todos los archivos .txt en tu carpeta: `find . -name "*.txt"`
2. Escribe algo en archivo1.txt: `echo "Hola mundo" > archivo1.txt`
3. Busca la palabra "mundo": `grep "mundo" archivo1.txt`

---

## Comandos de Emergencia

### Sistema no responde
```bash
sudo reboot              # Reiniciar sistema
sudo shutdown -h now     # Apagar sistema
```

### Procesos problemáticos
```bash
killall nombre-programa  # Terminar todos los procesos del programa
sudo kill -9 PID         # Forzar terminación de proceso por ID
```

### Espacio en disco lleno
```bash
sudo apt autoremove      # Limpiar paquetes no necesarios
sudo apt autoclean       # Limpiar caché de paquetes
```

---

## Recursos Adicionales

- Manual en línea: `man comando`
- Ayuda del comando: `comando --help`
- Información del sistema: `uname -a`
- Información de distribución: `lsb_release -a`

¡Practica estos comandos regularmente y pronto te sentirás cómodo usando el terminal de Ubuntu!