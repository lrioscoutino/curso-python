# Modulo 8: Cifrado (Tema 6.7)

## 8.1 Teoria: Fundamentos del Cifrado

```
CIFRADO = Transformar datos legibles (texto plano) en datos ilegibles
          (texto cifrado) usando un algoritmo y una clave.

  Texto Plano + Clave + Algoritmo = Texto Cifrado
  "Hola mundo" + clave123 + AES = "x7$kL9m..."

  Texto Cifrado + Clave + Algoritmo = Texto Plano
  "x7$kL9m..." + clave123 + AES = "Hola mundo"

Objetivo: que solo quien tiene la clave pueda leer la informacion.
```

### Tipos de Cifrado

```
┌──────────────────────┬──────────────────────┬──────────────────────┐
│                      │ SIMETRICO            │ ASIMETRICO           │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Claves               │ UNA clave            │ DOS claves           │
│                      │ (misma para cifrar   │ (publica + privada)  │
│                      │ y descifrar)         │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Velocidad            │ RAPIDO               │ LENTO                │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Uso tipico           │ Cifrar datos grandes │ Intercambio de       │
│                      │ (disco, archivos)    │ claves, firmas       │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Problema             │ Como compartir la    │ Computacionalmente   │
│                      │ clave de forma       │ costoso para datos   │
│                      │ segura?              │ grandes              │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Algoritmos           │ AES, ChaCha20,       │ RSA, ECC, Ed25519    │
│                      │ 3DES, Blowfish       │                      │
├──────────────────────┼──────────────────────┼──────────────────────┤
│ Analogia             │ Una cerradura con    │ Buzon de correo:     │
│                      │ una sola llave.      │ todos meten cartas   │
│                      │ Ambas partes la      │ (clave publica) pero │
│                      │ necesitan            │ solo tu abres (priv) │
└──────────────────────┴──────────────────────┴──────────────────────┘
```

### Cifrado Simetrico en Detalle

```
  Emisor                                      Receptor
    │                                             │
    │  Texto: "Hola"                              │
    │  Clave: "secreto123"                        │
    │         │                                   │
    │    ┌────▼────┐                              │
    │    │ CIFRAR  │  AES-256                     │
    │    │ (AES)   │                              │
    │    └────┬────┘                              │
    │         │                                   │
    │  Cifrado: "x7$kL9m..."  ──────────────>     │
    │                                     ┌───────▼──────┐
    │                                     │ DESCIFRAR    │
    │                                     │ (AES)        │
    │                                     │ Clave:       │
    │                                     │ "secreto123" │
    │                                     └───────┬──────┘
    │                                             │
    │                                     Texto: "Hola"

  PROBLEMA: Ambos necesitan la misma clave.
  Como se la pasas al receptor de forma segura?
  -> Solucion: usar cifrado asimetrico para intercambiar la clave simetrica
```

### Cifrado Asimetrico en Detalle

```
  1. Receptor genera par de claves:
     - Clave PUBLICA  (la comparte con todos)
     - Clave PRIVADA  (solo la tiene el)

  2. Emisor cifra con la clave PUBLICA del receptor:

  Emisor                                      Receptor
    │                                             │
    │  Texto: "Hola"                              │
    │  Clave PUBLICA del receptor                 │
    │         │                                   │
    │    ┌────▼────┐                              │
    │    │ CIFRAR  │  RSA                         │
    │    │ (pub)   │                              │
    │    └────┬────┘                              │
    │         │                                   │
    │  Cifrado: "a8F#2q..."  ──────────────>      │
    │                                     ┌───────▼──────┐
    │                                     │ DESCIFRAR    │
    │                                     │ Clave        │
    │                                     │ PRIVADA      │
    │                                     └───────┬──────┘
    │                                             │
    │                                     Texto: "Hola"

  Solo la clave PRIVADA puede descifrar lo cifrado con la PUBLICA.
  Aunque intercepten el mensaje, sin la clave privada no lo leen.
```

### Funciones Hash (No son cifrado, pero son esenciales)

