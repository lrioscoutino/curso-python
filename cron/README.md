# Manual de Configuración de Cron y Crontab en Ubuntu

## Instalación en Ubuntu

### Verificar si Cron está instalado
```bash
# Verificar si cron está instalado
which cron

# Ver estado del servicio
sudo systemctl status cron
```

### Instalar Cron (si no está instalado)
```bash
# Actualizar repositorios
sudo apt update

# Instalar cron
sudo apt install cron

# Habilitar e iniciar el servicio
sudo systemctl enable cron
sudo systemctl start cron
```

## Definiciones Teóricas

### ¿Qué es Cron?

**Cron** es un demonio del sistema (daemon) en sistemas Unix/Linux que ejecuta tareas programadas automáticamente en momentos específicos. Es un servicio del sistema que se ejecuta continuamente en segundo plano y revisa la tabla de tareas programadas (crontab) cada minuto para determinar si hay trabajos que ejecutar.

### ¿Qué es Crontab?

**Crontab** (Cron Table) es el archivo donde se almacenan las tareas programadas para un usuario específico. Cada usuario del sistema puede tener su propio archivo crontab, y también existe un crontab del sistema para tareas administrativas.

### Sintaxis de Crontab

La sintaxis básica de una entrada en crontab es:

```
* * * * * comando_a_ejecutar
│ │ │ │ │
│ │ │ │ └─── Día de la semana (0-7, donde 0 y 7 = Domingo)
│ │ │ └───── Mes (1-12)
│ │ └─────── Día del mes (1-31)
│ └───────── Hora (0-23)
└─────────── Minuto (0-59)
```

### Caracteres especiales:
- `*` : Cualquier valor
- `,` : Lista de valores (ej: 1,3,5)
- `-` : Rango de valores (ej: 1-5)
- `/` : Intervalos (ej: */5 = cada 5 unidades)

## Comandos Básicos

### Gestión de Crontab
```bash
# Editar crontab del usuario actual
crontab -e

# Listar tareas del usuario actual
crontab -l

# Eliminar todas las tareas del usuario actual
crontab -r

# Editar crontab de otro usuario (requiere privilegios)
sudo crontab -u usuario -e

# Ver logs de cron
sudo tail -f /var/log/syslog | grep CRON
```

### Estado del servicio Cron
```bash
# Verificar estado del servicio
sudo systemctl status cron

# Iniciar el servicio
sudo systemctl start cron

# Detener el servicio
sudo systemctl stop cron

# Reiniciar el servicio
sudo systemctl restart cron
```

## Prácticas

### Práctica 1: Log de Sistema cada 2 Minutos

**Objetivo:** Crear un registro simple que escriba la fecha y hora actual cada 2 minutos.

**Paso 1:** Crear el script
```bash
# Crear directorio para scripts
mkdir -p ~/scripts

# Crear script simple
cat > ~/scripts/log_minutos.sh << 'EOF'
#!/bin/bash

# Archivo de log
LOG_FILE="$HOME/logs/sistema_minutos.log"
mkdir -p "$HOME/logs"

# Escribir fecha y hora
echo "$(date): Sistema activo - Memoria libre: $(free -h | awk 'NR==2{print $7}')" >> "$LOG_FILE"
EOF

# Dar permisos
chmod +x ~/scripts/log_minutos.sh
```

**Paso 2:** Configurar en crontab
```bash
# Abrir crontab
crontab -e

# Agregar esta línea:
*/2 * * * * /home/$USER/scripts/log_minutos.sh
```

**Explicación:** Se ejecuta cada 2 minutos (*/2 en el campo de minutos).

### Práctica 2: Contador de Procesos cada 3 Minutos

**Objetivo:** Contar cuántos procesos están ejecutándose y guardarlo en un log cada 3 minutos.

**Paso 1:** Crear el script
```bash
cat > ~/scripts/contador_procesos.sh << 'EOF'
#!/bin/bash

LOG_FILE="$HOME/logs/procesos.log"
mkdir -p "$HOME/logs"

# Contar procesos
PROCESOS=$(ps aux | wc -l)
USUARIOS=$(who | wc -l)

# Escribir al log
echo "$(date): $PROCESOS procesos activos, $USUARIOS usuarios conectados" >> "$LOG_FILE"
EOF

chmod +x ~/scripts/contador_procesos.sh
```

