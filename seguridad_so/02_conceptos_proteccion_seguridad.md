# Modulo 2: Concepto y Objetivos de Proteccion y Seguridad (Tema 6.1)

## 2.1 Teoria: Diferencia entre Proteccion y Seguridad

Aunque se usan como sinonimos, en sistemas operativos tienen significados distintos:

```
+-------------------+------------------------------------------------+
| Concepto          | Definicion                                     |
+-------------------+------------------------------------------------+
| PROTECCION        | Mecanismos INTERNOS del SO que controlan el    |
|                   | acceso de procesos y usuarios a recursos.      |
|                   | Se enfoca en: quien puede hacer que.           |
+-------------------+------------------------------------------------+
| SEGURIDAD         | Conjunto de politicas y mecanismos que          |
|                   | defienden al sistema contra amenazas           |
|                   | EXTERNAS e INTERNAS (ataques, errores, etc).   |
+-------------------+------------------------------------------------+
```

### Analogia

```
PROTECCION = las cerraduras, llaves y permisos dentro de un edificio
  -> La puerta del laboratorio solo la abre quien tiene la llave correcta
  -> El ascensor de servicio solo funciona con tarjeta de empleado

SEGURIDAD = el sistema completo de defensa del edificio
  -> Guardias, camaras, alarmas, protocolos de emergencia
  -> Incluye la proteccion, pero tambien ataques externos, desastres, etc.
```

### Relacion entre ambos

```
  ┌─────────────────────────────────┐
  │         SEGURIDAD               │
  │  (politicas, autenticacion,     │
  │   cifrado, auditorias)          │
  │                                 │
  │    ┌───────────────────┐        │
  │    │   PROTECCION      │        │
  │    │  (control acceso, │        │
  │    │   permisos, ACLs) │        │
  │    └───────────────────┘        │
  │                                 │
  └─────────────────────────────────┘

  La proteccion es un SUBCONJUNTO de la seguridad.
  Puedes tener proteccion sin seguridad completa,
  pero no puedes tener seguridad sin proteccion.
```

## 2.2 Objetivos de la Proteccion

```
1. CONTROLAR ACCESO A RECURSOS
   - Archivos, memoria, CPU, dispositivos I/O
   - Cada proceso solo accede a lo que necesita

2. PREVENIR ERRORES ACCIDENTALES
   - Un proceso con bug no debe corromper datos de otro
   - Ej: un programa mal escrito no debe borrar /etc/passwd

3. GARANTIZAR AISLAMIENTO
   - Los procesos de usuario A no leen memoria de usuario B
   - Cada proceso vive en su "burbuja" (espacio de direcciones)

4. APLICAR PRINCIPIO DE MENOR PRIVILEGIO
   - Minimos permisos necesarios para la tarea
   - Un servidor web no necesita ser root

5. DETECTAR VIOLACIONES
   - Registrar intentos de acceso no autorizado
   - Logs, auditorias, alertas
```

## 2.3 Objetivos de la Seguridad

```
1. CONFIDENCIALIDAD
   - Solo usuarios autorizados leen la informacion
   - Mecanismos: cifrado, permisos, ACLs

2. INTEGRIDAD
   - Los datos no se modifican sin autorizacion
   - Mecanismos: checksums, firmas digitales, permisos de escritura

3. DISPONIBILIDAD
   - Los recursos estan accesibles cuando se necesitan
   - Mecanismos: redundancia, backups, proteccion contra DoS

4. AUTENTICACION
   - Verificar que el usuario es quien dice ser
   - Mecanismos: passwords, tokens, biometria, certificados

5. NO REPUDIO
   - Un usuario no puede negar haber realizado una accion
   - Mecanismos: logs, firmas digitales, auditorias
```

## 2.4 Dominios de Proteccion

Un **dominio de proteccion** define un conjunto de pares (recurso, permisos):

```
Dominio D1 = { (archivo1, leer), (archivo2, leer+escribir), (impresora, usar) }
Dominio D2 = { (archivo1, leer+escribir+ejecutar), (red, enviar) }
Dominio D3 = { (archivo3, leer), (memoria_compartida, leer+escribir) }

Cada proceso se ejecuta dentro de un dominio.
Un proceso en D1 puede leer archivo1 pero NO escribirlo.
Un proceso en D2 SI puede escribir archivo1.
```

### Dominios en Linux

```
En Linux, cada proceso tiene un dominio definido por:

1. UID (User ID) - identifica al usuario
2. GID (Group ID) - identifica al grupo
3. Bits de permisos (rwx) en cada archivo
4. Capabilities del kernel (permisos granulares de root)

Ejemplo:
  Proceso del usuario "www-data" (UID 33):
    - Puede leer /var/www/html/index.html (permisos: 644, owner: www-data)
    - NO puede leer /etc/shadow (permisos: 640, owner: root)
    - NO puede escribir en /usr/bin/ (permisos: 755, owner: root)
```

## 2.5 Practica: Explorando Dominios de Proteccion en Linux

