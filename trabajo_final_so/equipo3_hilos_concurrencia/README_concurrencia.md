[Contenido anterior se mantiene]

# Conceptos Fundamentales de Programación Concurrente

## Definiciones Clave

### 1. Concurrencia vs Paralelismo
**Concurrencia**: 
- Definición: La capacidad de un sistema para manejar múltiples tareas en progreso al mismo tiempo.
- Ejemplo práctico: Un cajero de banco atendiendo a múltiples filas de clientes, alternando entre ellas.
```python
# Ejemplo de concurrencia con threading
import threading

def tarea(nombre):
    print(f"Iniciando tarea {nombre}")
    # Simular trabajo
    time.sleep(1)
    print(f"Completando tarea {nombre}")

# Crear múltiples threads
threads = [threading.Thread(target=tarea, args=(f"T{i}",)) for i in range(3)]
for t in threads:
    t.start()
```

**Paralelismo**: 
- Definición: La ejecución simultánea real de múltiples tareas, utilizando múltiples recursos de procesamiento.
- Ejemplo práctico: Múltiples cajeros atendiendo a diferentes clientes simultáneamente.
```python
# Ejemplo de paralelismo con multiprocessing
import multiprocessing

def proceso(nombre):
    print(f"Ejecutando proceso {nombre}")
    # Trabajo real en otro núcleo de CPU
    resultado = sum(i * i for i in range(10**6))

if __name__ == '__main__':
    procesos = [multiprocessing.Process(target=proceso, args=(f"P{i}",)) 
                for i in range(3)]
    for p in procesos:
        p.start()
```

### 2. Thread (Hilo)
- Definición: Unidad básica de ejecución dentro de un proceso. Múltiples threads comparten el mismo espacio de memoria.
- Características:
  * Comparten recursos del proceso
  * Creación más ligera que un proceso
  * Útil para tareas I/O-bound
```python
import threading

class MiThread(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        print(f"Thread {self.nombre} ejecutándose")

# Uso
thread = MiThread("T1")
thread.start()
```

### 3. Proceso
- Definición: Instancia independiente de un programa en ejecución, con su propio espacio de memoria.
- Características:
  * Aislamiento de memoria
  * Mayor overhead de creación
  * Ideal para tareas CPU-bound
```python
import multiprocessing

def worker(nombre):
    print(f"Proceso {nombre} trabajando")

if __name__ == '__main__':
    proceso = multiprocessing.Process(target=worker, args=("P1",))
    proceso.start()
    proceso.join()
```

### 4. Race Condition
- Definición: Situación donde el resultado depende del orden de ejecución de múltiples threads.
- Ejemplo de problema:
```python
# Ejemplo de race condition
contador = 0

def incrementar():
    global contador
    actual = contador
    time.sleep(0.1)  # Simular algún procesamiento
    contador = actual + 1

# Este código puede producir resultados inconsistentes
threads = [threading.Thread(target=incrementar) for _ in range(5)]
for t in threads:
    t.start()
```

- Solución usando lock:
```python
contador = 0
lock = threading.Lock()

def incrementar_seguro():
    global contador
    with lock:
        actual = contador
        time.sleep(0.1)
        contador = actual + 1

# Este código producirá resultados consistentes
threads = [threading.Thread(target=incrementar_seguro) for _ in range(5)]
for t in threads:
    t.start()
```

### 5. Deadlock
- Definición: Situación donde dos o más threads están bloqueados mutuamente, esperando recursos que el otro tiene.
- Ejemplo:
```python
lock1 = threading.Lock()
lock2 = threading.Lock()

def tarea1():
    with lock1:
        time.sleep(0.1)  # Aumenta la probabilidad de deadlock
        with lock2:
            print("Tarea 1 completada")

def tarea2():
    with lock2:
        time.sleep(0.1)
        with lock1:
            print("Tarea 2 completada")

# Este código puede resultar en deadlock
t1 = threading.Thread(target=tarea1)
t2 = threading.Thread(target=tarea2)
t1.start()
t2.start()
```

### 6. Mecanismos de Sincronización

#### a. Lock (Cerrojo)
- Definición: Mecanismo básico de sincronización para garantizar el acceso exclusivo a recursos compartidos.
```python
lock = threading.Lock()

def acceso_seguro():
    with lock:
        # Código que accede a recursos compartidos
        pass
```

#### b. Semaphore (Semáforo)
- Definición: Contador que permite el acceso a un recurso a un número limitado de threads.
```python
# Limitar el acceso a 3 threads simultáneos
semaforo = threading.Semaphore(3)

def acceso_limitado():
    with semaforo:
        print("Accediendo al recurso")
        time.sleep(1)
```

#### c. Event
- Definición: Mecanismo para comunicación entre threads, donde uno espera una señal de otro.
```python
evento = threading.Event()

def esperar_señal():
    print("Esperando señal...")
    evento.wait()
    print("Señal recibida!")

def enviar_señal():
    time.sleep(2)
    evento.set()

t1 = threading.Thread(target=esperar_señal)
t2 = threading.Thread(target=enviar_señal)
t1.start()
t2.start()
```

### 7. AsyncIO
- Definición: Modelo de programación concurrente basado en corrutinas, eventos y tareas.
- Características:
  * Ideal para operaciones I/O-bound
  * Usa un solo thread
  * Basado en eventos y callbacks
```python
import asyncio

async def tarea_asincrona(nombre):
    print(f"Iniciando {nombre}")
    await asyncio.sleep(1)  # Simular I/O
    print(f"Completado {nombre}")

async def main():
    tareas = [tarea_asincrona(f"Tarea {i}") for i in range(3)]
    await asyncio.gather(*tareas)

asyncio.run(main())
```

# Ejercicios de Práctica

### Ejercicio 1: Identificación de Race Conditions
Analiza el siguiente código y explica por qué puede ocurrir una race condition:
```python
class Contador:
    def __init__(self):
        self.valor = 0

    def incrementar(self):
        temp = self.valor
        time.sleep(0.0001)  # Simular procesamiento
        self.valor = temp + 1

# Crear instancia compartida
contador = Contador()

def worker():
    for _ in range(100):
        contador.incrementar()

threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Valor final: {contador.valor}")
```

### Ejercicio 2: Resolución de Deadlock
Modifica el siguiente código para prevenir el deadlock:
```python
def transferir(origen, destino, cantidad):
    with origen.lock:
        with destino.lock:
            origen.balance -= cantidad
            destino.balance += cantidad

class Cuenta:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()

# Escenario de deadlock
cuenta1 = Cuenta(1000)
cuenta2 = Cuenta(1000)

t1 = threading.Thread(target=transferir, args=(cuenta1, cuenta2, 100))
t2 = threading.Thread(target=transferir, args=(cuenta2, cuenta1, 50))
```

[Resto del contenido original se mantiene]

