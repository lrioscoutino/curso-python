# Modulo 1: Introduccion a la Seguridad en Sistemas Operativos Ubuntu

## 1.1 Conceptos Fundamentales

### Que es la seguridad informatica?

La seguridad informatica es el conjunto de medidas preventivas y reactivas que protegen
la integridad, confidencialidad y disponibilidad de la informacion y los recursos de un sistema.

### La Triada CIA

```
        Confidencialidad
            /\
           /  \
          /    \
         /      \
        /________\
 Integridad    Disponibilidad
```

- **Confidencialidad**: Solo usuarios autorizados acceden a la informacion
- **Integridad**: Los datos no son alterados sin autorizacion
- **Disponibilidad**: Los recursos estan accesibles cuando se necesitan

### Ejemplos de la triada CIA en la vida real

```
Confidencialidad:
  - Tu contrasena de email: solo TU debes conocerla
  - Historial medico: solo tu doctor debe verlo
  - Codigo fuente de una empresa: solo los desarrolladores autorizados

Integridad:
  - Una transferencia bancaria por $1,000 no debe cambiar a $10,000 en el camino
  - Una receta medica no debe ser alterada
  - Un archivo de configuracion del servidor no debe ser modificado sin autorizacion

Disponibilidad:
  - El sitio web de un banco debe funcionar 24/7
  - El sistema de emergencias (911) no puede "caerse"
  - Tu servidor debe responder cuando los usuarios lo necesitan
```

### Principio de Menor Privilegio

> Un usuario o proceso solo debe tener los permisos minimos necesarios para realizar su tarea.

```
Ejemplo cotidiano:
  Un empleado de caja en una tienda:
    - SI puede: cobrar productos, dar cambio
    - NO puede: abrir la caja fuerte, cambiar precios, ver nominas

Ejemplo en Linux:
  Un servidor web (nginx):
    - SI puede: leer archivos HTML/CSS/JS, escuchar conexiones web
    - NO puede: leer contrasenas del sistema, instalar programas, borrar archivos del sistema
```

### Defensa en Profundidad

No depender de una sola capa de seguridad. Implementar multiples barreras:

```
Analogia: Seguridad de una casa

  [Calle]       -> [Reja]    -> [Puerta]   -> [Alarma]    -> [Caja fuerte]
  Cualquiera       1ra barrera  2da barrera    3ra barrera    4ta barrera

En un servidor:

  [Internet]    -> [Firewall] -> [SSH]      -> [Permisos]  -> [Cifrado]
  Trafico externo  Filtra       Solo con      Solo archivos   Datos
                   puertos      clave SSH     permitidos      protegidos
```

### Principio de Minima Exposicion

> Si no necesitas un servicio, desactivalo. Lo que no existe, no se puede atacar.

```
Servidor web:
  Necesita:  Nginx, SSH
  NO necesita: Bluetooth, impresoras, FTP, servidor de correo

  Cada servicio activo = una puerta mas que un atacante puede intentar abrir
```

## 1.2 Superficie de Ataque en Ubuntu

### Que es la superficie de ataque?

> Es el conjunto de todos los puntos por donde un atacante podria intentar entrar a tu sistema.

```
Analogia: Tu casa
  - Puerta principal (puede forzarse)
  - Ventanas (pueden romperse)
  - Garage (puede abrirse)
  - Red WiFi (puede hackearse)

Tu servidor Ubuntu:
  - Puertos abiertos (SSH, HTTP, etc.)
  - Software instalado (puede tener vulnerabilidades)
  - Usuarios (contrasenas debiles)
  - Configuraciones (permisos excesivos)

REGLA: Menos superficie de ataque = mas seguro
  -> Cierra puertos innecesarios
  -> Desinstala software que no uses
  -> Elimina usuarios innecesarios
```

### Vectores de ataque comunes

| Vector | Que es | Ejemplo | Como protegerse |
|--------|--------|---------|-----------------|
| Red | Ataques por la red/internet | Alguien intenta adivinar tu contrasena SSH miles de veces | Firewall, Fail2Ban, claves SSH |
| Aplicaciones | Bugs en el software | Un programa con un error permite ejecutar comandos | Actualizaciones, AppArmor |
| Usuarios | Engano a personas | Email falso que pide tu contrasena | Capacitacion, 2FA |
| Fisico | Acceso al equipo | Alguien conecta una USB maliciosa | Cifrado de disco, BIOS con contrasena |
| Configuracion | Ajustes inseguros | Dejar permisos 777 en archivos importantes | Auditorias, principio de menor privilegio |

