# Tarea: Programacion Shell en Ubuntu 24

## Parte Teorica

### 1. Conceptos Fundamentales

**Shell** es el interprete de comandos que actua como interfaz entre el usuario y el kernel de Linux. En Ubuntu 24, el shell por defecto es **Bash** (Bourne Again Shell).

### Tipos de Shell disponibles en Ubuntu 24:

| Shell | Ruta | Descripcion |
|-------|------|-------------|
| bash | `/bin/bash` | Shell por defecto, scripting robusto |
| sh | `/bin/sh` | Shell POSIX, enlace a dash en Ubuntu |
| zsh | `/bin/zsh` | Shell avanzado con autocompletado |
| dash | `/bin/dash` | Shell minimalista, rapido para scripts |

### 2. Estructura de un script Shell

```bash
#!/bin/bash
# Shebang: indica al sistema que interprete usar
# Comentarios: documentan el codigo

# Variables (sin espacios alrededor del =)
NOMBRE="valor"

# Lectura de entrada
read -p "Ingrese dato: " variable

# Estructuras de control
if [ condicion ]; then
    comandos
elif [ otra_condicion ]; then
    comandos
else
    comandos
fi

# Bucles
for i in 1 2 3; do
    echo "$i"
done

while [ condicion ]; do
    comandos
done

# Funciones
mi_funcion() {
    echo "Argumento 1: $1"
    return 0
}
```

### 3. Operadores de comparacion

| Numerico | Cadena | Descripcion |
|----------|--------|-------------|
| `-eq` | `=` | Igual |
| `-ne` | `!=` | Diferente |
| `-gt` | | Mayor que |
| `-lt` | | Menor que |
| `-ge` | | Mayor o igual |
| `-le` | | Menor o igual |
| | `-z` | Cadena vacia |
| | `-n` | Cadena no vacia |

### 4. Operadores de archivos

| Operador | Descripcion |
|----------|-------------|
| `-f` | Es archivo regular |
| `-d` | Es directorio |
| `-r` | Tiene permiso de lectura |
| `-w` | Tiene permiso de escritura |
| `-x` | Tiene permiso de ejecucion |
| `-s` | Archivo no esta vacio |
| `-e` | Existe |

### 5. Variables especiales

| Variable | Significado |
|----------|-------------|
| `$0` | Nombre del script |
| `$1..$9` | Argumentos posicionales |
| `$#` | Numero de argumentos |
| `$@` | Todos los argumentos (como lista) |
| `$*` | Todos los argumentos (como cadena) |
| `$?` | Codigo de salida del ultimo comando |
| `$$` | PID del proceso actual |
| `$!` | PID del ultimo proceso en background |

---

## Parte Practica

### Ejercicio: Sistema de Gestion de Usuarios del Sistema

Crear un script llamado `gestion_usuarios.sh` que funcione como un menu interactivo para administrar informacion de usuarios en Ubuntu 24.

### Requisitos:

1. Mostrar un menu con las siguientes opciones:
   - Listar usuarios activos del sistema
   - Buscar un usuario por nombre
   - Mostrar informacion detallada de un usuario
   - Generar reporte de uso de disco por usuario
   - Mostrar los ultimos accesos al sistema
   - Salir

2. Usar funciones para cada opcion
3. Validar entradas del usuario
4. Manejar errores con mensajes claros
5. Generar un log de las operaciones realizadas

---

### Solucion:

