# Práctica de WebSockets con Python: De Junior a Middle

Esta guía te llevará a través de los conceptos teóricos y prácticos de los WebSockets en Python, manteniendo los ejemplos simples y claros.

---

### **Contexto Teórico: ¿Qué son los WebSockets?**

#### El Problema con HTTP

Imagina que estás chateando en una web. Con el protocolo HTTP tradicional, cada vez que quieres enviar un mensaje, tu navegador envía una petición al servidor (como tocar una puerta). El servidor responde y cierra la conexión (abre la puerta, te da algo y la cierra). Si quieres saber si tienes mensajes nuevos, tienes que volver a tocar la puerta una y otra vez (a esto se le llama *polling*). Es ineficiente y lento.

**Analogía:** HTTP es como enviar cartas por correo postal. Envías una, esperas una respuesta, y la conversación es lenta.

#### La Solución: WebSockets

Los WebSockets solucionan este problema creando una **conexión persistente y bidireccional** entre el cliente (tu navegador) y el servidor.

1.  **El "Apretón de Manos" (Handshake):** La conexión empieza como una petición HTTP normal, pero el cliente le pide al servidor "actualizar" la conexión a un WebSocket.
2.  **Canal Abierto:** Si el servidor está de acuerdo, la conexión HTTP se transforma en una conexión WebSocket que permanece abierta.
3.  **Comunicación Bidireccional:** Ahora, tanto el cliente como el servidor pueden enviarse mensajes en cualquier momento, sin necesidad de hacer nuevas peticiones.

**Analogía:** Un WebSocket es como una llamada telefónica. Una vez que ambos contestan, la línea está abierta y pueden hablar libremente en ambas direcciones hasta que uno de los dos cuelga.

**Casos de uso comunes:**
*   Aplicaciones de chat en tiempo real.
*   Notificaciones instantáneas (como en redes sociales).
*   Juegos multijugador en línea.
*   Paneles de datos que se actualizan en vivo (ej. precios de acciones).

---

### **Parte 1: Nivel Junior - Un Servidor de "Eco"**

El "Hola, Mundo" de los WebSockets. Crearemos un servidor que simplemente devuelve cualquier mensaje que recibe.

#### **Paso 1: Instalación**

Usaremos la librería `websockets`, que es muy popular y fácil de usar.

```bash
pip install websockets
```

#### **Paso 2: Código del Servidor de Eco (`server_echo.py`)**

Crea un archivo llamado `server_echo.py`.

```python
import asyncio
import websockets

# Esta función se ejecuta cada vez que un cliente se conecta.
async def echo(websocket, path):
    print(f"Cliente conectado desde {websocket.remote_address}")
    try:
        # Itera sobre los mensajes recibidos del cliente.
        async for message in websocket:
            print(f"Recibido del cliente: {message}")
            
            # Envía el mismo mensaje de vuelta al cliente.
            await websocket.send(message)
            print(f"Enviado al cliente: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"Cliente desconectado: {websocket.remote_address}")
    finally:
        # El bucle termina cuando el cliente se desconecta.
        print("Conexión cerrada.")

async def main():
    # Inicia el servidor de WebSockets en localhost, puerto 8765.
    # Llama a la función `echo` para cada nueva conexión.
    async with websockets.serve(echo, "localhost", 8765):
        print("Servidor de Eco iniciado en ws://localhost:8765")
        await asyncio.Future()  # Mantiene el servidor corriendo indefinidamente.

if __name__ == "__main__":
    asyncio.run(main())
```

#### **Paso 3: Código del Cliente de Eco (`client_echo.py`)**

Crea otro archivo llamado `client_echo.py`.

```python
import asyncio
import websockets

async def send_and_receive():
    # Se conecta al servidor WebSocket.
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message_to_send = "Hola, Servidor!"
        
        # Envía un mensaje.
        await websocket.send(message_to_send)
        print(f"> Enviado: {message_to_send}")
        
        # Espera y recibe la respuesta del servidor.
        response = await websocket.recv()
        print(f"< Recibido: {response}")

if __name__ == "__main__":
    asyncio.run(send_and_receive())
```

#### **Paso 4: ¡A Probar!**