```
Hash = Funcion unidireccional que genera una "huella digital" de datos.

Propiedades:
  1. Determinista: mismo input -> mismo hash siempre
  2. Unidireccional: del hash NO se puede obtener el input
  3. Efecto avalancha: un bit de cambio = hash completamente diferente
  4. Resistente a colisiones: dificil encontrar dos inputs con mismo hash

  "Hola"     -> SHA-256 -> "3c96d9e..."  (siempre el mismo)
  "Holb"     -> SHA-256 -> "a82f1c7..."  (completamente diferente)
  "Hola" * 1000 -> SHA-256 -> "9f2e..."  (siempre 256 bits)

Algoritmos:
  MD5:      128 bits (INSEGURO, obsoleto, NO usar para seguridad)
  SHA-1:    160 bits (INSEGURO, obsoleto)
  SHA-256:  256 bits (seguro, estandar actual)
  SHA-512:  512 bits (seguro, mas largo)
  bcrypt:   Para passwords (incluye salt y es lento a proposito)
  argon2:   Para passwords (ganador de PHC, recomendado actual)

Usos:
  - Almacenar passwords (hash + salt, nunca texto plano)
  - Verificar integridad de archivos (checksums)
  - Firmas digitales (hash del documento + cifrado asimetrico)
```

### Firma Digital

```
Prueba que un mensaje fue creado por quien dice ser y no fue alterado.

  Emisor (firma):
    1. Calcula hash del mensaje: hash("Hola") = "3c96..."
    2. Cifra el hash con su clave PRIVADA: cifrar("3c96...", priv) = firma
    3. Envia: mensaje + firma

  Receptor (verifica):
    1. Calcula hash del mensaje: hash("Hola") = "3c96..."
    2. Descifra la firma con clave PUBLICA del emisor: descifrar(firma, pub) = "3c96..."
    3. Compara: si ambos hashes coinciden -> firma VALIDA

  Si alguien modifica el mensaje, los hashes NO coincidiran.
  Si alguien intenta falsificar la firma, no tiene la clave privada.
```

## 8.2 Cifrado en Sistemas Operativos

### Cifrado de Disco Completo

```
Protege datos si el dispositivo es robado o accedido fisicamente.

Linux (LUKS/dm-crypt):
  - Cifra la particion completa
  - Pide password al arrancar (antes de cargar el SO)
  - Sin la password, el disco es datos aleatorios

Windows (BitLocker):
  - Cifra el volumen completo
  - Usa TPM (chip de seguridad) + PIN

macOS (FileVault):
  - Cifra el disco con XTS-AES-128
  - Integrado con cuenta de usuario
```

### Cifrado de Comunicaciones

```
TLS/SSL (HTTPS):
  1. Cliente conecta al servidor
  2. Servidor envia certificado (contiene clave publica)
  3. Cliente verifica certificado con CA (Certificate Authority)
  4. Intercambian clave simetrica (via asimetrico)
  5. Toda la comunicacion usa la clave simetrica (rapido)

SSH:
  1. Cliente y servidor negocian algoritmos
  2. Intercambio de claves (Diffie-Hellman)
  3. Autenticacion (password o clave publica)
  4. Canal cifrado establecido

VPN:
  Tunel cifrado entre dos puntos de red.
  Todo el trafico dentro del tunel esta cifrado.
```

## 8.3 Practica: Cifrado con Python

### Ejercicio 1: Funciones Hash

