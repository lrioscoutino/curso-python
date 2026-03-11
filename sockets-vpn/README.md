# Sockets en Red VPN para Interoperabilidad de Sistemas Operativos

Tutorial teórico-práctico paso a paso sobre la implementación de sockets en una red VPN para la comunicación entre Linux, Windows y macOS.

---

## Tabla de Contenidos

1. [Fundamentos Teóricos](#1-fundamentos-teóricos)
2. [Configuración del Entorno VPN](#2-configuración-del-entorno-vpn)
3. [Protocolo de Comunicación Multiplataforma](#3-protocolo-de-comunicación-multiplataforma)
4. [Servidor Multiplataforma (TCP)](#4-servidor-multiplataforma-tcp)
5. [Cliente Multiplataforma](#5-cliente-multiplataforma)
6. [Transferencia de Archivos](#6-transferencia-de-archivos)
7. [Descubrimiento de Servicios (UDP)](#7-descubrimiento-de-servicios-udp)
8. [Arquitectura Completa](#8-arquitectura-completa)
9. [Checklist de Interoperabilidad](#9-checklist-de-interoperabilidad)
10. [Ejercicios](#10-ejercicios)

---

## 1. Fundamentos Teóricos

### 1.1 ¿Qué es un Socket?

Un socket es un **endpoint de comunicación bidireccional** entre dos procesos, identificado por:

```
(Protocolo, IP_local, Puerto_local, IP_remota, Puerto_remota)
```

**Tipos principales:**

| Tipo | Constante | Descripción | Caso de uso |
|------|-----------|-------------|-------------|
| TCP | `SOCK_STREAM` | Conexión confiable, ordenada | Transferencia de archivos, APIs |
| UDP | `SOCK_DGRAM` | Sin conexión, rápido | Streaming, juegos, descubrimiento |
| RAW | `SOCK_RAW` | Acceso directo al protocolo IP | Herramientas de diagnóstico |

### 1.2 ¿Por qué VPN + Sockets?

Una VPN crea una **red virtual privada** donde máquinas con distintos SO comparten un espacio de direcciones IP privado. Los sockets operan sobre esta capa de red de forma transparente.

```
┌─────────────┐         VPN Tunnel          ┌─────────────┐
│  Linux      │══════════════════════════════│  Windows    │
│  10.8.0.2   │   (cifrado, encapsulado)     │  10.8.0.3   │
│  Server.py  │                              │  Client.exe │
└─────────────┘                              └─────────────┘
        │                                           │
        └───────── Red Virtual: 10.8.0.0/24 ────────┘
```

**Ventajas:**

- Comunicación segura (cifrada) sin implementar TLS manualmente
- IPs estables en la red virtual
- Atraviesa NAT y firewalls
- Los sockets funcionan igual que en una LAN

### 1.3 Desafíos de Interoperabilidad entre SO

| Problema | Descripción | Solución |
|----------|-------------|----------|
| **Byte order** | x86 es little-endian, la red usa big-endian | Usar `htonl/ntohl` o `struct.pack('!I', ...)` |
| **Encoding** | Windows usa CP-1252 por defecto, Linux UTF-8 | Forzar UTF-8 en todo mensaje |
| **Line endings** | Windows: `\r\n`, Linux/macOS: `\n` | Normalizar al recibir |
| **Path separators** | Windows: `\`, Linux/macOS: `/` | Usar `pathlib` o normalizar |
| **Tamaño de datos** | `int` varía entre plataformas en C | Definir protocolo con tamaños fijos |

---

## 2. Configuración del Entorno VPN

### 2.1 Instalar WireGuard

WireGuard es más simple y eficiente que OpenVPN. Usa criptografía moderna y tiene un código base mínimo.

#### Servidor (Linux)

```bash
# Instalar
sudo apt install wireguard

# Generar claves
wg genkey | tee server_private.key | wg pubkey > server_public.key
```

Crear `/etc/wireguard/wg0.conf`:

```ini
[Interface]
PrivateKey = <CLAVE_PRIVADA_SERVIDOR>
Address = 10.8.0.1/24
ListenPort = 51820

[Peer]
# Cliente Windows
PublicKey = <CLAVE_PUBLICA_CLIENTE_WINDOWS>
AllowedIPs = 10.8.0.2/32

[Peer]
# Cliente macOS
PublicKey = <CLAVE_PUBLICA_CLIENTE_MACOS>
AllowedIPs = 10.8.0.3/32
```

```bash
# Activar
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

#### Cliente (Windows)

Descargar WireGuard desde [wireguard.com](https://www.wireguard.com/install/), crear túnel con:

```ini
[Interface]
PrivateKey = <CLAVE_PRIVADA_CLIENTE>
Address = 10.8.0.2/24

[Peer]
PublicKey = <CLAVE_PUBLICA_SERVIDOR>
Endpoint = <IP_PUBLICA_SERVIDOR>:51820
AllowedIPs = 10.8.0.0/24
PersistentKeepalive = 25
```

#### Verificar conectividad

```bash
ping 10.8.0.1   # servidor
ping 10.8.0.2   # cliente windows
ping 10.8.0.3   # cliente macOS
```

---

## 3. Protocolo de Comunicación Multiplataforma

### 3.1 Formato de Mensaje Binario Portable

```
┌──────────┬──────────┬────────┬───────────────┐
│ MAGIC(2) │ TYPE(1)  │ LEN(4) │  PAYLOAD(N)   │
│  0xCAFE  │  uint8   │ uint32 │   bytes       │
└──────────┴──────────┴────────┴───────────────┘
```

- **MAGIC** (2 bytes): Identificador del protocolo `0xCAFE`
- **TYPE** (1 byte): Tipo de mensaje
  - `0x01` = texto
  - `0x02` = archivo
  - `0x03` = comando
  - `0x04` = heartbeat
- **LEN** (4 bytes, big-endian): Longitud del payload
- **PAYLOAD** (N bytes): Datos codificados en UTF-8

### 3.2 Implementación del Protocolo

> Archivo: `protocol.py` — Funciona en Linux, Windows y macOS

```python
import struct

MAGIC = b'\xCA\xFE'
HEADER_SIZE = 7  # 2 + 1 + 4

MSG_TEXT = 0x01
MSG_FILE = 0x02
MSG_CMD  = 0x03
MSG_HEARTBEAT = 0x04


def pack_message(msg_type: int, payload: bytes) -> bytes:
    """Empaqueta un mensaje con header portable.

    '!' = network byte order (big-endian) — clave para interoperabilidad.
    """
    header = MAGIC + struct.pack('!B I', msg_type, len(payload))
    return header + payload


def unpack_header(data: bytes) -> tuple[int, int]:
    """Desempaqueta header. Retorna (tipo, longitud)."""
    if data[:2] != MAGIC:
        raise ValueError("Magic number inválido")
    msg_type, length = struct.unpack('!B I', data[2:7])
    return msg_type, length


def recv_message(sock) -> tuple[int, bytes]:
    """Recibe un mensaje completo del socket."""
    header = recv_exact(sock, HEADER_SIZE)
    msg_type, length = unpack_header(header)
    payload = recv_exact(sock, length) if length > 0 else b''
    return msg_type, payload


def recv_exact(sock, n: int) -> bytes:
    """Recibe exactamente n bytes — maneja fragmentación TCP.

    TCP puede entregar datos en chunks parciales, por eso
    debemos iterar hasta recibir exactamente la cantidad
    esperada de bytes.
    """
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Conexión cerrada")
        data.extend(chunk)
    return bytes(data)
```

---

## 4. Servidor Multiplataforma (TCP)

> Archivo: `server.py` — Ejecutar en Linux (10.8.0.1)

```python
import socket
import threading
import json
import platform
from protocol import pack_message, recv_message, MSG_TEXT, MSG_HEARTBEAT

VPN_HOST = '10.8.0.1'  # IP en la VPN
PORT = 9000

clients: dict[str, socket.socket] = {}
lock = threading.Lock()


def handle_client(conn: socket.socket, addr: tuple):
    """Maneja la conexión de un cliente individual."""
    client_id = f"{addr[0]}:{addr[1]}"
    print(f"[+] Conectado: {client_id}")

    with lock:
        clients[client_id] = conn

    try:
        # Enviar info del servidor al conectarse
        info = json.dumps({
            "server_os": platform.system(),
            "server_version": platform.version(),
            "python": platform.python_version(),
        }).encode('utf-8')
        conn.sendall(pack_message(MSG_TEXT, info))

        while True:
            msg_type, payload = recv_message(conn)

            if msg_type == MSG_TEXT:
                text = payload.decode('utf-8')
                print(f"[{client_id}] {text}")
                broadcast(client_id, msg_type, payload)

            elif msg_type == MSG_HEARTBEAT:
                conn.sendall(pack_message(MSG_HEARTBEAT, b'pong'))

    except ConnectionError:
        print(f"[-] Desconectado: {client_id}")
    finally:
        with lock:
            clients.pop(client_id, None)
        conn.close()


def broadcast(sender_id: str, msg_type: int, payload: bytes):
    """Envía un mensaje a todos los clientes excepto al emisor."""
    with lock:
        for cid, sock in clients.items():
            if cid != sender_id:
                try:
                    sock.sendall(pack_message(msg_type, payload))
                except OSError:
                    pass


def main():
    # AF_INET + SOCK_STREAM = TCP/IPv4
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((VPN_HOST, PORT))
    srv.listen(5)

    print(f"[*] Servidor escuchando en {VPN_HOST}:{PORT}")
    print(f"[*] SO: {platform.system()} {platform.release()}")

    try:
        while True:
            conn, addr = srv.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True,
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[*] Servidor detenido")
    finally:
        srv.close()


if __name__ == '__main__':
    main()
```

---

## 5. Cliente Multiplataforma

> Archivo: `client.py` — Ejecutar en cualquier SO conectado a la VPN

```python
import socket
import threading
import json
import platform
from protocol import pack_message, recv_message, MSG_TEXT, MSG_HEARTBEAT

VPN_SERVER = '10.8.0.1'
PORT = 9000


def receive_loop(sock: socket.socket):
    """Hilo que escucha mensajes del servidor."""
    try:
        while True:
            msg_type, payload = recv_message(sock)

            if msg_type == MSG_TEXT:
                text = payload.decode('utf-8')
                try:
                    data = json.loads(text)
                    if 'server_os' in data:
                        print(f"\n[Servidor] SO={data['server_os']}, "
                              f"Python={data['python']}")
                        continue
                except json.JSONDecodeError:
                    pass
                print(f"\n[Mensaje] {text}")

            elif msg_type == MSG_HEARTBEAT:
                pass  # pong recibido

    except ConnectionError:
        print("\n[!] Conexión con servidor perdida")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((VPN_SERVER, PORT))

    print(f"[*] Conectado a {VPN_SERVER}:{PORT}")
    print(f"[*] SO local: {platform.system()} {platform.release()}")
    print("[*] Comandos: /info (enviar info SO), /quit (salir)\n")

    thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    thread.start()

    try:
        while True:
            text = input("> ")
            if text.lower() == '/quit':
                break
            if text.lower() == '/info':
                info = {
                    "os": platform.system(),
                    "release": platform.release(),
                    "machine": platform.machine(),
                    "python": platform.python_version(),
                }
                payload = json.dumps(info).encode('utf-8')
            else:
                payload = text.encode('utf-8')
            sock.sendall(pack_message(MSG_TEXT, payload))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("[*] Desconectado")


if __name__ == '__main__':
    main()
```

---

## 6. Transferencia de Archivos

> Archivo: `file_transfer.py` — Módulo de transferencia portable

```python
import os
import json
from protocol import pack_message, recv_message, MSG_FILE

CHUNK_SIZE = 65536  # 64KB


def send_file(sock, filepath: str):
    """Envía un archivo en chunks por el socket."""
    filename = os.path.basename(filepath)  # Normaliza separadores de ruta
    filesize = os.path.getsize(filepath)

    # Enviar metadata como JSON
    meta = json.dumps({
        "filename": filename,
        "size": filesize,
    }).encode('utf-8')
    sock.sendall(pack_message(MSG_FILE, meta))

    # Enviar contenido en chunks
    sent = 0
    with open(filepath, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sock.sendall(pack_message(MSG_FILE, chunk))
            sent += len(chunk)
            print(f"\r  Enviando: {sent}/{filesize} bytes "
                  f"({100 * sent // filesize}%)", end='', flush=True)
    print(" — Completo")


def recv_file(sock, output_dir: str) -> str:
    """Recibe un archivo completo. Retorna la ruta del archivo guardado."""
    # Recibir metadata
    _, meta_bytes = recv_message(sock)
    meta = json.loads(meta_bytes.decode('utf-8'))

    # Seguridad: evitar path traversal usando solo el nombre base
    filename = os.path.basename(meta['filename'])
    filesize = meta['size']

    filepath = os.path.join(output_dir, filename)
    received = 0

    with open(filepath, 'wb') as f:
        while received < filesize:
            _, chunk = recv_message(sock)
            f.write(chunk)
            received += len(chunk)
            print(f"\r  Recibiendo: {received}/{filesize} bytes "
                  f"({100 * received // filesize}%)", end='', flush=True)
    print(" — Completo")
    return filepath
```

---

## 7. Descubrimiento de Servicios (UDP)

> Archivo: `discovery.py` — Descubrir otros nodos en la VPN

```python
import socket
import json
import platform
import time

DISCOVERY_PORT = 9001
VPN_BROADCAST = '10.8.0.255'  # Broadcast de la subred VPN


def announce(interval: int = 5):
    """Anuncia presencia en la red VPN cada `interval` segundos."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    info = json.dumps({
        "hostname": platform.node(),
        "os": platform.system(),
        "service_port": 9000,
    }).encode('utf-8')

    while True:
        sock.sendto(info, (VPN_BROADCAST, DISCOVERY_PORT))
        time.sleep(interval)


def listen_for_peers():
    """Escucha anuncios de otros nodos en la red VPN."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', DISCOVERY_PORT))

    print("[*] Escuchando peers en la VPN...")
    seen = set()

    while True:
        data, addr = sock.recvfrom(1024)
        if addr[0] not in seen:
            seen.add(addr[0])
            info = json.loads(data.decode('utf-8'))
            print(f"[Peer] {addr[0]} — {info['hostname']} "
                  f"({info['os']}) puerto:{info['service_port']}")
```

---

## 8. Arquitectura Completa

```
                        ┌─────────────────────────────┐
                        │      Red VPN (WireGuard)     │
                        │       10.8.0.0/24            │
                        └──────────┬──────────────────-┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
   ┌──────┴──────┐          ┌──────┴──────┐          ┌──────┴──────┐
   │   Linux     │          │   Windows   │          │   macOS     │
   │  10.8.0.1   │          │  10.8.0.2   │          │  10.8.0.3   │
   │             │          │             │          │             │
   │ ┌─────────┐ │          │ ┌─────────┐ │          │ ┌─────────┐ │
   │ │ Server  │ │◄──TCP───►│ │ Client  │ │          │ │ Client  │ │
   │ │ :9000   │ │          │ │         │ │          │ │         │ │
   │ └─────────┘ │          │ └─────────┘ │          │ └─────────┘ │
   │ ┌─────────┐ │          │ ┌─────────┐ │          │ ┌─────────┐ │
   │ │Discovery│ │◄──UDP───►│ │Discovery│ │◄──UDP───►│ │Discovery│ │
   │ │ :9001   │ │broadcast │ │ :9001   │ │broadcast │ │ :9001   │ │
   │ └─────────┘ │          │ └─────────┘ │          │ └─────────┘ │
   └─────────────┘          └─────────────┘          └─────────────┘
```

### Capas del sistema

```
┌──────────────────────────────────────┐
│  Aplicación (protocol.py, JSON)      │  ← Tu código
├──────────────────────────────────────┤
│  Socket API (TCP/UDP)                │  ← El SO abstrae diferencias
├──────────────────────────────────────┤
│  VPN (WireGuard tunnel)              │  ← Cifrado + encapsulación
├──────────────────────────────────────┤
│  Internet / Red física               │  ← Transporte real
└──────────────────────────────────────┘
```

---

## 9. Checklist de Interoperabilidad

- [ ] Usar network byte order (`!` en `struct.pack`) siempre
- [ ] Codificar strings como UTF-8 explícitamente
- [ ] Normalizar rutas con `os.path.basename()` al recibir nombres de archivo
- [ ] Usar `recv_exact()` para manejar fragmentación TCP
- [ ] JSON como formato de intercambio de datos
- [ ] Probar en los 3 SO antes de considerar estable
- [ ] Manejar `\r\n` vs `\n` al procesar texto línea por línea
- [ ] No asumir tamaño de `int` — usar tamaños explícitos en el protocolo
- [ ] Abrir puertos en la interfaz VPN (no en la pública)
- [ ] Configurar `sock.settimeout()` para detectar nodos caídos

---

## 10. Ejercicios

| # | Ejercicio | Dificultad |
|---|-----------|------------|
| 1 | Ejecutar server en Linux, client en Windows, enviar mensajes | Basico |
| 2 | Agregar transferencia de archivos con barra de progreso | Intermedio |
| 3 | Implementar heartbeat cada 10s para detectar desconexiones | Intermedio |
| 4 | Agregar descubrimiento automatico de peers con UDP | Intermedio |
| 5 | Reemplazar threading con `asyncio` para mejor escalabilidad | Avanzado |
| 6 | Implementar un sistema de comandos remotos (tipo SSH ligero) | Avanzado |
| 7 | Agregar autenticacion con token al conectarse | Avanzado |

---

## Estructura del Proyecto

```
sockets-vpn/
├── README.md            # Este archivo
├── protocol.py          # Protocolo binario portable
├── server.py            # Servidor TCP multi-cliente
├── client.py            # Cliente TCP multiplataforma
├── file_transfer.py     # Transferencia de archivos
└── discovery.py         # Descubrimiento UDP de peers
```

## Ejecucion

```bash
# En el servidor (Linux, 10.8.0.1)
python3 server.py

# En cada cliente (Windows, macOS u otro Linux)
python3 client.py
```
