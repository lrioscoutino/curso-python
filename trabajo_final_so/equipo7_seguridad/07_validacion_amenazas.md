# Modulo 7: Validacion y Amenazas al Sistema (Tema 6.6)

## 7.1 Teoria: Validacion del Sistema

La validacion verifica que el sistema cumple con las politicas
de seguridad y que no ha sido comprometido.

```
VALIDACION = Responder a: "El sistema esta en un estado seguro?"

Tipos de validacion:
  1. Validacion de entrada:  Verificar datos que entran al sistema
  2. Validacion de estado:   Verificar integridad del sistema
  3. Validacion de identidad: Autenticacion de usuarios/procesos
  4. Validacion continua:    Monitoreo permanente
```

### Validacion de Entrada (Input Validation)

```
TODO dato que entra al sistema es SOSPECHOSO hasta validarse.

Fuentes no confiables:
  - Input del usuario (formularios, CLI, API)
  - Datos de la red (peticiones HTTP, DNS, emails)
  - Archivos subidos
  - Variables de entorno
  - Datos de bases de datos externas

Principio: NUNCA confiar en datos externos.
  Siempre: sanitizar, validar, escapar.
```

## 7.2 Amenazas al Sistema

### Taxonomia de Amenazas

```
┌─────────────────────┬──────────────────────────────────────────────┐
│ Categoria           │ Descripcion                                  │
├─────────────────────┼──────────────────────────────────────────────┤
│ Interrupcion        │ Destruir o inhabilitar un recurso             │
│ (Disponibilidad)    │ Ej: DoS, destruir disco, cortar red          │
├─────────────────────┼──────────────────────────────────────────────┤
│ Intercepcion        │ Acceso no autorizado a informacion            │
│ (Confidencialidad)  │ Ej: Sniffing, keylogger, leer archivos       │
├─────────────────────┼──────────────────────────────────────────────┤
│ Modificacion        │ Alterar datos sin autorizacion                │
│ (Integridad)        │ Ej: Man-in-the-middle, alterar DB, rootkit   │
├─────────────────────┼──────────────────────────────────────────────┤
│ Fabricacion         │ Crear objetos falsos en el sistema            │
│ (Autenticidad)      │ Ej: IP spoofing, phishing, inyeccion de log  │
└─────────────────────┴──────────────────────────────────────────────┘
```

### Amenazas Comunes en Detalle

```
1. MALWARE
   Virus:        Se adjunta a programas, se propaga al ejecutarlos
   Gusano:       Se propaga por la red SIN interaccion del usuario
   Troyano:      Se disfraza de software legitimo
   Ransomware:   Cifra archivos y pide rescate
   Rootkit:      Se oculta en el SO para mantener acceso
   Spyware:      Monitorea actividad del usuario

2. ATAQUES DE RED
   DoS/DDoS:     Inundar el sistema con trafico para inhabilitarlo
   MITM:         Interceptar comunicacion entre dos partes
   Sniffing:     Capturar paquetes de red no cifrados
   DNS Spoofing: Redirigir a sitios falsos via DNS

3. ATAQUES DE APLICACION
   SQL Injection:     Inyectar SQL en inputs
   XSS:               Inyectar JavaScript en paginas web
   Buffer Overflow:   Sobreescribir memoria para ejecutar codigo
   Command Injection: Inyectar comandos del SO

4. ATAQUES DE AUTENTICACION
   Fuerza Bruta:      Probar todas las combinaciones posibles
   Diccionario:       Probar passwords comunes
   Pass the Hash:     Usar hash robado sin conocer el password
   Session Hijacking: Robar token de sesion

5. AMENAZAS INTERNAS
   Empleado malicioso: Abuso de permisos legitimos
   Error humano:       Configuracion incorrecta, click en phishing
   Ingenieria social:  Manipulacion psicologica
```

### Modelo STRIDE (Microsoft)