```python
#!/usr/bin/env python3
"""
Demuestra funciones hash y su uso en seguridad.
"""
import hashlib
import hmac
import os


def banner(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def demo_hashes():
    """Demuestra diferentes funciones hash."""
    banner("FUNCIONES HASH")

    texto = "Hola mundo"
    texto_bytes = texto.encode('utf-8')

    algoritmos = ['md5', 'sha1', 'sha256', 'sha512']

    print(f"  Texto original: '{texto}'\n")

    for algo in algoritmos:
        h = hashlib.new(algo, texto_bytes)
        seguro = "INSEGURO" if algo in ('md5', 'sha1') else "SEGURO"
        print(f"  {algo.upper():10} ({seguro}):")
        print(f"    {h.hexdigest()}")
        print(f"    Bits: {h.digest_size * 8}")
        print()


def demo_efecto_avalancha():
    """Un bit de cambio = hash completamente diferente."""
    banner("EFECTO AVALANCHA")

    textos = ["Hola", "Holb", "hola", "Hola "]

    print("  SHA-256 de textos similares:\n")
    for t in textos:
        h = hashlib.sha256(t.encode()).hexdigest()
        print(f"  '{t}' -> {h[:32]}...")
    print("\n  Nota: un solo caracter de diferencia = hash totalmente distinto")


def demo_password_hash():
    """Demuestra hash de passwords con salt."""
    banner("HASH DE PASSWORDS (CON SALT)")

    password = "mi_password_123"

    # SIN salt (inseguro): mismo password = mismo hash
    hash_sin_salt = hashlib.sha256(password.encode()).hexdigest()
    print(f"  Password: '{password}'")
    print(f"  Sin salt: {hash_sin_salt}")
    print(f"  Problema: si dos usuarios usan el mismo password,")
    print(f"            tendran el mismo hash -> atacante lo detecta")

    # CON salt (seguro): cada hash es unico
    print(f"\n  Con salt (cada hash es unico):")
    for i in range(3):
        salt = os.urandom(16)
        hash_con_salt = hashlib.pbkdf2_hmac(
            'sha256', password.encode(), salt, iterations=100000
        )
        print(f"    Salt {i+1}: {salt.hex()[:16]}...")
        print(f"    Hash {i+1}: {hash_con_salt.hex()[:32]}...")
        print()

    print("  Mismo password, diferente salt = diferente hash")
    print("  El salt se almacena junto al hash (no es secreto)")


def demo_verificacion_integridad():
    """Verificar que un archivo no fue modificado."""
    banner("VERIFICACION DE INTEGRIDAD (CHECKSUM)")

    # Simular un archivo
    contenido_original = "Este es el contenido original del archivo"
    contenido_modificado = "Este es el contenido modificado del archivo"

    hash_original = hashlib.sha256(contenido_original.encode()).hexdigest()
    hash_modificado = hashlib.sha256(contenido_modificado.encode()).hexdigest()

    print(f"  Contenido original:")
    print(f"    '{contenido_original}'")
    print(f"    SHA-256: {hash_original[:32]}...")

    print(f"\n  Contenido modificado:")
    print(f"    '{contenido_modificado}'")
    print(f"    SHA-256: {hash_modificado[:32]}...")

    print(f"\n  Coinciden? {'SI' if hash_original == hash_modificado else 'NO'}")
    print(f"  -> Si el hash cambia, el archivo fue modificado")


def demo_hmac():
    """HMAC: Hash con clave para autenticar mensajes."""
    banner("HMAC (Hash-based Message Authentication Code)")

    clave = b"clave_secreta_compartida"
    mensaje = b"Transferir $1000 a cuenta 12345"

    # Crear HMAC
    mac = hmac.new(clave, mensaje, hashlib.sha256).hexdigest()
    print(f"  Mensaje: '{mensaje.decode()}'")
    print(f"  HMAC:    {mac[:32]}...")

    # Verificar (receptor con la misma clave)
    mac_verificacion = hmac.new(clave, mensaje, hashlib.sha256).hexdigest()
    print(f"\n  Verificacion: {'VALIDO' if hmac.compare_digest(mac, mac_verificacion) else 'INVALIDO'}")

    # Si alguien modifica el mensaje
    mensaje_alterado = b"Transferir $9999 a cuenta 12345"
    mac_alterado = hmac.new(clave, mensaje_alterado, hashlib.sha256).hexdigest()
    print(f"\n  Mensaje alterado: '{mensaje_alterado.decode()}'")
    print(f"  HMAC alterado:    {mac_alterado[:32]}...")
    print(f"  Coincide con original? {'SI' if hmac.compare_digest(mac, mac_alterado) else 'NO'}")
    print(f"  -> La alteracion se detecta porque el HMAC cambia")


if __name__ == "__main__":
    demo_hashes()
    demo_efecto_avalancha()
    demo_password_hash()
    demo_verificacion_integridad()
    demo_hmac()
```

Guarda como `hashing_demo.py` y ejecuta:

```bash
python3 hashing_demo.py
```

### Ejercicio 2: Cifrado Simetrico y Asimetrico