### Ejercicio 1: Ver tu dominio actual

```bash
# Tu identidad actual (tu dominio)
id
# Salida ejemplo: uid=1000(luis) gid=1000(luis) groups=1000(luis),27(sudo)

# El dominio de un proceso especifico
# Busca el PID de un proceso y examina su estado
ps aux | head -5

# Ver el dominio de un proceso por PID
cat /proc/self/status | grep -E "Uid|Gid|Groups|Cap"
```

### Ejercicio 2: Demostrar aislamiento entre dominios

```bash
# Crear dos usuarios de prueba
sudo useradd -m usuario_a
sudo useradd -m usuario_b

# Crear archivo privado para usuario_a
sudo -u usuario_a bash -c 'echo "datos secretos de A" > /home/usuario_a/secreto.txt'
sudo -u usuario_a chmod 600 /home/usuario_a/secreto.txt

# Intentar leer desde usuario_b (debe fallar)
sudo -u usuario_b cat /home/usuario_a/secreto.txt
# Salida esperada: Permission denied

# Ver los permisos
ls -la /home/usuario_a/secreto.txt
# Salida: -rw------- 1 usuario_a usuario_a ... secreto.txt
# Solo el owner (usuario_a) tiene rw, nadie mas
```

### Ejercicio 3: Cambio de dominio con sudo

```bash
# Ver tu dominio actual
whoami
id

# Cambiar al dominio de root temporalmente
sudo whoami
# Salida: root

# Cambiar al dominio de otro usuario
sudo -u usuario_a whoami
# Salida: usuario_a

# Cada vez que usas sudo, CAMBIAS de dominio de proteccion
# Esto se llama "domain switching" en la teoria de SO
```

### Ejercicio 4: Script demostrativo de dominios

```python
#!/usr/bin/env python3
"""
Demuestra como un proceso hereda el dominio de proteccion
del usuario que lo ejecuta.
"""
import os
import stat

def mostrar_dominio():
    """Muestra el dominio de proteccion del proceso actual."""
    print("=== Dominio de Proteccion del Proceso Actual ===")
    print(f"  PID:        {os.getpid()}")
    print(f"  UID real:   {os.getuid()}")
    print(f"  UID efect:  {os.geteuid()}")
    print(f"  GID real:   {os.getgid()}")
    print(f"  GID efect:  {os.getegid()}")
    print(f"  Grupos:     {os.getgroups()}")
    print()

def verificar_acceso(ruta):
    """Verifica que permisos tiene el proceso sobre un archivo."""
    print(f"  Acceso a '{ruta}':")
    print(f"    Lectura:    {'SI' if os.access(ruta, os.R_OK) else 'NO'}")
    print(f"    Escritura:  {'SI' if os.access(ruta, os.W_OK) else 'NO'}")
    print(f"    Ejecucion:  {'SI' if os.access(ruta, os.X_OK) else 'NO'}")

def main():
    mostrar_dominio()

    archivos_prueba = [
        "/etc/passwd",      # Legible por todos
        "/etc/shadow",      # Solo root
        "/tmp",             # Directorio temporal
        "/usr/bin/python3", # Ejecutable
    ]

    print("=== Verificacion de Acceso a Recursos ===")
    for archivo in archivos_prueba:
        if os.path.exists(archivo):
            verificar_acceso(archivo)
            print()

if __name__ == "__main__":
    main()
```

Guarda como `dominio_proteccion.py` y ejecuta:

```bash
# Como usuario normal
python3 dominio_proteccion.py

# Como root (dominio diferente, mas acceso)
sudo python3 dominio_proteccion.py

# Compara las salidas: root tiene acceso a /etc/shadow, tu usuario no
```

### Limpieza

```bash
# Eliminar usuarios de prueba
sudo userdel -r usuario_a
sudo userdel -r usuario_b
```

## 2.6 Resumen del Modulo

```
PROTECCION:
  - Mecanismos internos del SO para controlar acceso
  - Opera con dominios de proteccion (UID, GID, permisos)
  - Previene errores y accesos no autorizados DENTRO del sistema

SEGURIDAD:
  - Marco completo de defensa (incluye proteccion)
  - CIA: Confidencialidad, Integridad, Disponibilidad
  - Autenticacion + No repudio
  - Defiende contra amenazas externas e internas

DOMINIO DE PROTECCION:
  - Conjunto de (recurso, permisos) asignado a un proceso
  - En Linux: definido por UID/GID/capabilities
  - Los procesos pueden cambiar de dominio (sudo, setuid)
```

## 2.7 Preguntas de Repaso

1. Explica la diferencia entre proteccion y seguridad con un ejemplo.
2. Que es un dominio de proteccion? Como se implementa en Linux?
3. Nombra los 5 objetivos de la seguridad y da un ejemplo de cada uno.
4. Por que el principio de menor privilegio es importante?
5. Que pasa cuando ejecutas `sudo`? Como cambia tu dominio?