```
Framework para identificar amenazas sistematicamente:

  S - Spoofing     (Suplantacion de identidad)
  T - Tampering    (Manipulacion de datos)
  R - Repudiation  (Negar haber hecho algo)
  I - Information Disclosure (Fuga de informacion)
  D - Denial of Service (Denegacion de servicio)
  E - Elevation of Privilege (Escalada de privilegios)

  Para cada componente del sistema, preguntate:
  "Es vulnerable a alguna de las 6 amenazas STRIDE?"
```

## 7.3 Ataques Clasicos Explicados

### Buffer Overflow (desbordamiento de buffer)

```
El atacante envia mas datos de los que caben en un buffer,
sobreescribiendo datos adyacentes en memoria (como la direccion
de retorno de una funcion).

Memoria antes del ataque:
  [buffer: 8 bytes][saved_ebp][return_address][...]
  [AAAAAAA\0      ][          ][0x08048456    ]

Memoria despues del overflow:
  [AAAAAAAAAAAAAAAA][AAAA     ][0xDEADBEEF    ]
                                 ^ direccion del codigo del atacante

  El programa "retorna" a la direccion del atacante
  y ejecuta su codigo con los permisos del proceso.

Defensa:
  - Stack canaries (valores centinela que detectan overflow)
  - ASLR (Address Space Layout Randomization)
  - DEP/NX (No-Execute bit en paginas de datos)
  - Usar lenguajes memory-safe (Python, Rust, Go)
```

### SQL Injection

```
El atacante inyecta codigo SQL a traves de input no sanitizado.

Codigo vulnerable (Python):
  query = f"SELECT * FROM users WHERE name = '{user_input}'"

Input normal:  "luis"
  -> SELECT * FROM users WHERE name = 'luis'  (OK)

Input malicioso: "' OR '1'='1"
  -> SELECT * FROM users WHERE name = '' OR '1'='1'
  -> Retorna TODOS los usuarios (bypass de autenticacion)

Input destructivo: "'; DROP TABLE users; --"
  -> SELECT * FROM users WHERE name = ''; DROP TABLE users; --'
  -> BORRA toda la tabla de usuarios

Defensa: Consultas parametrizadas (prepared statements)
  cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
```

### Escalada de Privilegios

```
El atacante obtiene permisos mayores a los que tiene.

Horizontal: acceder a recursos de OTRO usuario del mismo nivel
  Ej: usuario A lee archivos de usuario B

Vertical: obtener permisos de un nivel SUPERIOR
  Ej: usuario normal obtiene acceso root

Metodos comunes en Linux:
  - Explotar binarios SUID con vulnerabilidades
  - Explotar configuraciones incorrectas de sudo
  - Kernel exploits (vulnerabilidades del kernel)
  - Acceso a credenciales almacenadas (scripts, historiales)
  - Cron jobs ejecutandose como root con permisos laxos
```

## 7.4 Practica: Validacion y Deteccion de Amenazas

### Ejercicio 1: Input Validation en Python