```python
#!/usr/bin/env python3
"""
Demuestra cifrado simetrico (AES) y asimetrico (RSA) con Python.
Requiere: pip install cryptography
"""

# Verificar que cryptography esta instalado
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import os
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("=" * 60)
    print("  INSTALAR: pip install cryptography")
    print("=" * 60)


def banner(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")


def demo_cifrado_simetrico_fernet():
    """Cifrado simetrico usando Fernet (AES-128-CBC + HMAC)."""
    banner("CIFRADO SIMETRICO: FERNET (AES)")

    # Generar clave
    clave = Fernet.generate_key()
    f = Fernet(clave)

    print(f"  Clave: {clave.decode()[:30]}...")

    # Cifrar
    texto_plano = b"Informacion confidencial: password=admin123"
    texto_cifrado = f.encrypt(texto_plano)

    print(f"\n  Texto plano:   '{texto_plano.decode()}'")
    print(f"  Texto cifrado: '{texto_cifrado.decode()[:50]}...'")

    # Descifrar
    texto_descifrado = f.decrypt(texto_cifrado)
    print(f"  Descifrado:    '{texto_descifrado.decode()}'")
    print(f"  Coincide?      {texto_plano == texto_descifrado}")

    # Intentar descifrar con clave incorrecta
    clave_incorrecta = Fernet.generate_key()
    f_incorrecta = Fernet(clave_incorrecta)
    try:
        f_incorrecta.decrypt(texto_cifrado)
        print("  Clave incorrecta: DESCIFRADO (esto no deberia pasar!)")
    except Exception:
        print("\n  [OK] Clave incorrecta: no se puede descifrar")


def demo_cifrado_aes_raw():
    """Cifrado AES-256 directo (modo CTR)."""
    banner("CIFRADO SIMETRICO: AES-256-CTR (bajo nivel)")

    # Generar clave de 256 bits y nonce
    clave = os.urandom(32)     # 256 bits
    nonce = os.urandom(16)     # 128 bits

    print(f"  Clave (256 bits): {clave.hex()[:32]}...")
    print(f"  Nonce (128 bits): {nonce.hex()}")

    # Cifrar
    texto_plano = b"Datos sensibles que necesitan proteccion"
    cipher = Cipher(algorithms.AES(clave), modes.CTR(nonce))
    encryptor = cipher.encryptor()
    texto_cifrado = encryptor.update(texto_plano) + encryptor.finalize()

    print(f"\n  Texto plano:   '{texto_plano.decode()}'")
    print(f"  Cifrado (hex): {texto_cifrado.hex()[:40]}...")

    # Descifrar
    cipher = Cipher(algorithms.AES(clave), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    texto_descifrado = decryptor.update(texto_cifrado) + decryptor.finalize()

    print(f"  Descifrado:    '{texto_descifrado.decode()}'")


def demo_cifrado_asimetrico():
    """Cifrado asimetrico con RSA."""
    banner("CIFRADO ASIMETRICO: RSA")

    # Generar par de claves
    print("  Generando par de claves RSA-2048...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Serializar claves para mostrar
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print(f"  Clave publica (primeros 80 chars):")
    print(f"    {pub_bytes.decode()[:80]}...")

    # Cifrar con clave publica
    texto_plano = b"Mensaje secreto para el receptor"
    texto_cifrado = public_key.encrypt(
        texto_plano,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print(f"\n  Texto plano:   '{texto_plano.decode()}'")
    print(f"  Cifrado (hex): {texto_cifrado.hex()[:40]}...")
    print(f"  Tamano cifrado: {len(texto_cifrado)} bytes")

    # Descifrar con clave privada
    texto_descifrado = private_key.decrypt(
        texto_cifrado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"  Descifrado:    '{texto_descifrado.decode()}'")

    # Nota sobre el tamano
    print(f"\n  NOTA: RSA solo puede cifrar datos pequenos")
    print(f"  (< tamano_clave - overhead del padding)")
    print(f"  Para datos grandes: cifrar con AES, cifrar clave AES con RSA")


def demo_firma_digital():
    """Firma digital con RSA."""
    banner("FIRMA DIGITAL: RSA + SHA-256")

    # Generar claves
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Firmar un mensaje
    mensaje = b"Autorizo transferencia de $5000 a cuenta 12345"

    firma = private_key.sign(
        mensaje,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print(f"  Mensaje: '{mensaje.decode()}'")
    print(f"  Firma:   {firma.hex()[:40]}...")

    # Verificar firma (receptor usa clave publica)
    try:
        public_key.verify(
            firma,
            mensaje,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"  Verificacion: FIRMA VALIDA")
    except Exception:
        print(f"  Verificacion: FIRMA INVALIDA")

    # Intentar verificar con mensaje alterado
    mensaje_alterado = b"Autorizo transferencia de $9999 a cuenta 99999"
    try:
        public_key.verify(
            firma,
            mensaje_alterado,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"  Mensaje alterado: FIRMA VALIDA (esto no deberia pasar!)")
    except Exception:
        print(f"  Mensaje alterado: FIRMA INVALIDA (alteracion detectada)")


def demo_cifrado_hibrido():
    """Cifrado hibrido: RSA + AES (como funciona TLS)."""
    banner("CIFRADO HIBRIDO: RSA + AES (como TLS)")

    print("  Paso 1: Receptor genera par de claves RSA")
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )
    public_key = private_key.public_key()

    print("  Paso 2: Emisor genera clave AES aleatoria")
    clave_aes = os.urandom(32)  # 256 bits
    print(f"    Clave AES: {clave_aes.hex()[:16]}...")

    print("  Paso 3: Emisor cifra la clave AES con RSA (clave publica)")
    clave_aes_cifrada = public_key.encrypt(
        clave_aes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("  Paso 4: Emisor cifra el mensaje con AES")
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(clave_aes), modes.CTR(nonce))
    encryptor = cipher.encryptor()

    mensaje = b"Este mensaje largo se cifra con AES (rapido) " * 10
    mensaje_cifrado = encryptor.update(mensaje) + encryptor.finalize()

    print(f"    Mensaje original: {len(mensaje)} bytes")
    print(f"    Mensaje cifrado:  {len(mensaje_cifrado)} bytes")

    print("  Paso 5: Emisor envia: clave_AES_cifrada + nonce + mensaje_cifrado")

    print("\n  --- Receptor ---")
    print("  Paso 6: Receptor descifra clave AES con su clave privada RSA")
    clave_aes_descifrada = private_key.decrypt(
        clave_aes_cifrada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"    Clave AES recuperada: {clave_aes_descifrada.hex()[:16]}...")
    print(f"    Coincide? {clave_aes == clave_aes_descifrada}")

    print("  Paso 7: Receptor descifra mensaje con AES")
    cipher = Cipher(algorithms.AES(clave_aes_descifrada), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    mensaje_descifrado = decryptor.update(mensaje_cifrado) + decryptor.finalize()
    print(f"    Mensaje descifrado: {len(mensaje_descifrado)} bytes")
    print(f"    Coincide? {mensaje == mensaje_descifrado}")

    print("\n  RESUMEN:")
    print("    RSA (lento) -> solo para la clave AES (32 bytes)")
    print("    AES (rapido) -> para el mensaje completo (cualquier tamano)")
    print("    Asi funciona HTTPS/TLS en la vida real")


if __name__ == "__main__":
    if not CRYPTO_AVAILABLE:
        print("\nInstalar dependencia: pip install cryptography")
    else:
        demo_cifrado_simetrico_fernet()
        demo_cifrado_aes_raw()
        demo_cifrado_asimetrico()
        demo_firma_digital()
        demo_cifrado_hibrido()

        banner("RESUMEN DE ALGORITMOS")
        print("  Simetrico:  AES-256 (estandar), ChaCha20 (alternativa)")
        print("  Asimetrico: RSA-2048+ (clasico), Ed25519 (moderno)")
        print("  Hash:       SHA-256 (general), bcrypt/argon2 (passwords)")
        print("  En practica: cifrado HIBRIDO (RSA + AES)")
```