```bash
#!/bin/bash
#============================================================
# gestion_usuarios.sh
# Sistema de Gestion de Usuarios para Ubuntu 24
# Uso: chmod +x gestion_usuarios.sh && ./gestion_usuarios.sh
#============================================================

# --- Configuracion ---
LOG_FILE="/tmp/gestion_usuarios_$(date +%Y%m%d).log"
SEPARADOR="============================================"

# --- Colores para la terminal ---
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
SIN_COLOR='\033[0m'

# --- Funciones auxiliares ---

escribir_log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

mostrar_titulo() {
    echo ""
    echo -e "${AZUL}${SEPARADOR}${SIN_COLOR}"
    echo -e "${AZUL}  $1${SIN_COLOR}"
    echo -e "${AZUL}${SEPARADOR}${SIN_COLOR}"
    echo ""
}

mostrar_exito() {
    echo -e "${VERDE}[OK] $1${SIN_COLOR}"
}

mostrar_error() {
    echo -e "${ROJO}[ERROR] $1${SIN_COLOR}"
}

mostrar_aviso() {
    echo -e "${AMARILLO}[AVISO] $1${SIN_COLOR}"
}

pausar() {
    echo ""
    read -p "Presione ENTER para continuar..."
}

# --- Funciones principales ---

listar_usuarios() {
    mostrar_titulo "USUARIOS ACTIVOS DEL SISTEMA"
    escribir_log "Listado de usuarios activos"

    echo "Usuario         | UID  | Shell           | Directorio Home"
    echo "----------------|------|-----------------|------------------"

    # Filtrar usuarios reales (UID >= 1000) y root
    while IFS=: read -r usuario _ uid _ _ home shell; do
        if [ "$uid" -ge 1000 ] 2>/dev/null || [ "$usuario" = "root" ]; then
            printf "%-16s| %-5s| %-16s| %s\n" "$usuario" "$uid" "$shell" "$home"
        fi
    done < /etc/passwd

    TOTAL=$(awk -F: '$3 >= 1000 {count++} END {print count}' /etc/passwd)
    echo ""
    mostrar_exito "Total de usuarios regulares: $TOTAL"
    pausar
}

buscar_usuario() {
    mostrar_titulo "BUSCAR USUARIO"

    read -p "Ingrese nombre o parte del nombre: " busqueda

    if [ -z "$busqueda" ]; then
        mostrar_error "Debe ingresar un termino de busqueda"
        pausar
        return 1
    fi

    escribir_log "Busqueda de usuario: $busqueda"

    echo ""
    echo "Resultados para '$busqueda':"
    echo "$SEPARADOR"

    RESULTADOS=$(grep -i "$busqueda" /etc/passwd)

    if [ -z "$RESULTADOS" ]; then
        mostrar_aviso "No se encontraron usuarios con '$busqueda'"
    else
        echo "$RESULTADOS" | while IFS=: read -r usuario _ uid gid info home shell; do
            echo "  Usuario: $usuario"
            echo "  UID/GID: $uid/$gid"
            echo "  Info:    ${info:-Sin informacion}"
            echo "  Home:    $home"
            echo "  Shell:   $shell"
            echo "  ---"
        done
        TOTAL=$(echo "$RESULTADOS" | wc -l)
        mostrar_exito "Se encontraron $TOTAL resultado(s)"
    fi

    pausar
}

info_usuario() {
    mostrar_titulo "INFORMACION DETALLADA DE USUARIO"

    read -p "Ingrese el nombre de usuario: " nombre

    if [ -z "$nombre" ]; then
        mostrar_error "Debe ingresar un nombre de usuario"
        pausar
        return 1
    fi

    # Verificar si el usuario existe
    if ! id "$nombre" &>/dev/null; then
        mostrar_error "El usuario '$nombre' no existe"
        pausar
        return 1
    fi

    escribir_log "Consulta de info para usuario: $nombre"

    echo "--- Informacion de identidad ---"
    id "$nombre"

    echo ""
    echo "--- Grupos ---"
    groups "$nombre"

    echo ""
    echo "--- Datos de /etc/passwd ---"
    LINEA=$(grep "^${nombre}:" /etc/passwd)
    echo "  Linea completa: $LINEA"

    echo ""
    echo "--- Estado de la cuenta ---"
    passwd -S "$nombre" 2>/dev/null || mostrar_aviso "Sin permisos para ver estado de password"

    echo ""
    echo "--- Procesos activos ---"
    PROCS=$(ps -u "$nombre" --no-headers 2>/dev/null | wc -l)
    echo "  Procesos en ejecucion: $PROCS"

    if [ "$PROCS" -gt 0 ]; then
        echo ""
        echo "  PID    | Comando"
        echo "  -------|--------"
        ps -u "$nombre" -o pid,comm --no-headers 2>/dev/null | head -10 | while read -r pid cmd; do
            printf "  %-7s| %s\n" "$pid" "$cmd"
        done
        [ "$PROCS" -gt 10 ] && echo "  ... y $((PROCS - 10)) procesos mas"
    fi

    pausar
}

reporte_disco() {
    mostrar_titulo "REPORTE DE USO DE DISCO POR USUARIO"
    escribir_log "Generacion de reporte de disco"

    echo "Calculando uso de disco en /home..."
    echo "(Puede requerir permisos de root para otros usuarios)"
    echo ""
    echo "Directorio           | Tamano"
    echo "---------------------|--------"

    # Obtener tamano de cada directorio home
    for dir in /home/*/; do
        if [ -d "$dir" ]; then
            usuario=$(basename "$dir")
            tamano=$(du -sh "$dir" 2>/dev/null | cut -f1)
            printf "%-21s| %s\n" "$usuario" "${tamano:-sin acceso}"
        fi
    done

    echo ""
    echo "--- Resumen del sistema ---"
    echo "Uso total de /home:"
    du -sh /home/ 2>/dev/null || mostrar_aviso "Sin permisos para calcular total"

    echo ""
    echo "Espacio en disco:"
    df -h / | tail -1 | awk '{
        printf "  Total: %s | Usado: %s (%s) | Disponible: %s\n",
               $2, $3, $5, $4
    }'

    pausar
}

ultimos_accesos() {
    mostrar_titulo "ULTIMOS ACCESOS AL SISTEMA"
    escribir_log "Consulta de ultimos accesos"

    echo "--- Ultimos 15 accesos ---"
    echo ""
    last -15 2>/dev/null || mostrar_error "No se pudo obtener el historial de accesos"

    echo ""
    echo "--- Usuarios actualmente conectados ---"
    echo ""
    CONECTADOS=$(who 2>/dev/null)
    if [ -z "$CONECTADOS" ]; then
        mostrar_aviso "No hay otros usuarios conectados"
    else
        echo "$CONECTADOS"
        echo ""
        TOTAL=$(echo "$CONECTADOS" | wc -l)
        mostrar_exito "Sesiones activas: $TOTAL"
    fi

    echo ""
    echo "--- Ultimo acceso por usuario ---"
    echo ""
    lastlog 2>/dev/null | grep -v "Never" | head -20 || mostrar_aviso "Sin permisos"

    pausar
}

# --- Menu principal ---

mostrar_menu() {
    clear
    echo -e "${AZUL}"
    echo "  +--------------------------------------------+"
    echo "  |   SISTEMA DE GESTION DE USUARIOS           |"
    echo "  |   Ubuntu 24 - Shell Script                 |"
    echo "  +--------------------------------------------+"
    echo "  |                                            |"
    echo "  |  1) Listar usuarios activos                |"
    echo "  |  2) Buscar usuario por nombre              |"
    echo "  |  3) Informacion detallada de usuario       |"
    echo "  |  4) Reporte de uso de disco                |"
    echo "  |  5) Ultimos accesos al sistema             |"
    echo "  |  6) Salir                                  |"
    echo "  |                                            |"
    echo "  +--------------------------------------------+"
    echo -e "${SIN_COLOR}"
    echo -e "  Log: ${AMARILLO}${LOG_FILE}${SIN_COLOR}"
    echo ""
}

# --- Bucle principal ---

escribir_log "=== Inicio de sesion del sistema de gestion ==="

while true; do
    mostrar_menu
    read -p "  Seleccione una opcion [1-6]: " opcion

    case $opcion in
        1) listar_usuarios ;;
        2) buscar_usuario ;;
        3) info_usuario ;;
        4) reporte_disco ;;
        5) ultimos_accesos ;;
        6)
            escribir_log "=== Fin de sesion ==="
            mostrar_exito "Hasta luego. Log guardado en: $LOG_FILE"
            echo ""
            exit 0
            ;;
        *)
            mostrar_error "Opcion invalida. Use un numero del 1 al 6."
            sleep 1
            ;;
    esac
done
```

---

## Preguntas Teoricas de Evaluacion

**1.** Que es el shebang (`#!/bin/bash`) y por que es importante?

**2.** Cual es la diferencia entre `$@` y `$*` al estar entre comillas dobles?


**3.** Que hace `2>/dev/null` y por que se usa en el script?


**4.** Explique la diferencia entre `[ ]` y `[[ ]]` en Bash.


**5.** Por que usamos `read -r` en lugar de solo `read` al leer archivos?


**6.** Que sucede si no se pone `exit 0` al final del script?


**7.** Explique que hace el pipeline: `awk -F: '$3 >= 1000 {count++} END {print count}' /etc/passwd`


**8.** Cual es la diferencia entre `>` y `>>` en la redireccion de salida?


---

## Como ejecutar

```bash
# 1. Crear el archivo
nano gestion_usuarios.sh

# 2. Copiar el contenido del script

# 3. Dar permisos de ejecucion
chmod +x gestion_usuarios.sh

# 4. Ejecutar
./gestion_usuarios.sh

# 5. (Opcional) Ejecutar con permisos elevados para ver todo
sudo ./gestion_usuarios.sh
```

---