**Paso 2:** Programar cada 3 minutos
```bash
crontab -e

# Agregar:
*/3 * * * * /home/$USER/scripts/contador_procesos.sh
```

**Explicación:** Se ejecuta cada 3 minutos (*/3 en el campo de minutos).

### Práctica 3: Backup Automático Diario

**Objetivo:** Crear un script que haga backup de una carpeta importante todos los días a las 2:00 AM.

**Paso 1:** Crear el script de backup
```bash
# Crear directorio para scripts
mkdir -p ~/scripts

# Crear el script de backup
cat > ~/scripts/backup_diario.sh << 'EOF'
#!/bin/bash

# Variables
FECHA=$(date +%Y%m%d_%H%M%S)
ORIGEN="$HOME/Documentos"
DESTINO="$HOME/backups"
ARCHIVO="backup_documentos_$FECHA.tar.gz"

# Crear directorio de backups si no existe
mkdir -p "$DESTINO"

# Crear backup comprimido
tar -czf "$DESTINO/$ARCHIVO" "$ORIGEN"

# Registrar en log
echo "$(date): Backup creado: $ARCHIVO" >> "$HOME/backups/backup.log"

# Eliminar backups más antiguos de 7 días
find "$DESTINO" -name "backup_documentos_*.tar.gz" -mtime +7 -delete
EOF

# Dar permisos de ejecución
chmod +x ~/scripts/backup_diario.sh
```

**Paso 2:** Configurar en crontab
```bash
# Abrir crontab
crontab -e

# Agregar la siguiente línea:
0 2 * * * /home/$USER/scripts/backup_diario.sh
```

**Explicación:** Esta tarea se ejecutará todos los días a las 2:00 AM (0 minutos, 2 horas).

### Práctica 2: Monitor de Espacio en Disco

**Objetivo:** Verificar el espacio en disco cada hora y enviar alerta si supera el 80%.

**Paso 1:** Crear el script de monitoreo
```bash
cat > ~/scripts/monitor_disco.sh << 'EOF'
#!/bin/bash

# Obtener uso del disco raíz
USO=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

# Umbral de alerta (80%)
UMBRAL=80

# Archivo de log
LOG_FILE="$HOME/logs/monitor_disco.log"
mkdir -p "$HOME/logs"

if [ "$USO" -gt "$UMBRAL" ]; then
    MENSAJE="¡ALERTA! Espacio en disco al ${USO}% - $(date)"
    echo "$MENSAJE" >> "$LOG_FILE"

    # Enviar notificación al usuario (si está logueado)
    if [ -n "$DISPLAY" ]; then
        notify-send "Espacio en Disco" "$MENSAJE"
    fi
else
    echo "Espacio en disco OK: ${USO}% - $(date)" >> "$LOG_FILE"
fi
EOF

chmod +x ~/scripts/monitor_disco.sh
```

**Paso 2:** Programar ejecución cada hora
```bash
crontab -e

# Agregar:
0 * * * * /home/$USER/scripts/monitor_disco.sh
```

**Explicación:** Se ejecuta al minuto 0 de cada hora.

### Práctica 3: Limpieza Automática de Archivos Temporales

**Objetivo:** Limpiar archivos temporales y cache del sistema cada domingo a las 3:00 AM.

**Paso 1:** Crear script de limpieza
```bash
cat > ~/scripts/limpieza_semanal.sh << 'EOF'
#!/bin/bash

LOG_FILE="$HOME/logs/limpieza.log"
mkdir -p "$HOME/logs"

echo "=== Inicio limpieza semanal - $(date) ===" >> "$LOG_FILE"

# Limpiar cache de apt
sudo apt-get autoclean >> "$LOG_FILE" 2>&1
sudo apt-get autoremove -y >> "$LOG_FILE" 2>&1

# Limpiar archivos temporales del usuario
find "$HOME/.cache" -type f -atime +7 -delete 2>/dev/null
echo "Cache de usuario limpiado" >> "$LOG_FILE"

# Limpiar papelera
if [ -d "$HOME/.local/share/Trash/files" ]; then
    rm -rf "$HOME/.local/share/Trash/files/*" 2>/dev/null
    echo "Papelera vaciada" >> "$LOG_FILE"
fi

# Limpiar logs antiguos
find "$HOME/logs" -name "*.log" -mtime +30 -delete 2>/dev/null

echo "=== Fin limpieza semanal - $(date) ===" >> "$LOG_FILE"
EOF

chmod +x ~/scripts/limpieza_semanal.sh
```