### Que es un ataque de fuerza bruta?

```
Atacante intenta adivinar tu contrasena probando miles de combinaciones:

  Intento 1:  usuario: admin  password: 123456      -> Fallido
  Intento 2:  usuario: admin  password: password     -> Fallido
  Intento 3:  usuario: admin  password: admin123     -> Fallido
  ...
  Intento 9847: usuario: admin  password: S3gur@2024 -> EXITO!

  Programas automaticos pueden probar miles de contrasenas por segundo.

  Defensa:
    - Contrasenas largas y complejas (minimo 12 caracteres)
    - Bloquear IPs despues de varios intentos fallidos (Fail2Ban)
    - Usar claves SSH en lugar de contrasenas
    - Limitar quien puede conectarse (firewall)
```

### Que es una vulnerabilidad?

```
Una vulnerabilidad es un error o debilidad en el software que puede ser explotada.

Ejemplo real simplificado:
  Un programa espera recibir un nombre de 50 caracteres maximo.
  Si le envias 5000 caracteres, el programa se confunde
  y el atacante puede ejecutar sus propios comandos.
  Esto se llama "buffer overflow".

  Defensa:
    - Mantener TODO el software actualizado
    - Los parches de seguridad corrigen estas vulnerabilidades
    - Por eso las actualizaciones son tan importantes
```

## 1.3 Practica: Auditoria Inicial del Sistema

Una auditoria es revisar el estado actual de seguridad de tu sistema.

### Verificar version del sistema

```bash
# Version de Ubuntu
lsb_release -a

# Version del kernel (el corazon del sistema operativo)
uname -r

# Arquitectura del procesador
uname -m

# Informacion completa del sistema
hostnamectl
```

### Verificar usuarios del sistema

```bash
# Listar todos los usuarios del sistema
# Cada linea tiene el formato: usuario:x:UID:GID:comentario:home:shell
cat /etc/passwd

# Listar solo usuarios que pueden iniciar sesion
# (los que tienen bash u otro shell, no /nologin)
grep -v '/nologin\|/false' /etc/passwd

# Ver usuarios con UID 0 (privilegios de root)
# SOLO deberia aparecer "root". Si hay otro, es sospechoso.
awk -F: '($3 == "0") {print $1}' /etc/passwd

# Ver quien puede usar sudo (ejecutar comandos como administrador)
getent group sudo
```

### Verificar servicios activos y puertos

```bash
# Ver que servicios estan corriendo
# Un servicio es un programa que corre en segundo plano
systemctl list-units --type=service --state=running

# Ver que puertos estan abiertos y que programa los usa
# RECUERDA: cada puerto abierto es una "puerta" que podria ser atacada
ss -tulnp

# Explicacion de las banderas:
#  -t = mostrar TCP
#  -u = mostrar UDP
#  -l = solo los que estan escuchando (LISTEN)
#  -n = mostrar numeros de puerto (no nombres)
#  -p = mostrar que programa usa cada puerto
```

### Verificar actualizaciones pendientes

```bash
# Actualizar la lista de paquetes disponibles
sudo apt update

# Ver que actualizaciones hay disponibles
apt list --upgradable

# Ver actualizaciones de seguridad pendientes
sudo unattended-upgrade --dry-run
```

### Verificar configuracion del firewall

```bash
# Ver si el firewall esta activo
sudo ufw status

# Si dice "inactive", tu sistema NO tiene firewall activo
# Esto significa que TODOS los puertos estan expuestos
```

## 1.4 Tipos de Amenazas que Debes Conocer

### Malware (software malicioso)

```
+----------------+------------------------------------------------+
| Tipo           | Que hace                                       |
+----------------+------------------------------------------------+
| Virus          | Se adjunta a programas y se propaga            |
| Ransomware     | Cifra tus archivos y pide rescate ($$$)        |
| Rootkit        | Se esconde en el sistema para dar acceso       |
|                | permanente al atacante                         |
| Cryptominer    | Usa tu CPU para minar criptomonedas            |
|                | (tu servidor va lento sin razon aparente)      |
| Backdoor       | Puerta trasera: acceso secreto al sistema      |
+----------------+------------------------------------------------+

Linux no es inmune a malware!
Los servidores Linux son objetivos frecuentes porque:
  - Estan siempre encendidos
  - Tienen buena conexion a Internet
  - Pueden tener datos valiosos
```