```python
#!/usr/bin/env python3
"""
Demuestra la importancia de la validacion de entrada
y como prevenir ataques comunes.
"""
import re
import html
import shlex
import subprocess


def banner(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


# --- SQL INJECTION ---

def demo_sql_injection():
    banner("SQL INJECTION: VULNERABLE vs SEGURO")

    # Simulamos la consulta (sin BD real)
    def query_vulnerable(user_input: str) -> str:
        """VULNERABLE: concatenacion directa de strings."""
        return f"SELECT * FROM users WHERE name = '{user_input}'"

    def query_segura(user_input: str) -> str:
        """SEGURA: consulta parametrizada (simulada)."""
        # En codigo real: cursor.execute("SELECT ... WHERE name = %s", (input,))
        safe_input = user_input.replace("'", "''")  # Escape basico
        return f"SELECT * FROM users WHERE name = '{safe_input}'"
        # NOTA: en produccion SIEMPRE usar prepared statements, no escape manual

    inputs_prueba = [
        "luis",                           # Normal
        "' OR '1'='1",                    # Bypass autenticacion
        "'; DROP TABLE users; --",        # Eliminar tabla
        "' UNION SELECT password FROM admin; --",  # Extraer datos
    ]

    for inp in inputs_prueba:
        print(f"\n  Input: {inp!r}")
        print(f"  Vulnerable: {query_vulnerable(inp)}")
        print(f"  Segura:     {query_segura(inp)}")


# --- COMMAND INJECTION ---

def demo_command_injection():
    banner("COMMAND INJECTION: VULNERABLE vs SEGURO")

    def ping_vulnerable(host: str) -> str:
        """VULNERABLE: input directo en shell command."""
        # NUNCA hacer esto:
        # os.system(f"ping -c 1 {host}")
        return f"os.system('ping -c 1 {host}')"

    def ping_seguro(host: str) -> str:
        """SEGURO: validar input y usar subprocess con lista."""
        # Validar que es un hostname/IP valido
        if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
            return f"RECHAZADO: '{host}' contiene caracteres no permitidos"
        # subprocess con lista (no shell=True)
        return f"subprocess.run(['ping', '-c', '1', '{host}'])"

    inputs_prueba = [
        "google.com",                     # Normal
        "8.8.8.8",                        # Normal
        "google.com; cat /etc/passwd",    # Inyeccion de comando
        "$(whoami)",                       # Sustitucion de comando
        "google.com && rm -rf /",         # Encadenamiento destructivo
    ]

    for inp in inputs_prueba:
        print(f"\n  Input: {inp!r}")
        print(f"  Vulnerable: {ping_vulnerable(inp)}")
        print(f"  Seguro:     {ping_seguro(inp)}")


# --- XSS (Cross-Site Scripting) ---

def demo_xss():
    banner("XSS: VULNERABLE vs SEGURO")

    def render_vulnerable(user_input: str) -> str:
        """VULNERABLE: input directo en HTML."""
        return f"<p>Hola, {user_input}</p>"

    def render_seguro(user_input: str) -> str:
        """SEGURO: escapar HTML."""
        safe_input = html.escape(user_input)
        return f"<p>Hola, {safe_input}</p>"

    inputs_prueba = [
        "Luis",                                         # Normal
        "<script>alert('hackeado')</script>",            # XSS basico
        "<img src=x onerror='document.location=\"http://evil.com\"'>",  # XSS
        "Luis<br><h1>SOY ADMIN</h1>",                   # HTML injection
    ]

    for inp in inputs_prueba:
        print(f"\n  Input: {inp!r}")
        print(f"  Vulnerable: {render_vulnerable(inp)}")
        print(f"  Seguro:     {render_seguro(inp)}")


# --- PATH TRAVERSAL ---

def demo_path_traversal():
    banner("PATH TRAVERSAL: VULNERABLE vs SEGURO")

    import os

    BASE_DIR = "/var/www/uploads"

    def leer_vulnerable(filename: str) -> str:
        """VULNERABLE: path directo."""
        path = f"{BASE_DIR}/{filename}"
        return f"open('{path}')"

    def leer_seguro(filename: str) -> str:
        """SEGURO: validar que el path no escape del directorio."""
        # Resolver el path completo
        path = os.path.realpath(os.path.join(BASE_DIR, filename))
        # Verificar que esta dentro del directorio permitido
        if not path.startswith(BASE_DIR):
            return f"RECHAZADO: '{filename}' intenta salir del directorio"
        return f"open('{path}')"

    inputs_prueba = [
        "foto.jpg",                        # Normal
        "../../../etc/passwd",             # Path traversal
        "../../etc/shadow",                # Path traversal
        "subdir/archivo.txt",              # Normal, subdirectorio
    ]

    for inp in inputs_prueba:
        print(f"\n  Input: {inp!r}")
        print(f"  Vulnerable: {leer_vulnerable(inp)}")
        print(f"  Seguro:     {leer_seguro(inp)}")


# --- VALIDADOR COMPLETO ---

def demo_validador_completo():
    banner("VALIDADOR DE INPUT COMPLETO")

    class InputValidator:
        """Validador reutilizable para diferentes tipos de input."""

        @staticmethod
        def username(value: str) -> tuple[bool, str]:
            """Valida nombre de usuario."""
            if not value:
                return False, "Vacio"
            if len(value) < 3 or len(value) > 30:
                return False, "Largo debe ser 3-30 caracteres"
            if not re.match(r'^[a-zA-Z0-9_]+$', value):
                return False, "Solo alfanumerico y guion bajo"
            return True, "Valido"

        @staticmethod
        def email(value: str) -> tuple[bool, str]:
            """Valida email basico."""
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                return False, "Formato de email invalido"
            return True, "Valido"

        @staticmethod
        def ip_address(value: str) -> tuple[bool, str]:
            """Valida direccion IPv4."""
            parts = value.split(".")
            if len(parts) != 4:
                return False, "Debe tener 4 octetos"
            for part in parts:
                try:
                    num = int(part)
                    if num < 0 or num > 255:
                        return False, f"Octeto {part} fuera de rango"
                except ValueError:
                    return False, f"'{part}' no es un numero"
            return True, "Valido"

        @staticmethod
        def path(value: str, base_dir: str = "/var/www") -> tuple[bool, str]:
            """Valida que un path no escape del directorio base."""
            import os
            full_path = os.path.realpath(os.path.join(base_dir, value))
            if not full_path.startswith(os.path.realpath(base_dir)):
                return False, "Path traversal detectado"
            return True, "Valido"

    v = InputValidator()

    print("\n  --- Validacion de Usernames ---")
    for name in ["luis", "a", "admin' OR '1'='1", "user_123", "a" * 50]:
        ok, msg = v.username(name)
        print(f"  {'[OK]' if ok else '[NO]'} '{name}': {msg}")

    print("\n  --- Validacion de Emails ---")
    for email in ["luis@mail.com", "no-arroba", "x@x", "test@domain.co"]:
        ok, msg = v.email(email)
        print(f"  {'[OK]' if ok else '[NO]'} '{email}': {msg}")

    print("\n  --- Validacion de IPs ---")
    for ip in ["192.168.1.1", "999.1.1.1", "abc.1.1.1", "8.8.8.8"]:
        ok, msg = v.ip_address(ip)
        print(f"  {'[OK]' if ok else '[NO]'} '{ip}': {msg}")

    print("\n  --- Validacion de Paths ---")
    for path in ["uploads/foto.jpg", "../../../etc/passwd", "normal/file.txt"]:
        ok, msg = v.path(path)
        print(f"  {'[OK]' if ok else '[NO]'} '{path}': {msg}")


if __name__ == "__main__":
    demo_sql_injection()
    demo_command_injection()
    demo_xss()
    demo_path_traversal()
    demo_validador_completo()

    print(f"\n{'=' * 60}")
    print("  REGLAS DE ORO DE VALIDACION:")
    print("  1. NUNCA confiar en input externo")
    print("  2. Validar tipo, formato, rango y longitud")
    print("  3. Usar consultas parametrizadas (SQL)")
    print("  4. Escapar output (HTML, shell)")
    print("  5. Aplicar principio de menor privilegio")
    print(f"{'=' * 60}")
```