Guarda como `cifrado_demo.py` y ejecuta:

```bash
# Instalar dependencia
pip install cryptography

# Ejecutar
python3 cifrado_demo.py
```

### Ejercicio 3: Cifrado en Linux (comandos)

```bash
# --- CIFRADO DE ARCHIVOS CON GPG ---

# Cifrado simetrico de archivo
echo "datos secretos" > /tmp/secreto.txt
gpg --symmetric --cipher-algo AES256 /tmp/secreto.txt
# Pide password, genera secreto.txt.gpg

# Descifrar
gpg --decrypt /tmp/secreto.txt.gpg

# --- CIFRADO CON OPENSSL ---

# Cifrar archivo con AES-256
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -in /tmp/secreto.txt -out /tmp/secreto.enc

# Descifrar
openssl enc -aes-256-cbc -d -pbkdf2 \
  -in /tmp/secreto.enc -out /tmp/secreto_descifrado.txt

# --- GENERAR PAR DE CLAVES RSA ---

# Generar clave privada
openssl genrsa -out /tmp/privada.pem 2048

# Extraer clave publica
openssl rsa -in /tmp/privada.pem -pubout -out /tmp/publica.pem

# Ver claves
echo "=== Clave Publica ==="
cat /tmp/publica.pem

# --- HASH DE ARCHIVOS ---

# Calcular checksums
echo "contenido de prueba" > /tmp/test_hash.txt
echo "=== SHA-256 ==="
sha256sum /tmp/test_hash.txt

echo "=== SHA-512 ==="
sha512sum /tmp/test_hash.txt

echo "=== MD5 (solo referencia, NO usar para seguridad) ==="
md5sum /tmp/test_hash.txt

# --- SSH KEYS ---

# Ver tus claves SSH (si existen)
ls -la ~/.ssh/

# La clave publica se comparte (*.pub)
# La clave privada NUNCA se comparte
cat ~/.ssh/id_ed25519.pub 2>/dev/null || echo "No tienes clave Ed25519"
cat ~/.ssh/id_rsa.pub 2>/dev/null || echo "No tienes clave RSA"

# Limpiar archivos de prueba
rm -f /tmp/secreto.txt /tmp/secreto.txt.gpg /tmp/secreto.enc
rm -f /tmp/secreto_descifrado.txt /tmp/privada.pem /tmp/publica.pem
rm -f /tmp/test_hash.txt
```