1.  Abre una terminal y ejecuta el servidor: `python server_echo.py`
2.  Abre **otra** terminal y ejecuta el cliente: `python client_echo.py`

Verás cómo el cliente envía "Hola, Servidor!" y el servidor se lo devuelve inmediatamente.

---

### **Parte 2: Nivel Middle - Una Sala de Chat Simple (Broadcast)**

Ahora, hagamos que el servidor reenvíe los mensajes de un cliente a **todos** los demás clientes conectados.

#### **Paso 1: El Concepto de "Broadcast"**

Para hacer un broadcast, el servidor necesita mantener un registro de todos los clientes que están conectados en un momento dado. Un `set` de Python es perfecto para esto.

#### **Paso 2: Código del Servidor de Chat (`server_chat.py`)**

```python
import asyncio
import websockets
import json

# Un conjunto para almacenar todas las conexiones de clientes activas.
CONNECTED_CLIENTS = set()

async def handler(websocket, path):
    # Añade el nuevo cliente al conjunto de conexiones.
    CONNECTED_CLIENTS.add(websocket)
    print(f"Nuevo cliente conectado. Total: {len(CONNECTED_CLIENTS)}")
    
    try:
        # Escucha mensajes de este cliente.
        async for message in websocket:
            print(f"Mensaje recibido: {message}")
            
            # Prepara el mensaje para el broadcast.
            # Podríamos añadir información del remitente aquí.
            
            # Crea una lista de tareas de envío para todos los clientes.
            tasks = [client.send(message) for client in CONNECTED_CLIENTS]
            
            # Ejecuta todas las tareas de envío de forma concurrente.
            await asyncio.gather(*tasks)
            print(f"Mensaje '{message}' enviado a {len(CONNECTED_CLIENTS)} clientes.")

    except websockets.exceptions.ConnectionClosed:
        print("Un cliente se ha desconectado.")
    finally:
        # Elimina al cliente del conjunto cuando se desconecta.
        CONNECTED_CLIENTS.remove(websocket)
        print(f"Cliente eliminado. Total: {len(CONNECTED_CLIENTS)}")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Servidor de Chat iniciado en ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
```

#### **Paso 3: Código del Cliente de Chat (`client_chat.py`)**

Este cliente necesita hacer dos cosas a la vez: escuchar los mensajes del servidor y permitir al usuario escribir mensajes. Usaremos `asyncio` para manejar esta concurrencia.

```python
import asyncio
import websockets

async def chat_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        
        # Tarea para recibir mensajes del servidor.
        async def receive_messages():
            try:
                async for message in websocket:
                    # Imprime el mensaje recibido para que el usuario lo vea.
                    print(f"\n< Mensaje de otro usuario: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Conexión cerrada por el servidor.")

        # Tarea para enviar mensajes escritos por el usuario.
        async def send_messages():
            while True:
                message = await asyncio.to_thread(input, "Escribe tu mensaje y presiona Enter: ")
                if message.lower() == 'exit':
                    break
                await websocket.send(message)

        # Ejecuta ambas tareas concurrentemente.
        receive_task = asyncio.create_task(receive_messages())
        send_task = asyncio.create_task(send_messages())

        # Espera a que ambas tareas terminen (en este caso, nunca, hasta que se cancele).
        await asyncio.gather(receive_task, send_task)

if __name__ == "__main__":
    try:
        asyncio.run(chat_client())
    except KeyboardInterrupt:
        print("\nCerrando cliente.")

```
*Nota: `asyncio.to_thread` es una forma moderna y segura de ejecutar código bloqueante (como `input()`) en un hilo separado sin bloquear el bucle de eventos de asyncio.*

#### **Paso 4: ¡A Chatear!**

1.  Abre una terminal y ejecuta el servidor: `python server_chat.py`
2.  Abre una **segunda** terminal y ejecuta un cliente: `python client_chat.py`
3.  Abre una **tercera** terminal y ejecuta otro cliente: `python client_chat.py`

Ahora, escribe un mensaje en cualquiera de las terminales de los clientes y presiona Enter. Verás cómo tu mensaje aparece instantáneamente en la otra terminal. ¡Has creado una sala de chat!