Guarda como `validacion_amenazas.py` y ejecuta:

```bash
python3 validacion_amenazas.py
```

### Ejercicio 2: Auditoria del sistema en Linux

```bash
# Buscar archivos SUID (posibles vectores de escalada)
echo "=== Archivos SUID ==="
find / -perm -4000 -type f 2>/dev/null | head -20

# Buscar archivos con permisos de escritura mundial
echo "=== Archivos world-writable en /etc ==="
find /etc -perm -o+w -type f 2>/dev/null

# Buscar cron jobs de root
echo "=== Cron jobs de root ==="
sudo crontab -l 2>/dev/null
ls -la /etc/cron.d/ 2>/dev/null

# Verificar intentos de login fallidos
echo "=== Ultimos intentos fallidos ==="
sudo grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10

# Verificar conexiones de red activas
echo "=== Conexiones activas ==="
ss -tulnp | grep LISTEN

# Buscar procesos sospechosos
echo "=== Procesos con mas CPU ==="
ps aux --sort=-%cpu | head -10
```

### Ejercicio 3: Script de deteccion de amenazas

```python
#!/usr/bin/env python3
"""
Script basico de deteccion de amenazas en el sistema.
Revisa indicadores comunes de compromiso.
"""
import os
import subprocess
import pwd


def ejecutar(cmd: str) -> str:
    """Ejecuta un comando y retorna la salida."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, Exception) as e:
        return f"Error: {e}"


def banner(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def verificar_usuarios_root():
    """Busca usuarios con UID 0 (permisos de root)."""
    banner("USUARIOS CON UID 0 (ROOT)")
    usuarios_root = []
    with open("/etc/passwd") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) >= 3 and parts[2] == "0":
                usuarios_root.append(parts[0])

    if len(usuarios_root) == 1 and usuarios_root[0] == "root":
        print("  [OK] Solo 'root' tiene UID 0")
    else:
        print(f"  [ALERTA] Usuarios con UID 0: {usuarios_root}")
        print("  -> Solo 'root' deberia tener UID 0")


def verificar_archivos_suid():
    """Busca archivos SUID en ubicaciones inusuales."""
    banner("ARCHIVOS SUID EN UBICACIONES INUSUALES")

    # Ubicaciones normales para SUID
    dirs_normales = {"/usr/bin", "/usr/sbin", "/usr/lib", "/usr/libexec",
                     "/bin", "/sbin"}

    output = ejecutar("find / -perm -4000 -type f 2>/dev/null")
    sospechosos = []

    for path in output.split("\n"):
        if not path:
            continue
        directorio = os.path.dirname(path)
        if directorio not in dirs_normales:
            sospechosos.append(path)

    if not sospechosos:
        print("  [OK] No se encontraron SUID en ubicaciones inusuales")
    else:
        print(f"  [ALERTA] SUID sospechosos encontrados:")
        for s in sospechosos[:10]:
            print(f"    - {s}")


def verificar_puertos_abiertos():
    """Lista puertos en escucha."""
    banner("PUERTOS EN ESCUCHA")

    output = ejecutar("ss -tulnp 2>/dev/null | grep LISTEN")
    if not output:
        print("  No se pudieron obtener puertos (ejecutar como root)")
        return

    lineas = output.split("\n")
    print(f"  {len(lineas)} puertos en escucha:")
    for line in lineas:
        parts = line.split()
        if len(parts) >= 5:
            proto = parts[0]
            addr = parts[4]
            proceso = parts[-1] if "users:" in line else "desconocido"
            print(f"    {proto} {addr} ({proceso})")


def verificar_archivos_recientes():
    """Busca archivos modificados recientemente en directorios criticos."""
    banner("ARCHIVOS MODIFICADOS EN ULTIMAS 24H (/etc)")

    output = ejecutar("find /etc -mtime -1 -type f 2>/dev/null")
    if not output:
        print("  [OK] No se modificaron archivos en /etc en 24h")
    else:
        archivos = output.split("\n")
        print(f"  [INFO] {len(archivos)} archivos modificados:")
        for a in archivos[:10]:
            print(f"    - {a}")


def verificar_cron_sospechosos():
    """Busca cron jobs potencialmente sospechosos."""
    banner("CRON JOBS DEL SISTEMA")

    cron_dirs = ["/etc/cron.d", "/etc/cron.daily",
                 "/etc/cron.hourly", "/etc/cron.weekly"]

    for d in cron_dirs:
        if os.path.isdir(d):
            archivos = os.listdir(d)
            print(f"  {d}: {len(archivos)} jobs")
            for a in archivos:
                filepath = os.path.join(d, a)
                st = os.stat(filepath)
                owner = pwd.getpwuid(st.st_uid).pw_name
                print(f"    - {a} (owner: {owner})")


def verificar_shells_usuarios():
    """Verifica que usuarios tienen shell de login."""
    banner("USUARIOS CON SHELL DE LOGIN")

    shells_login = []
    with open("/etc/passwd") as f:
        for line in f:
            parts = line.strip().split(":")
            shell = parts[-1]
            if shell not in ("/usr/sbin/nologin", "/bin/false", "/sbin/nologin"):
                nombre = parts[0]
                uid = int(parts[2])
                shells_login.append((nombre, uid, shell))

    print(f"  {len(shells_login)} usuarios con shell de login:")
    for nombre, uid, shell in shells_login:
        alerta = " [REVISAR]" if uid == 0 and nombre != "root" else ""
        print(f"    {nombre} (UID:{uid}) -> {shell}{alerta}")


def main():
    print("=" * 60)
    print("  SCRIPT DE DETECCION BASICA DE AMENAZAS")
    print("  (Ejecutar como root para resultados completos)")
    print("=" * 60)

    verificar_usuarios_root()
    verificar_archivos_suid()
    verificar_puertos_abiertos()
    verificar_archivos_recientes()
    verificar_cron_sospechosos()
    verificar_shells_usuarios()

    banner("RECOMENDACIONES")
    print("  1. Ejecutar este script periodicamente")
    print("  2. Comparar resultados con una baseline conocida")
    print("  3. Investigar cualquier cambio inesperado")
    print("  4. Mantener el sistema actualizado")
    print("  5. Revisar logs de autenticacion regularmente")


if __name__ == "__main__":
    main()
```