### Ejercicio 4: Verificacion de integridad de paquetes

```bash
# Linux verifica la integridad de paquetes con firmas GPG

# Ver claves GPG de APT (Ubuntu/Debian)
apt-key list 2>/dev/null | head -20

# Ver la firma de un paquete descargado
# apt download coreutils
# dpkg-sig --verify coreutils_*.deb 2>/dev/null

# Verificar integridad de archivos del sistema con debsums
# sudo apt install debsums
# sudo debsums --changed  # Muestra archivos modificados
```

## 8.4 Resumen del Modulo

```
CIFRADO SIMETRICO:
  - Una clave para cifrar y descifrar
  - Rapido, para datos grandes
  - Algoritmo: AES-256 (estandar)
  - Problema: compartir la clave

CIFRADO ASIMETRICO:
  - Par de claves: publica + privada
  - Lento, para datos pequenos o intercambio de claves
  - Algoritmos: RSA-2048, Ed25519
  - Resuelve el problema del intercambio de claves

HASH:
  - Funcion unidireccional (no se puede revertir)
  - Para passwords: bcrypt, argon2 (con salt)
  - Para integridad: SHA-256, SHA-512
  - Para autenticacion de mensajes: HMAC

FIRMA DIGITAL:
  - Hash del mensaje + cifrado con clave privada
  - Prueba autenticidad e integridad

CIFRADO HIBRIDO:
  - RSA para intercambiar clave AES
  - AES para cifrar los datos
  - Asi funciona TLS/HTTPS

EN LINUX:
  - gpg: cifrado de archivos y emails
  - openssl: operaciones criptograficas
  - LUKS: cifrado de disco completo
  - SSH: comunicacion cifrada
```

## 8.5 Preguntas de Repaso

1. Cual es la diferencia entre cifrado simetrico y asimetrico?
2. Por que se usa cifrado hibrido en TLS y no solo RSA?
3. Que es un hash y por que NO es cifrado?
4. Por que se usa salt al hashear passwords?
5. Que es una firma digital y que garantiza?
6. Que algoritmo de hash usarias para passwords? Por que no SHA-256?