### Ingenieria social

```
No atacan la tecnologia, atacan a las PERSONAS.

Ejemplo 1 - Phishing:
  "Hola sysadmin, soy del equipo de seguridad de la empresa.
   Necesito tu contrasena de root para una auditoria urgente."
   -> NUNCA dar contrasenas por email/telefono/chat

Ejemplo 2 - Pretexting:
  "Soy el nuevo desarrollador, me puedes dar acceso SSH al servidor
   de produccion? El jefe dijo que era urgente."
   -> Siempre verificar identidad por canales oficiales

Defensa: La tecnologia no puede proteger contra un humano
que voluntariamente da sus credenciales.
```

## 1.5 Modelo de Amenazas: De que te proteges?

Antes de asegurar un sistema, preguntate:

```
1. QUE protejo?
   - Datos de usuarios
   - Codigo fuente
   - Base de datos
   - Disponibilidad del servicio

2. DE QUIEN me protejo?
   - Bots automaticos (lo mas comun)
   - Hackers oportunistas
   - Empleados maliciosos (amenaza interna)
   - Atacantes dirigidos (poco comun para la mayoria)

3. QUE pasa si fallo?
   - Robo de datos -> multas legales, perdida de confianza
   - Servidor caido -> perdida de ingresos
   - Ransomware -> perdida total de datos

4. QUE recursos tengo?
   - Tiempo para configurar seguridad
   - Conocimiento tecnico
   - Presupuesto para herramientas
```

## 1.6 Ejercicio Practico

Realiza una auditoria inicial de tu sistema respondiendo:

1. Que version de Ubuntu tienes instalada?
2. Cuantos usuarios tienen shell de login?
3. Existe algun usuario con UID 0 ademas de root?
4. Cuantos servicios estan corriendo actualmente?
5. Cuantos puertos estan abiertos y escuchando?
6. Tienes actualizaciones de seguridad pendientes?
7. Tu firewall esta activo?

Documenta los resultados.

### Script de auditoria automatica

Copia y ejecuta este script para obtener un reporte rapido:

```bash
#!/bin/bash
echo "==========================================="
echo "  AUDITORIA INICIAL DE SEGURIDAD"
echo "  Fecha: $(date)"
echo "  Host: $(hostname)"
echo "==========================================="

echo ""
echo "--- Sistema Operativo ---"
lsb_release -d 2>/dev/null || cat /etc/os-release | grep PRETTY
echo "Kernel: $(uname -r)"

echo ""
echo "--- Red ---"
echo "IP privada: $(hostname -I)"
echo "Gateway: $(ip route | grep default | awk '{print $3}')"

echo ""
echo "--- Usuarios con shell de login ---"
grep -v '/nologin\|/false' /etc/passwd | awk -F: '{print "  " $1 " (UID:" $3 ")"}'

echo ""
echo "--- Usuarios con UID 0 (root) ---"
awk -F: '($3 == "0") {print "  " $1}' /etc/passwd

echo ""
echo "--- Servicios activos ---"
systemctl list-units --type=service --state=running --no-pager | grep ".service" | wc -l
echo "  servicios corriendo"

echo ""
echo "--- Puertos abiertos ---"
ss -tulnp 2>/dev/null | grep LISTEN | awk '{print "  " $5}' | sort -u

echo ""
echo "--- Firewall ---"
sudo ufw status 2>/dev/null || echo "  UFW no instalado"

echo ""
echo "--- Actualizaciones pendientes ---"
apt list --upgradable 2>/dev/null | grep -c upgradable
echo "  paquetes por actualizar"

echo ""
echo "==========================================="
echo "  FIN DE AUDITORIA"
echo "==========================================="
```

Guarda el script y ejecutalo:

```bash
# Guardar el script
nano auditoria.sh

# Darle permisos de ejecucion
chmod +x auditoria.sh

# Ejecutar
sudo bash auditoria.sh
```