Guarda como `deteccion_amenazas.py` y ejecuta:

```bash
# Como usuario normal (algunos checks limitados)
python3 deteccion_amenazas.py

# Como root (resultados completos)
sudo python3 deteccion_amenazas.py
```

## 7.5 Resumen del Modulo

```
VALIDACION:
  - Todo input externo es sospechoso
  - Validar tipo, formato, rango, longitud
  - Consultas parametrizadas (SQL), escapar output (HTML)
  - Principio: defense in depth (multiples capas)

AMENAZAS:
  Interrupcion:  Destruir/inhabilitar recursos (DoS)
  Intercepcion:  Acceso no autorizado (sniffing, keylogger)
  Modificacion:  Alterar datos (MITM, rootkit)
  Fabricacion:   Crear objetos falsos (spoofing, phishing)

ATAQUES CLASICOS:
  Buffer Overflow:      Sobreescribir memoria (defensa: ASLR, NX, lenguajes seguros)
  SQL Injection:        Inyectar SQL (defensa: prepared statements)
  XSS:                  Inyectar JS en web (defensa: html.escape())
  Command Injection:    Inyectar comandos SO (defensa: subprocess con lista)
  Path Traversal:       Escapar directorio (defensa: validar path canonico)
  Escalada Privilegios: Obtener permisos mayores (defensa: menor privilegio, auditar SUID)

MODELO STRIDE: Spoofing, Tampering, Repudiation,
               Info Disclosure, DoS, Elevation of Privilege
```

## 7.6 Preguntas de Repaso

1. Que es SQL Injection? Muestra un ejemplo vulnerable y su correccion.
2. Explica la diferencia entre escalada horizontal y vertical de privilegios.
3. Que es STRIDE y como se usa para analizar amenazas?
4. Por que es peligroso usar `shell=True` en subprocess?
5. Que es un rootkit y por que es dificil de detectar?
