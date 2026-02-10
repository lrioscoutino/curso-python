# Tutorial de Sistemas Operativos: Procesos, Hilos, Concurrencia y Planificación

Este repositorio contiene un tutorial exhaustivo y resuelto sobre los conceptos fundamentales de los sistemas operativos, enfocado en **Procesos, Hilos, Concurrencia y Planificación**. Incluye una sección teórica con preguntas y respuestas detalladas, así como un ejercicio práctico de programación en Python para demostrar la concurrencia y la importancia de la sincronización.

## Tabla de Contenidos

1.  [Introducción](#introducción)
2.  [Parte 1: Conceptos Teóricos (Preguntas y Respuestas)](#parte-1-conceptos-teóricos-preguntas-y-respuestas)
    *   [2.1. Concepto de Proceso](#21-concepto-de-proceso)
    *   [2.2. Estados y Transiciones de los Procesos](#22-estados-y-transiciones-de-los-procesos)
    *   [2.3. Procesos Ligeros: Hilos o Hebras](#23-procesos-ligeros-hilos-o-hebras)
    *   [2.4. Concurrencia y Secuencialidad](#24-concurrencia-y-secuencialidad)
    *   [2.5. Niveles, Objetivos y Criterios de Planificación](#25-niveles-objetivos-y-criterios-de-planificación)
    *   [2.6. Técnicas de Administración del Planificador](#26-técnicas-de-administración-del-planificador)
3.  [Parte 2: Implementación Práctica (Python Resuelta)](#parte-2-implementación-práctica-python-resuelta)
    *   [Objetivo](#objetivo)
    *   [Escenario](#escenario)
    *   [Paso 2.1: Versión SIN Sincronización (Demostración de Condición de Carrera)](#paso-21-versión-sin-sincronización-demostración-de-condición-de-carrera)
    *   [Paso 2.2: Versión CON Sincronización (Resolución de Condiciones de Carrera)](#paso-22-versión-con-sincronización-resolución-de-condiciones-de-carrera)
    *   [Cómo Ejecutar el Código Python](#cómo-ejecutar-el-código-python)
4.  [Conclusión](#conclusión)

---

## Introducción

Este documento te guiará a través de los conceptos fundamentales de los sistemas operativos relacionados con la gestión de procesos, hilos, concurrencia y planificación. Se exploran las definiciones, diferencias y aplicaciones, proporcionando un recurso completo para estudiantes y entusiastas de los sistemas operativos.

---

## Parte 1: Conceptos Teóricos (Preguntas y Respuestas)

Esta sección cubre los aspectos teóricos clave con preguntas y respuestas detalladas para una comprensión sólida.

### 2.1. Concepto de Proceso

*   **Pregunta 1.1:** Define qué es un "proceso" en el contexto de los sistemas operativos. ¿En qué se diferencia fundamentalmente de un "programa"?
    *   **Respuesta:** Un **proceso** es una instancia de un programa en ejecución. Es una entidad activa con recursos asignados. Un **programa** es una entidad pasiva, un conjunto de instrucciones almacenadas. El programa es el "plano", el proceso es la "ejecución".

*   **Pregunta 1.2:** Explica el rol principal y los contenidos clave de un Bloque de Control de Proceso (PCB).
    *   **Respuesta:** El **PCB** es una estructura de datos que el SO usa para gestionar un proceso. Su rol es permitir el cambio de contexto, guardando el estado de la CPU. Contiene el estado del proceso, contador de programa, registros de CPU, información de planificación, gestión de memoria, contabilidad y estado de E/S.

### 2.2. Estados y Transiciones de los Procesos

*   **Pregunta 2.1:** Enumera y describe los cinco estados comunes en los que puede estar un proceso (Nuevo, Listo, Ejecución, Espera/Bloqueado, Terminado).
    *   **Respuesta:**
        1.  **Nuevo:** Siendo creado.
        2.  **Listo:** Creado, en memoria, esperando CPU.
        3.  **Ejecución:** Instrucciones siendo ejecutadas por CPU.
        4.  **Espera/Bloqueado:** Esperando un evento (E/S, recurso).
        5.  **Terminado:** Ha completado su ejecución o abortado.

*   **Pregunta 2.2:** Describe los eventos típicos que desencadenan las transiciones entre estos estados. Puedes usar un diagrama conceptual para ilustrar estas transiciones.
    *   **Respuesta:**
        ```
                +-------+      (Admisión)      +-------+
                | Nuevo |--------------------->| Listo |
                +-------+                      +-------+
                    ^                           |   ^
                    |                           |   |
                    |                           |   | (Evento Completo)
                    |                           |   |
                    |  (Creación)               |   |
                    |                           |   |
                    |                           v   | (Expulsión/Interrupción de Tiempo)
                    |                           +-------+
                    |                           | Ejecución |
                    |                           +-------+
                    |                           |   ^
                    |                           |   |
                    |                           |   | (Petición E/S/Evento)
                    |                           |   |
                    |                           v   |
                    |                           +-------+
                    |                           | Espera|
                    |                           +-------+
                    |                                |
                    |                                | (Fin del Proceso/Error)
                    +--------------------------------v
                                                +-------+
                                                | Terminado |
                                                +-------+
        ```
        Las transiciones son: Admisión, Despacho/Planificación, Interrupción de Tiempo/Expulsión, Petición de E/S/Evento, Evento Completo, Fin del Proceso/Error.

### 2.3. Procesos Ligeros: Hilos o Hebras

*   **Pregunta 3.1:** ¿Qué es un "hilo" (o hebra)?
    *   **Respuesta:** Un **hilo** es una unidad básica de utilización de la CPU dentro de un proceso. Comparte el espacio de direcciones de memoria del proceso, pero tiene su propio contador de programa, pila y registros.

*   **Pregunta 3.2:** Compara y contrasta procesos y hilos, destacando sus diferencias clave en términos de compartición de recursos, sobrecarga, mecanismos de comunicación e independencia.
    *   **Respuesta:**
        | Característica            | Procesos                                          | Hilos                                               |
        | :------------------------ | :------------------------------------------------ | :-------------------------------------------------- |
        | **Compartición de Recursos** | No comparten memoria por defecto.                | Comparten el espacio de memoria y recursos del proceso. |
        | **Sobrecarga (Creación/Conmutación)** | Alta.                                            | Baja.                                               |
        | **Comunicación**          | Requiere IPC explícitos y costosos.             | Más sencilla y eficiente (comparten memoria), requiere sincronización. |
        | **Independencia**         | Muy independientes.                               | Menos independientes (fallo en uno afecta a otros). |

*   **Pregunta 3.3:** Proporciona dos ejemplos distintos de escenarios donde el uso de hilos sería más beneficioso que usar procesos separados.
    *   **Respuesta:**
        1.  **Servidor Web Concurrente:** Para manejar múltiples solicitudes de clientes de forma eficiente, evitando la alta sobrecarga de creación de procesos.
        2.  **Interfaz de Usuario Gráfica (GUI) Reactiva:** Para realizar operaciones largas en segundo plano sin "congelar" la interfaz de usuario principal.

### 2.4. Concurrencia y Secuencialidad

*   **Pregunta 4.1:** Define claramente "concurrencia" y "secuencialidad" en la computación.
    *   **Respuesta:**
        *   **Secuencialidad:** Ejecución de tareas una tras otra, en orden predefinido.
        *   **Concurrencia:** Capacidad de gestionar múltiples tareas de forma "superpuesta" en el tiempo, dando la ilusión de simultaneidad.

*   **Pregunta 4.2:** Explica la relación entre concurrencia y paralelismo. ¿Puede una CPU de un solo núcleo lograr concurrencia? ¿Puede lograr verdadero paralelismo? Justifica tus respuestas.
    *   **Respuesta:**
        *   **Concurrencia:** Gestionar varias tareas que progresan al mismo tiempo.
        *   **Paralelismo:** Ejecutar varias tareas *literalmente* al mismo tiempo (en diferentes núcleos).
        *   **CPU de un solo núcleo:** **Sí** puede lograr concurrencia (mediante multiplexación de tiempo), pero **no** puede lograr verdadero paralelismo (solo puede ejecutar una instrucción a la vez).

### 2.5. Niveles, Objetivos y Criterios de Planificación

*   **Pregunta 5.1:** ¿Cuál es el propósito principal de la planificación de procesos en un sistema operativo?
    *   **Respuesta:** Optimizar el uso de la CPU y otros recursos, distribuyendo el tiempo de CPU entre los procesos para maximizar el rendimiento, minimizar tiempos de respuesta y asegurar equidad.

*   **Pregunta 5.2:** Identifica y describe al menos tres criterios o métricas cruciales utilizados para evaluar el rendimiento y la equidad de un algoritmo de planificación.
    *   **Respuesta:**
        1.  **Utilización de la CPU:** Porcentaje de tiempo que la CPU está ocupada.
        2.  **Tiempo de Retorno:** Tiempo total desde la llegada hasta la finalización del proceso.
        3.  **Tiempo de Espera:** Tiempo que un proceso pasa en la cola de listo.
        4.  **Tiempo de Respuesta:** Tiempo desde la solicitud hasta la primera respuesta.
        5.  **Rendimiento (Throughput):** Número de procesos completados por unidad de tiempo.

### 2.6. Técnicas de Administración del Planificador

*   **Pregunta 6.1:** Describe dos algoritmos de planificación de CPU diferentes. Para cada uno, explica su principio básico y discute al menos una ventaja y una desventaja.
    *   **Respuesta:**
        1.  **First-Come, First-Served (FCFS):** Los procesos se atienden en orden de llegada.
            *   **Ventaja:** Simple de implementar.
            *   **Desventaja:** "Efecto convoy", alto tiempo de espera promedio.
        2.  **Shortest Job Next (SJN) (no-expropiativo):** Se selecciona el proceso con la ráfaga de CPU más corta.
            *   **Ventaja:** Tiempo de espera promedio mínimo.
            *   **Desventaja:** Impracticable (se necesita conocer la ráfaga futura), puede causar inanición.

*   **Pregunta 6.2:** Considera el siguiente conjunto de procesos con sus tiempos de llegada y tiempos de ráfaga:
    *   P1: Tiempo de Llegada = 0 ms, Tiempo de Ráfaga = 5 ms
    *   P2: Tiempo de Llegada = 2 ms, Tiempo de Ráfaga = 3 ms
    *   P3: Tiempo de Llegada = 4 ms, Tiempo de Ráfaga = 2 ms
    Calcula el Tiempo de Espera Promedio y el Tiempo de Retorno Promedio para estos procesos si se planifican usando:
    *   **First-Come, First-Served (FCFS)**
    *   **Shortest Job Next (SJN)** (no-expropiativo)
    *   **Respuesta:**
        *   **FCFS:**
            *   Tiempo de Espera Promedio: **2.33 ms**
            *   Tiempo de Retorno Promedio: **5.67 ms**
        *   **SJN (no-expropiativo):**
            *   Tiempo de Espera Promedio: **2.00 ms**
            *   Tiempo de Retorno Promedio: **5.33 ms**

---

## Parte 2: Implementación Práctica (Python Resuelta)

### Objetivo

Implementar un programa en Python que simule una aplicación multi-hilo demostrando la concurrencia y la necesidad crítica de sincronización al tratar con recursos compartidos.

### Escenario

Simularemos la gestión de inventario de una tienda online simple. Múltiples hilos que representan "clientes" intentarán comprar artículos de un `inventory` compartido.

### Paso 2.1: Versión SIN Sincronización (Demostración de Condición de Carrera)

Este código muestra cómo pueden ocurrir condiciones de carrera cuando múltiples hilos acceden a un recurso compartido sin protección, lo que lleva a resultados incorrectos.

#### Código Python (Versión SIN Sincronización)

```python
import threading
import time
import random

# Inventario compartido (sin protección inicial)
# ¡ADVERTENCIA! Este inventario es global y será modificado por los hilos concurrentemente sin seguridad.
inventory = {"Laptop": 5, "Mouse": 10, "Keyboard": 7}

def customer_order_unsynchronized(customer_id, item, quantity):
    """
    Simula el intento de un cliente de comprar un artículo sin ninguna sincronización.
    """
    print(f"Cliente {customer_id}: Intentando comprar {quantity} de {item}...")
    time.sleep(random.uniform(0.01, 0.1)) # Simula un pequeño retraso de procesamiento

    # --- Sección Crítica sin protección ---
    if item in inventory and inventory[item] >= quantity:
        # Aquí es donde puede ocurrir la condición de carrera:
        # Múltiples hilos pueden leer el mismo valor de 'inventory[item]',
        # decidir que hay suficiente stock y proceder a deducir,
        # lo que lleva a un stock final incorrecto.
        inventory[item] -= quantity
        print(f"Cliente {customer_id}: Compra exitosa de {quantity} de {item}. Restante {item}: {inventory[item]}")
    else:
        print(f"Cliente {customer_id}: Falló la compra de {quantity} de {item}. Stock insuficiente o artículo no encontrado. Stock actual de {item}: {inventory.get(item, 0)}")
    # --- Fin de la Sección Crítica ---

def run_unsynchronized_simulation():
    global inventory # Asegurarse de que modificamos el inventario global
    inventory = {"Laptop": 5, "Mouse": 10, "Keyboard": 7} # Reinicia el inventario para esta simulación

    print("
" + "="*50)
    print("--- Versión SIN Sincronización ---")
    print("="*50)
    print("Inventario inicial:", inventory)

    threads = []
    # Clientes intentando comprar Laptops (stock inicial: 5)
    threads.append(threading.Thread(target=customer_order_unsynchronized, args=(1, "Laptop", 3)))
    threads.append(threading.Thread(target=customer_order_unsynchronized, args=(2, "Laptop", 4))) # Este debería causar un problema
    threads.append(threading.Thread(target=customer_order_unsynchronized, args=(3, "Laptop", 1)))
    # Otro cliente intentando Mouse
    threads.append(threading.Thread(target=customer_order_unsynchronized, args=(4, "Mouse", 6)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("
" + "="*50)
    print("--- Inventario Final (SIN Sincronización) ---")
    print("="*50)
    for item, quantity in inventory.items():
        print(f"{item}: {quantity}")
    print("
¡ATENCIÓN! Observe los posibles errores en el stock de 'Laptop' debido a la condición de carrera.")

```

#### Explicación de las Condiciones de Carrera (SIN Sincronización)

Una **condición de carrera** ocurre cuando la salida de un programa depende de la secuencia o la temporización de eventos incontrolables, como el *scheduling* de hilos. En este código, múltiples hilos pueden leer el valor de `inventory[item]`, decidir que hay suficiente stock y proceder a deducir la cantidad. Sin embargo, si el planificador de hilos interrumpe a un hilo después de leer el stock pero antes de actualizarlo, otro hilo podría leer el stock desactualizado, llevando a una deducción incorrecta y, en última instancia, a un inventario final inconsistente (incluso stock negativo). El comportamiento exacto varía en cada ejecución.

### Paso 2.2: Versión CON Sincronización (Resolución de Condiciones de Carrera)

Este código introduce un `threading.Lock` para proteger la sección crítica donde se accede y modifica el inventario. Esto garantiza que solo un hilo pueda ejecutar esa sección a la vez, eliminando las condiciones de carrera.

#### Código Python (Versión CON Sincronización)

```python
import threading
import time
import random

# Inventario compartido (para la versión sincronizada)
inventory_synchronized = {"Laptop": 5, "Mouse": 10, "Keyboard": 7}
# Objeto Lock para proteger el inventario compartido
inventory_lock = threading.Lock()

def customer_order_synchronized(customer_id, item, quantity):
    """
    Simula el intento de un cliente de comprar un artículo CON sincronización usando un Lock.
    """
    print(f"Cliente {customer_id}: Intentando comprar {quantity} de {item}...")
    time.sleep(random.uniform(0.01, 0.1)) # Simula un pequeño retraso de procesamiento

    # --- Sección Crítica Protegida por el Lock ---
    with inventory_lock: # Adquiere el lock, lo libera automáticamente al salir del bloque 'with'
        if item in inventory_synchronized and inventory_synchronized[item] >= quantity:
            inventory_synchronized[item] -= quantity
            print(f"Cliente {customer_id}: Compra exitosa de {quantity} de {item}. Restante {item}: {inventory_synchronized[item]}")
        else:
            print(f"Cliente {customer_id}: Falló la compra de {quantity} de {item}. Stock insuficiente o artículo no encontrado. Stock actual de {item}: {inventory_synchronized.get(item, 0)}")
    # --- Fin de la Sección Crítica ---

def run_synchronized_simulation():
    global inventory_synchronized # Asegurarse de que modificamos el inventario global
    inventory_synchronized = {"Laptop": 5, "Mouse": 10, "Keyboard": 7} # Reinicia el inventario para esta simulación

    print("

" + "="*50)
    print("--- Versión CON Sincronización ---")
    print("="*50)
    print("Inventario inicial:", inventory_synchronized)

    threads = []
    # Clientes intentando comprar Laptops (stock inicial: 5)
    threads.append(threading.Thread(target=customer_order_synchronized, args=(1, "Laptop", 3)))
    threads.append(threading.Thread(target=customer_order_synchronized, args=(2, "Laptop", 4))) # Este debería fallar, o al menos un pedido fallar
    threads.append(threading.Thread(target=customer_order_synchronized, args=(3, "Laptop", 1)))
    # Otro cliente intentando Mouse
    threads.append(threading.Thread(target=customer_order_synchronized, args=(4, "Mouse", 6)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("
" + "="*50)
    print("--- Inventario Final (CON Sincronización) ---")
    print("="*50)
    for item, quantity in inventory_synchronized.items():
        print(f"{item}: {quantity}")
    print("
¡CORRECTO! El stock de 'Laptop' es ahora consistente y sin errores gracias a la sincronización.")

```

#### Explicación de la Solución (CON Sincronización)

El objeto `threading.Lock` actúa como un mecanismo de **exclusión mutua**. Cuando un hilo adquiere el *lock* (mediante `with inventory_lock:`), se le otorga acceso exclusivo a la sección de código crítica que le sigue. Si otro hilo intenta adquirir el mismo *lock* mientras ya está en posesión de otro hilo, se bloqueará y esperará hasta que el *lock* sea liberado. Esto asegura que solo un hilo a la vez pueda ejecutar la sección crítica (verificación y modificación del inventario), eliminando así las condiciones de carrera y garantizando la integridad de los datos.

### Cómo Ejecutar el Código Python

1.  **Guarda el código:** Copia todo el código Python de las secciones "Versión SIN Sincronización" y "Versión CON Sincronización" en un solo archivo, por ejemplo, `concurrency_tutorial.py`.
2.  **Asegúrate de que las funciones de ejecución principal están habilitadas:** Al final del archivo, agrega:
    ```python
    if __name__ == "__main__":
        # Ejecutar primero la versión sin sincronización para observar el problema
        run_unsynchronized_simulation()

        # Luego, ejecutar la versión con sincronización para ver la solución
        run_synchronized_simulation()
    ```
    Estas líneas aseguran que ambas simulaciones se ejecutarán cuando ejecutes el archivo.
3.  **Ejecuta desde la terminal:** Abre una terminal o línea de comandos, navega hasta el directorio donde guardaste el archivo y ejecuta:
    ```bash
    python concurrency_tutorial.py
    ```
4.  **Observa la salida:** Compara los resultados de la simulación "SIN Sincronización" (donde el stock de `Laptop` probablemente será incorrecto) con los de la simulación "CON Sincronización" (donde el stock será siempre consistente y correcto).

---
