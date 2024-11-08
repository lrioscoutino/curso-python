Ejemplo práctico de programación de sockets en Python con un servidor y un cliente que pueden comunicarse entre sí.



```python
# servidor.py
import socket
import threading

class ServidorChat:
    def __init__(self, host='localhost', port=55555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        
        self.clientes = []
        self.nicknames = []
        
    def broadcast(self, mensaje):
        """Envía un mensaje a todos los clientes conectados"""
        for cliente in self.clientes:
            cliente.send(mensaje)
    
    def handle_client(self, cliente):
        """Maneja los mensajes de un cliente específico"""
        while True:
            try:
                # Recibir mensaje del cliente
                mensaje = cliente.recv(1024)
                # Transmitir el mensaje a todos los clientes
                self.broadcast(mensaje)
            except:
                # Remover y cerrar cliente si hay error
                index = self.clientes.index(cliente)
                self.clientes.remove(cliente)
                cliente.close()
                nickname = self.nicknames[index]
                self.broadcast(f'{nickname} se ha desconectado!'.encode('utf-8'))
                self.nicknames.remove(nickname)
                break
    
    def start(self):
        """Inicia el servidor y acepta conexiones"""
        print("Servidor iniciado y escuchando...")
        while True:
            # Aceptar conexión
            cliente, address = self.server.accept()
            print(f"Conectado con {str(address)}")
            
            # Solicitar y almacenar nickname
            cliente.send('NICK'.encode('utf-8'))
            nickname = cliente.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clientes.append(cliente)
            
            # Imprimir y transmitir nickname
            print(f'Nickname del cliente es {nickname}!')
            self.broadcast(f'{nickname} se unió al chat!'.encode('utf-8'))
            cliente.send('Conectado al servidor!'.encode('utf-8'))
            
            # Iniciar hilo para el cliente
            thread = threading.Thread(target=self.handle_client, args=(cliente,))
            thread.start()

# Iniciar el servidor
if __name__ == "__main__":
    servidor = ServidorChat()
    servidor.start()

# cliente.py
import socket
import threading

class ClienteChat:
    def __init__(self, host='localhost', port=55555):
        self.nickname = input("Elige un nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.running = True

    def receive(self):
        """Recibe mensajes del servidor"""
        while self.running:
            try:
                mensaje = self.client.recv(1024).decode('utf-8')
                if mensaje == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(mensaje)
            except:
                print("¡Error!")
                self.client.close()
                break

    def write(self):
        """Envía mensajes al servidor"""
        while self.running:
            mensaje = f'{self.nickname}: {input("")}'
            self.client.send(mensaje.encode('utf-8'))

    def start(self):
        """Inicia los hilos de recepción y escritura"""
        receive_thread = threading.Thread(target=self.receive)
        write_thread = threading.Thread(target=self.write)
        
        receive_thread.start()
        write_thread.start()

# Iniciar el cliente
if __name__ == "__main__":
    cliente = ClienteChat()
    cliente.start()

```

Este ejemplo implementa un chat básico usando sockets. Aquí está cómo funciona:

1. Para probar el código, guarda los archivos como `servidor.py` y `cliente.py`

2. Primero, ejecuta el servidor:
```bash
python servidor.py
```

3. Luego, ejecuta el cliente en otra terminal:
```bash
python cliente.py
```

4. Puedes ejecutar múltiples clientes para simular un chat grupal.

Características del código:

- Usa TCP/IP para la comunicación
- Soporta múltiples clientes simultáneos usando threads
- Maneja desconexiones gracefully
- Broadcast de mensajes a todos los clientes conectados
- Sistema de nicknames para identificar usuarios

El código implementa las siguientes funcionalidades:

**Servidor:**
- Acepta conexiones entrantes
- Maneja múltiples clientes simultáneamente
- Transmite mensajes a todos los clientes
- Maneja desconexiones de clientes

**Cliente:**
- Se conecta al servidor
- Envía mensajes al chat
- Recibe mensajes de otros usuarios
- Maneja la desconexión del servidor