**Paso 2:** Programar para domingos
```bash
crontab -e

# Agregar:
0 3 * * 0 /home/$USER/scripts/limpieza_semanal.sh
```

**Explicación:** Se ejecuta los domingos (0) a las 3:00 AM.

### Práctica 4: Sincronización de Archivos con Servidor Remoto

**Objetivo:** Sincronizar una carpeta local con un servidor remoto cada 6 horas usando rsync.

**Paso 1:** Configurar acceso SSH sin contraseña (prerequisito)
```bash
# Generar clave SSH si no existe
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -C "backup@$(hostname)" -f ~/.ssh/id_rsa -N ""
fi

# Copiar clave al servidor remoto (reemplazar con datos reales)
# ssh-copy-id usuario@servidor.ejemplo.com
```

**Paso 2:** Crear script de sincronización
```bash
cat > ~/scripts/sync_remoto.sh << 'EOF'
#!/bin/bash

# Configuración
SERVIDOR="usuario@servidor.ejemplo.com"
CARPETA_LOCAL="$HOME/Documentos/importante"
CARPETA_REMOTA="/home/usuario/backup_cliente"
LOG_FILE="$HOME/logs/sync.log"

mkdir -p "$HOME/logs"

echo "=== Inicio sincronización - $(date) ===" >> "$LOG_FILE"

# Verificar conectividad
if ping -c 1 servidor.ejemplo.com >/dev/null 2>&1; then
    # Sincronizar archivos
    rsync -avz --delete \
          --exclude='*.tmp' \
          --exclude='.*' \
          "$CARPETA_LOCAL/" \
          "$SERVIDOR:$CARPETA_REMOTA/" \
          >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        echo "Sincronización exitosa - $(date)" >> "$LOG_FILE"
    else
        echo "Error en sincronización - $(date)" >> "$LOG_FILE"
    fi
else
    echo "Servidor no disponible - $(date)" >> "$LOG_FILE"
fi

echo "=== Fin sincronización - $(date) ===" >> "$LOG_FILE"
EOF

chmod +x ~/scripts/sync_remoto.sh
```

**Paso 3:** Programar cada 6 horas
```bash
crontab -e

# Agregar:
0 */6 * * * /home/$USER/scripts/sync_remoto.sh
```

**Explicación:** Se ejecuta cada 6 horas (*/6).

## Verificación y Troubleshooting

### Verificar que Cron está funcionando
```bash
# Ver estado del servicio
sudo systemctl status cron

# Verificar logs recientes
sudo grep CRON /var/log/syslog | tail -10

# Ver tareas programadas del usuario
crontab -l
```

### Problemas Comunes

1. **Scripts no se ejecutan:**
   - Verificar permisos de ejecución: `chmod +x script.sh`
   - Usar rutas absolutas en crontab
   - Verificar variables de entorno

2. **Paths y variables de entorno:**
   ```bash
   # Al inicio del crontab agregar:
   PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
   HOME=/home/usuario
   ```

3. **Debugging:**
   ```bash
   # Agregar al final de la línea de crontab para capturar errores:
   0 2 * * * /home/user/script.sh >> /tmp/cron.log 2>&1
   ```

## Ejemplos Adicionales de Horarios

```bash
# Cada minuto
* * * * * comando

# Cada 5 minutos
*/5 * * * * comando

# Todos los días a las 12:30 PM
30 12 * * * comando

# Lunes a viernes a las 9:00 AM
0 9 * * 1-5 comando

# Primer día de cada mes a las 6:00 AM
0 6 1 * * comando

# Cada 2 horas
0 */2 * * * comando

# Solo en enero y julio
0 0 1 1,7 * comando
```

---