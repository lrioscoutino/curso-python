# Unidad 3: Administracion de Memoria

## Tutorial Teorico-Practico — Sistemas Operativos

**Herramientas**: Python 3, Terminal Linux

---

### Objetivos de aprendizaje

Al finalizar esta unidad el alumno sera capaz de:

1. Explicar las politicas y filosofias que guian la administracion de memoria en un SO.
2. Describir los esquemas de memoria real (particiones fijas y dinamicas).
3. Comprender la organizacion de memoria virtual (paginacion y segmentacion).
4. Analizar y comparar algoritmos de reemplazo de paginas.
5. Utilizar herramientas de Linux para observar el comportamiento real de la memoria.
6. Implementar simulaciones en Python de los algoritmos estudiados.

### Prerequisitos

- Python 3 instalado (`python3 --version`).
- Acceso a una terminal Linux (nativo, WSL o maquina virtual).
- Concepto general de proceso y espacio de direcciones.

---

## 3.1 Politica y filosofia

### 3.1.1 Teoria

La memoria principal (RAM) es un recurso **finito y compartido**. Multiples procesos compiten por ella simultaneamente, y el sistema operativo debe arbitrar el acceso de forma eficiente y segura.

Sin administracion de memoria:
- Un proceso podria leer o modificar datos de otro proceso.
- No seria posible ejecutar programas mas grandes que la memoria fisica disponible.
- La multiprogramacion seria inviable.

#### Objetivos de la administracion de memoria

| Objetivo | Descripcion |
|---|---|
| **Reubicacion** | Los procesos deben poder cargarse en cualquier posicion de memoria |
| **Proteccion** | Un proceso no debe acceder a la memoria de otro sin autorizacion |
| **Comparticion** | Procesos cooperativos deben poder compartir regiones de memoria de forma controlada |
| **Organizacion logica** | Separar codigo, datos y pila de cada proceso |
| **Organizacion fisica** | Gestionar la jerarquia de almacenamiento: registros, cache, RAM, disco |
| **Maximizar multiprogramacion** | Mantener el mayor numero posible de procesos en memoria |

#### Jerarquia de memoria

```
Velocidad alta                                  Capacidad alta
    |                                               |
    v                                               v
Registros  -->  Cache L1/L2/L3  -->  RAM  -->  Disco/SSD

 ~1 ns            ~5-20 ns         ~100 ns      ~10 ms
```

El SO se concentra en la gestion de **RAM** y su interaccion con **disco** (swap/memoria virtual).

#### Politicas fundamentales

1. **Fetch (traida)**: Cuando traer un bloque a memoria.
   - *Por demanda*: solo cuando se necesita (lo mas comun).
   - *Por anticipacion* (prefetch): antes de que se necesite.

2. **Placement (colocacion)**: Donde colocar el bloque en memoria.
   - First Fit, Best Fit, Worst Fit, Next Fit.

3. **Replacement (reemplazo)**: Que bloque sacar cuando no hay espacio.
   - FIFO, LRU, Optimo, Clock.

### 3.1.2 Practica Linux: Observar la memoria del sistema

```bash
# Resumen de memoria del sistema en formato legible
free -h
```

Salida tipica:

```
               total        used        free      shared  buff/cache   available
Mem:           15Gi        6.2Gi       2.1Gi       512Mi        7.1Gi       8.5Gi
Swap:          2.0Gi       128Mi       1.9Gi
```

- **total**: Memoria fisica instalada.
- **used**: Memoria utilizada por procesos.
- **buff/cache**: Memoria usada por el kernel como cache de disco (se puede liberar si se necesita).
- **available**: Estimacion de cuanta memoria esta realmente disponible para nuevos procesos.
- **Swap**: Espacio en disco que actua como extension de la RAM.

```bash
# Informacion detallada del kernel
head -20 /proc/meminfo
```

Campos importantes: `MemTotal`, `MemFree`, `MemAvailable`, `Buffers`, `Cached`, `SwapTotal`, `SwapFree`.

**Preguntas para reflexionar:**
- Cuanta RAM total tiene tu sistema?
- Cuanta esta libre y cuanta en buff/cache?
- Cuanto swap hay configurado y cuanto se esta usando?

### 3.1.3 Practica Python: Simulacion de politicas de asignacion

Este script simula tres politicas de asignacion de bloques de memoria: **First Fit**, **Best Fit** y **Worst Fit**.

```python
#!/usr/bin/env python3
"""
Simulacion de politicas de asignacion de memoria.
Compara First Fit, Best Fit y Worst Fit.

Ejecutar: python3 politicas_asignacion.py
"""


def first_fit(bloques, proceso):
    """Asigna al primer bloque suficientemente grande."""
    for i, bloque in enumerate(bloques):
        if bloque >= proceso:
            return i
    return -1


def best_fit(bloques, proceso):
    """Asigna al bloque mas pequeno que sea suficiente."""
    mejor = -1
    menor_desperdicio = float('inf')
    for i, bloque in enumerate(bloques):
        if bloque >= proceso:
            desperdicio = bloque - proceso
            if desperdicio < menor_desperdicio:
                menor_desperdicio = desperdicio
                mejor = i
    return mejor


def worst_fit(bloques, proceso):
    """Asigna al bloque mas grande disponible."""
    peor = -1
    mayor_tamano = -1
    for i, bloque in enumerate(bloques):
        if bloque >= proceso:
            if bloque > mayor_tamano:
                mayor_tamano = bloque
                peor = i
    return peor


def simular(nombre, funcion, bloques_originales, procesos):
    """Ejecuta la simulacion de una politica."""
    bloques = list(bloques_originales)  # copia
    print(f"\n{'=' * 55}")
    print(f"  Politica: {nombre}")
    print(f"{'=' * 55}")
    print(f"  Bloques iniciales: {bloques}")
    print(f"  Procesos a asignar: {procesos}")
    print(f"{'-' * 55}")

    asignaciones = 0
    frag_interna_total = 0

    for proc in procesos:
        idx = funcion(bloques, proc)
        if idx != -1:
            desperdicio = bloques[idx] - proc
            frag_interna_total += desperdicio
            print(f"  Proceso {proc:>4} KB -> Bloque[{idx}] ({bloques[idx]} KB)"
                  f"  | Fragmentacion interna: {desperdicio} KB")
            bloques[idx] -= proc  # espacio restante
            asignaciones += 1
        else:
            print(f"  Proceso {proc:>4} KB -> SIN ESPACIO")

    print(f"{'-' * 55}")
    print(f"  Asignaciones exitosas: {asignaciones}/{len(procesos)}")
    print(f"  Fragmentacion interna total: {frag_interna_total} KB")
    print(f"  Bloques restantes: {bloques}")


def main():
    # Bloques de memoria disponibles (en KB)
    bloques = [100, 500, 200, 300, 600]

    # Procesos solicitando memoria (en KB)
    procesos = [212, 417, 112, 426]

    for nombre, funcion in [("First Fit", first_fit),
                            ("Best Fit", best_fit),
                            ("Worst Fit", worst_fit)]:
        simular(nombre, funcion, bloques, procesos)


if __name__ == "__main__":
    main()
```

**Preguntas de reflexion:**
1. Cual politica logro asignar mas procesos?
2. Cual genero menos fragmentacion interna total?
3. En que escenarios podria ser preferible Worst Fit sobre Best Fit?

---

## 3.2 Memoria real

### 3.2.1 Teoria

#### Particiones fijas (estaticas)

La memoria se divide en bloques de tamano fijo al iniciar el sistema:

```
+----------+----------+----------+----------+
|  Part 1  |  Part 2  |  Part 3  |  Part 4  |
|  64 KB   | 128 KB   | 256 KB   | 512 KB   |
+----------+----------+----------+----------+
```

- **Fragmentacion interna**: Un proceso de 50 KB en una particion de 64 KB desperdicia 14 KB.
- Ventaja: implementacion simple, overhead minimo.
- Desventaja: numero y tamano de procesos limitado por las particiones.

#### Particiones dinamicas (variables)

Las particiones se crean al tamano exacto del proceso:

```
Antes:     [  P1 (100KB)  ][   Libre (200KB)  ][  P2 (150KB)  ]
Despues:   [  P1 (100KB)  ][ P3 (80KB) ][ Libre 120KB ][  P2 (150KB)  ]
```

- **Fragmentacion externa**: huecos libres no contiguos que en total serian suficientes pero individualmente no.
- Solucion: **compactacion** (mover procesos para unir huecos — costosa en tiempo).

#### Fragmentacion: interna vs externa

| Tipo | Causa | Donde ocurre | Solucion |
|---|---|---|---|
| **Interna** | Espacio sobrante dentro de una particion asignada | Particiones fijas, paginacion | Ajustar tamanos |
| **Externa** | Huecos dispersos entre particiones ocupadas | Particiones dinamicas, segmentacion | Compactacion, paginacion |

#### Algoritmos de colocacion

| Algoritmo | Descripcion | Pros | Contras |
|---|---|---|---|
| **First Fit** | Primer hueco suficiente | Rapido | Fragmenta el inicio de la memoria |
| **Best Fit** | Hueco mas pequeno que alcance | Menor desperdicio inmediato | Genera huecos diminutos e inutiles |
| **Worst Fit** | Hueco mas grande | Deja huecos grandes potencialmente utiles | Consume los bloques mas grandes |
| **Next Fit** | Como First Fit, pero continua desde la ultima posicion | Distribuye mejor la fragmentacion | Puede ser peor que First Fit |

#### Estructuras de control: bitmap y listas enlazadas

**Bitmap (mapa de bits):**
- La memoria se divide en unidades de asignacion. Cada unidad se representa con un bit: `1` = ocupada, `0` = libre.
- Ejemplo: `11110000 11100000` (4 ocupadas, 4 libres, 3 ocupadas, 5 libres).
- Busqueda lenta (hay que encontrar secuencias de ceros), pero representacion compacta.

**Lista enlazada:**
- Cada nodo describe un segmento: `(tipo, inicio, tamano)` donde tipo es "proceso" o "hueco".
- Facilita la busqueda y fusion de huecos adyacentes.

### 3.2.2 Practica Linux: Sistema buddy y mapeo de procesos

```bash
# Sistema buddy de Linux: bloques libres por orden de tamano
cat /proc/buddyinfo
```

Salida tipica:

```
Node 0, zone   Normal   1024   512   256   128    64    32    16     8     4     2     1
```

Cada columna indica cuantos bloques libres hay de tamano 2^n paginas (4KB, 8KB, 16KB, ...). El sistema buddy divide y fusiona bloques en potencias de 2.

```bash
# Mapeo de memoria de un proceso (PID de tu shell actual)
pmap -x $$

# O directamente desde /proc
head -20 /proc/$$/maps
```

La salida muestra cada region de memoria: direccion, tamano, permisos y que la respalda (archivo, heap, stack, etc).

### 3.2.3 Practica Python: Simulador de particiones dinamicas

```python
#!/usr/bin/env python3
"""
Simulador de particiones dinamicas con visualizacion ASCII.
Muestra la fragmentacion conforme se asignan y liberan procesos.

Ejecutar: python3 particiones_dinamicas.py
"""


class Bloque:
    def __init__(self, inicio, tamano, proceso=None):
        self.inicio = inicio
        self.tamano = tamano
        self.proceso = proceso  # None = hueco libre

    @property
    def libre(self):
        return self.proceso is None


class MemoriaDinamica:
    ANCHO_VISUAL = 60

    def __init__(self, tamano_total):
        self.tamano_total = tamano_total
        self.bloques = [Bloque(0, tamano_total)]

    def asignar(self, nombre_proceso, tamano, politica="first_fit"):
        """Asigna memoria a un proceso usando la politica indicada."""
        idx = self._buscar_hueco(tamano, politica)
        if idx == -1:
            print(f"  ERROR: No hay espacio para '{nombre_proceso}' ({tamano} KB)")
            return False

        bloque = self.bloques[idx]
        if bloque.tamano == tamano:
            bloque.proceso = nombre_proceso
        else:
            nuevo_libre = Bloque(bloque.inicio + tamano,
                                 bloque.tamano - tamano)
            bloque.tamano = tamano
            bloque.proceso = nombre_proceso
            self.bloques.insert(idx + 1, nuevo_libre)

        print(f"  OK: '{nombre_proceso}' asignado ({tamano} KB)"
              f" en posicion {bloque.inicio}")
        return True

    def liberar(self, nombre_proceso):
        """Libera la memoria de un proceso y fusiona huecos adyacentes."""
        for bloque in self.bloques:
            if bloque.proceso == nombre_proceso:
                bloque.proceso = None
                print(f"  OK: '{nombre_proceso}' liberado ({bloque.tamano} KB)")
                self._fusionar_huecos()
                return True
        print(f"  ERROR: Proceso '{nombre_proceso}' no encontrado")
        return False

    def _buscar_hueco(self, tamano, politica):
        if politica == "first_fit":
            for i, b in enumerate(self.bloques):
                if b.libre and b.tamano >= tamano:
                    return i
        elif politica == "best_fit":
            mejor, menor = -1, float('inf')
            for i, b in enumerate(self.bloques):
                if b.libre and b.tamano >= tamano and b.tamano - tamano < menor:
                    menor = b.tamano - tamano
                    mejor = i
            return mejor
        elif politica == "worst_fit":
            peor, mayor = -1, -1
            for i, b in enumerate(self.bloques):
                if b.libre and b.tamano >= tamano and b.tamano > mayor:
                    mayor = b.tamano
                    peor = i
            return peor
        return -1

    def _fusionar_huecos(self):
        i = 0
        while i < len(self.bloques) - 1:
            actual = self.bloques[i]
            siguiente = self.bloques[i + 1]
            if actual.libre and siguiente.libre:
                actual.tamano += siguiente.tamano
                self.bloques.pop(i + 1)
            else:
                i += 1

    def mostrar(self):
        """Muestra el estado de la memoria con visualizacion ASCII."""
        print(f"\n  {'=' * (self.ANCHO_VISUAL + 22)}")
        print(f"  Memoria total: {self.tamano_total} KB")
        print(f"  {'-' * (self.ANCHO_VISUAL + 22)}")

        for bloque in self.bloques:
            ancho = max(1, int(bloque.tamano / self.tamano_total
                               * self.ANCHO_VISUAL))
            if bloque.libre:
                barra = '.' * ancho
                etiqueta = "LIBRE"
            else:
                barra = '#' * ancho
                etiqueta = bloque.proceso
            print(f"  |{barra:<{self.ANCHO_VISUAL}}|"
                  f" {bloque.tamano:>4} KB  {etiqueta}")

        libre = sum(b.tamano for b in self.bloques if b.libre)
        huecos = sum(1 for b in self.bloques if b.libre)
        hueco_max = max((b.tamano for b in self.bloques if b.libre),
                        default=0)
        print(f"  {'-' * (self.ANCHO_VISUAL + 22)}")
        print(f"  Libre total: {libre} KB | Huecos: {huecos}"
              f" | Hueco maximo: {hueco_max} KB")
        if huecos > 1:
            print(f"  Fragmentacion externa: {huecos} huecos dispersos"
                  f" (libre total {libre} KB pero hueco maximo solo"
                  f" {hueco_max} KB)")
        print(f"  {'=' * (self.ANCHO_VISUAL + 22)}")


def main():
    print("SIMULADOR DE PARTICIONES DINAMICAS")
    print("Politica: First Fit\n")

    mem = MemoriaDinamica(1024)

    # Fase 1: Asignar procesos
    print("--- Fase 1: Asignacion inicial ---")
    mem.asignar("P1", 200)
    mem.asignar("P2", 150)
    mem.asignar("P3", 300)
    mem.asignar("P4", 100)
    mem.mostrar()

    # Fase 2: Liberar algunos procesos (crear huecos)
    print("\n--- Fase 2: Liberar P2 y P4 (crear huecos) ---")
    mem.liberar("P2")
    mem.liberar("P4")
    mem.mostrar()

    # Fase 3: Intentar nuevas asignaciones
    print("\n--- Fase 3: Nuevas asignaciones ---")
    mem.asignar("P5", 120)  # Entra en el hueco de P2? (150 KB)
    mem.asignar("P6", 200)  # Puede entrar en algun hueco?
    mem.mostrar()


if __name__ == "__main__":
    main()
```

**Observa:**
- Como se fragmenta la memoria al liberar procesos intermedios.
- Como los huecos adyacentes se fusionan automaticamente.
- Como la fragmentacion externa puede impedir asignar un proceso grande aunque haya suficiente espacio libre total.

---

## 3.3 Organizacion de memoria virtual

### 3.3.1 Teoria

La memoria virtual crea una **abstraccion**: cada proceso cree tener toda la memoria para si mismo, aunque fisicamente comparte la RAM con otros procesos.

```
  Proceso A             Proceso B              Memoria Fisica
 +---------+          +---------+             +-------------+
 | Pagina 0|---+      | Pagina 0|------+      | Marco 0     |
 | Pagina 1|---+-+--> | Pagina 1|--+   +----> | Marco 1     |
 | Pagina 2|   | |    | Pagina 2|  |          | Marco 2     |
 | Pagina 3|   | |    +---------+  +--------> | Marco 3     |
 +---------+   | +-------------------------> | Marco 4     |
               +----------------------------> | Marco 5     |
                                              +-------------+
```

**Beneficios:**
- Cada proceso tiene su propio espacio de direcciones aislado (proteccion).
- Se puede ejecutar programas mas grandes que la memoria fisica.
- Facilita la comparticion de paginas entre procesos (ej. bibliotecas).
- Simplifica la carga de programas (no necesitan direcciones contiguas en RAM).

#### Paginacion

La memoria virtual y la fisica se dividen en bloques de tamano fijo:
- **Pagina**: bloque en el espacio virtual (tipicamente 4 KB).
- **Marco (frame)**: bloque en la memoria fisica.
- **Tabla de paginas**: estructura que mapea pagina virtual -> marco fisico.

**Traduccion de direcciones:**

```
Direccion virtual (32 bits, paginas de 4 KB):
+--------------------+------------------+
|  Numero de pagina  |  Desplazamiento  |
|    (20 bits)       |    (12 bits)     |
+--------------------+------------------+

Ejemplo con paginas de 4 KB (4096 = 2^12 bytes):
  Direccion virtual: 8196
  8196 / 4096 = pagina 2, desplazamiento 4
  Si tabla dice pagina 2 -> marco 5:
  Direccion fisica = (5 * 4096) + 4 = 20484
```

**Tabla de paginas:**

| Pagina Virtual | Marco Fisico | Bit de Validez | Proteccion |
|:-:|:-:|:-:|:-:|
| 0 | 3 | 1 | R/W |
| 1 | — | 0 | — |
| 2 | 5 | 1 | R |
| 3 | 1 | 1 | R/W |

- **Bit de validez**: 1 = pagina en memoria fisica; 0 = en disco (genera fallo de pagina).
- **Proteccion**: permisos de lectura (R), escritura (W), ejecucion (X).

#### TLB (Translation Lookaside Buffer)

Consultar la tabla de paginas en cada acceso a memoria duplicaria el tiempo. El **TLB** es una cache de hardware que almacena traducciones recientes.

```
CPU genera direccion virtual
         |
         v
    +----------+
    |   TLB    |--- Hit  ---> Marco fisico (rapido, ~1 ciclo)
    +----------+
         |
       Miss
         |
         v
  Tabla de paginas ---> Marco fisico (lento, acceso a memoria)
         |
    Actualizar TLB
```

El TLB tiene tipicamente 64-1024 entradas y una tasa de acierto > 99%.

#### Tablas de paginas multinivel

Con direcciones de 32 bits y paginas de 4 KB, la tabla tendria 2^20 = ~1 millon de entradas (~4 MB por proceso). Solucion: tablas multinivel.

```
Direccion virtual (32 bits, 2 niveles):
+----------+----------+------------------+
| Indice 1 | Indice 2 |  Desplazamiento  |
| (10 bits)| (10 bits)|    (12 bits)     |
+----------+----------+------------------+
     |           |
     v           v
  Tabla      Tabla de         Marco
  nivel 1    nivel 2   --->   fisico + desplazamiento
```

Solo se crean las tablas de segundo nivel que realmente se necesitan. En x86-64 se usan 4 niveles.

#### Segmentacion

Divide el espacio de direcciones segun la **estructura logica** del programa:

| Segmento | Contenido |
|---|---|
| Codigo (text) | Instrucciones del programa |
| Datos | Variables globales |
| Heap | Memoria dinamica (malloc) |
| Pila (stack) | Variables locales, llamadas a funciones |

Cada segmento tiene su propia base y limite. Una direccion es: `(numero_segmento, desplazamiento)`.

- Ventaja: refleja la estructura logica del programa.
- Desventaja: fragmentacion externa (segmentos de tamano variable).

#### Segmentacion paginada

Combina ambos: el espacio virtual se divide en segmentos (estructura logica), y cada segmento se divide internamente en paginas (elimina fragmentacion externa). Linux simplifica esto usando segmentacion plana + paginacion.

### 3.3.2 Practica Linux: Examinar la memoria virtual de un proceso

```bash
# Ver el mapeo virtual de tu shell actual
cat /proc/$$/maps
```

Salida tipica (simplificada):

```
55a3b2000000-55a3b2028000 r--p  /usr/bin/bash    <- codigo (solo lectura)
55a3b2028000-55a3b2118000 r-xp  /usr/bin/bash    <- codigo (ejecutable)
55a3b2300000-55a3b2380000 rw-p  [heap]           <- heap
7f8a12000000-7f8a12200000 r--p  /usr/lib/libc.so <- biblioteca compartida
7ffd4a700000-7ffd4a722000 rw-p  [stack]          <- pila
```

Cada linea muestra: rango de direcciones virtuales, permisos (`r`=read, `w`=write, `x`=execute, `p`=private), y que la respalda.

```bash
# Tamano de pagina del sistema (tipicamente 4096 = 4 KB)
getconf PAGE_SIZE
```

### 3.3.3 Practica Python: Simulador de traduccion de direcciones

```python
#!/usr/bin/env python3
"""
Simulador de traduccion de direcciones virtuales a fisicas.
Demuestra paginacion con tabla de paginas y TLB.

Ejecutar: python3 traduccion_direcciones.py
"""

import random


class TLB:
    """Simula un Translation Lookaside Buffer con reemplazo LRU."""

    def __init__(self, capacidad=4):
        self.capacidad = capacidad
        self.entradas = []  # lista de (pagina, marco), mas reciente al final
        self.hits = 0
        self.misses = 0

    def buscar(self, pagina):
        for i, (pag, marco) in enumerate(self.entradas):
            if pag == pagina:
                self.hits += 1
                self.entradas.append(self.entradas.pop(i))
                return marco
        self.misses += 1
        return None

    def insertar(self, pagina, marco):
        self.entradas = [(p, m) for p, m in self.entradas if p != pagina]
        if len(self.entradas) >= self.capacidad:
            self.entradas.pop(0)  # LRU: eliminar la menos reciente
        self.entradas.append((pagina, marco))


class SimuladorPaginacion:
    """Simula un sistema de paginacion con tabla de paginas y TLB."""

    def __init__(self, tam_pagina=4096, num_paginas=16,
                 num_marcos=8, tlb_capacidad=4):
        self.tam_pagina = tam_pagina
        self.bits_offset = tam_pagina.bit_length() - 1
        self.num_paginas = num_paginas
        self.num_marcos = num_marcos
        self.tlb = TLB(tlb_capacidad)

        # Crear tabla de paginas (algunas paginas en RAM, otras no)
        marcos_disponibles = list(range(num_marcos))
        random.shuffle(marcos_disponibles)

        self.tabla = []
        for i in range(num_paginas):
            if marcos_disponibles and random.random() < 0.7:
                self.tabla.append({
                    'marco': marcos_disponibles.pop(0),
                    'valida': True,
                    'proteccion': random.choice(['R', 'R/W', 'R/X']),
                })
            else:
                self.tabla.append({
                    'marco': None,
                    'valida': False,
                    'proteccion': None,
                })

    def traducir(self, direccion_virtual):
        """Traduce una direccion virtual a fisica."""
        num_pagina = direccion_virtual >> self.bits_offset
        desplazamiento = direccion_virtual & (self.tam_pagina - 1)

        print(f"\n  Direccion virtual: {direccion_virtual}"
              f" (0x{direccion_virtual:08X})")
        print(f"  -> Numero de pagina: {num_pagina}")
        print(f"  -> Desplazamiento:   {desplazamiento}"
              f" (0x{desplazamiento:03X})")

        if num_pagina >= self.num_paginas:
            print(f"  -> ERROR: Pagina {num_pagina} fuera de rango"
                  f" (max: {self.num_paginas - 1})")
            return None

        # Paso 1: Buscar en TLB
        marco = self.tlb.buscar(num_pagina)
        if marco is not None:
            dir_fisica = (marco << self.bits_offset) | desplazamiento
            print(f"  -> TLB HIT! Marco: {marco}")
            print(f"  -> Direccion fisica: {dir_fisica}"
                  f" (0x{dir_fisica:08X})")
            return dir_fisica

        # Paso 2: Buscar en tabla de paginas (TLB miss)
        print(f"  -> TLB MISS. Consultando tabla de paginas...")
        entrada = self.tabla[num_pagina]

        if not entrada['valida']:
            print(f"  -> FALLO DE PAGINA: Pagina {num_pagina}"
                  f" no esta en memoria fisica")
            return None

        marco = entrada['marco']
        self.tlb.insertar(num_pagina, marco)
        dir_fisica = (marco << self.bits_offset) | desplazamiento

        print(f"  -> Marco fisico: {marco}"
              f" | Proteccion: {entrada['proteccion']}")
        print(f"  -> Direccion fisica: {dir_fisica}"
              f" (0x{dir_fisica:08X})")
        print(f"  -> TLB actualizado")
        return dir_fisica

    def mostrar_tabla(self):
        """Muestra la tabla de paginas completa."""
        print(f"\n  {'Pagina':>8} | {'Marco':>8} | {'Valida':>8}"
              f" | {'Proteccion':>12}")
        print(f"  {'-' * 8}-+-{'-' * 8}-+-{'-' * 8}-+-{'-' * 12}")
        for i, entrada in enumerate(self.tabla):
            marco = str(entrada['marco']) if entrada['valida'] else "---"
            valida = "Si" if entrada['valida'] else "No"
            prot = entrada['proteccion'] if entrada['proteccion'] else "---"
            print(f"  {i:>8} | {marco:>8} | {valida:>8} | {prot:>12}")


def main():
    random.seed(42)  # Semilla fija para resultados reproducibles

    print("SIMULADOR DE TRADUCCION DE DIRECCIONES")
    print(f"Tamano de pagina: 4096 bytes (4 KB)")
    print(f"Paginas virtuales: 16 | Marcos fisicos: 8 | TLB: 4 entradas")

    sim = SimuladorPaginacion(
        tam_pagina=4096,
        num_paginas=16,
        num_marcos=8,
        tlb_capacidad=4,
    )

    print("\nTABLA DE PAGINAS:")
    sim.mostrar_tabla()

    # Traducir varias direcciones
    print("\n" + "=" * 55)
    print("TRADUCCIONES:")
    print("=" * 55)

    direcciones = [
        0,              # Inicio de pagina 0
        4096,           # Inicio de pagina 1
        8192 + 100,     # Pagina 2, desplazamiento 100
        4096 * 5 + 2048,  # Pagina 5, desplazamiento 2048
        100,            # Pagina 0 de nuevo (deberia ser TLB hit)
        4096 * 15 + 10, # Pagina 15
    ]

    for dir_virtual in direcciones:
        sim.traducir(dir_virtual)

    # Estadisticas del TLB
    print(f"\n{'=' * 55}")
    print("ESTADISTICAS DEL TLB:")
    print(f"  Aciertos (hits):  {sim.tlb.hits}")
    print(f"  Fallos (misses):  {sim.tlb.misses}")
    total = sim.tlb.hits + sim.tlb.misses
    tasa = sim.tlb.hits / total * 100 if total > 0 else 0
    print(f"  Tasa de acierto:  {tasa:.1f}%")


if __name__ == "__main__":
    main()
```

**Ejercicio:** Agrega mas direcciones de acceso y observa como mejora la tasa de acierto del TLB con patrones de localidad (accesos repetidos a las mismas paginas).

---

## 3.4 Administracion de memoria virtual

### 3.4.1 Teoria

#### Demanda de paginas (Demand Paging)

En lugar de cargar todo el programa en memoria al inicio, el SO carga paginas **solo cuando se necesitan**. Esto se llama paginacion por demanda.

```
1. CPU genera direccion virtual
2. Consultar TLB
   - Hit: acceso directo al marco fisico
   - Miss: consultar tabla de paginas
3. Consultar tabla de paginas
   - Bit de validez = 1: pagina en memoria, actualizar TLB
   - Bit de validez = 0: FALLO DE PAGINA
4. Fallo de pagina:
   a. Trap al sistema operativo
   b. Encontrar la pagina en disco (swap)
   c. Encontrar un marco libre (o elegir victima)
   d. Cargar pagina de disco a RAM
   e. Actualizar tabla de paginas y TLB
   f. Reiniciar la instruccion que fallo
```

#### Costo de un fallo de pagina

Un fallo de pagina **no es un error**, es el mecanismo normal de la paginacion por demanda. Sin embargo, son costosos:

- Acceso a memoria: ~100 nanosegundos
- Fallo de pagina (acceso a disco): ~10 milisegundos (**100,000 veces mas lento**)

Por eso es critico minimizar la tasa de fallos de pagina.

#### Algoritmos de reemplazo de paginas

Cuando ocurre un fallo de pagina y no hay marcos libres, el SO debe elegir una pagina victima para expulsar:

**FIFO (First In, First Out):**
- Reemplaza la pagina que lleva mas tiempo en memoria.
- Simple de implementar (cola).
- Problema: puede expulsar paginas muy usadas. Sufre la **anomalia de Belady**.

**LRU (Least Recently Used):**
- Reemplaza la pagina que no ha sido usada por mas tiempo.
- Buena aproximacion al optimo.
- Costoso de implementar exactamente (requiere timestamp en cada acceso).

**Optimo (OPT / MIN):**
- Reemplaza la pagina que tardara mas en volver a ser usada.
- **Imposible de implementar** (requiere conocer el futuro).
- Sirve como cota inferior teorica para evaluar otros algoritmos.

**Clock (Segunda Oportunidad):**
- Aproximacion eficiente de LRU.
- Cada pagina tiene un **bit de referencia** (R).
- Paginas en un buffer circular. Al buscar victima:
  - Si R = 1: dar segunda oportunidad (R = 0), avanzar.
  - Si R = 0: elegirla como victima.

```
        Manecilla
           |
           v
    +---+---+---+---+---+---+
    | 1 | 0 | 1 | 1 | 0 | 1 |   <- Bits de referencia
    +---+---+---+---+---+---+
     P0   P1  P2  P3  P4  P5

    Buscar victima:
    P0: R=1 -> R=0, avanzar
    P1: R=0 -> VICTIMA! Reemplazar P1
```

#### Anomalia de Belady

Con FIFO, **mas marcos no siempre significa menos fallos**:

```
Secuencia: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5

Con 3 marcos:  9 fallos
Con 4 marcos: 10 fallos  <-- MAS fallos con MAS marcos!
```

LRU y Optimo son "algoritmos de pila" y nunca sufren esta anomalia.

#### Working Set y Thrashing

**Working Set (conjunto de trabajo):**
- Es el conjunto de paginas que un proceso esta usando activamente en un intervalo de tiempo dado.
- Si el proceso tiene en memoria todas las paginas de su working set, genera pocos fallos.

**Thrashing (hiperpaginacion):**
- Ocurre cuando el sistema gasta mas tiempo manejando fallos de pagina que ejecutando instrucciones utiles.
- Causa: demasiados procesos compiten por pocos marcos.
- Sintoma: uso de CPU muy bajo, disco swap muy activo.
- Solucion: reducir el grado de multiprogramacion (suspender procesos).

```
  Uso de CPU
      ^
      |        /----\
      |       /      \
      |      /        \
      |     /          \___________ Thrashing
      |    /
      |   /
      +-------------------------------> Grado de multiprogramacion
```

### 3.4.2 Practica Linux: Observar fallos de pagina en tiempo real

```bash
# vmstat: estadisticas de memoria virtual (cada 2 segundos, 10 muestras)
vmstat 2 10
```

Campos relevantes de `vmstat`:

| Campo | Descripcion |
|---|---|
| `si` | Swap in: KB leidos desde swap (paginas traidas a RAM) |
| `so` | Swap out: KB escritos a swap (paginas expulsadas de RAM) |
| `bi` | Block in: bloques leidos de disco |
| `bo` | Block out: bloques escritos a disco |

Si `si` y `so` son consistentemente altos, el sistema puede estar en thrashing.

```bash
# Contadores acumulados de fallos de pagina del kernel
grep -E "pgfault|pgmajfault" /proc/vmstat
# pgfault = fallos totales (menores + mayores)
# pgmajfault = fallos mayores (requirieron acceso a disco)

# Fallos de pagina de un proceso especifico
ps -o pid,min_flt,maj_flt -p $$
# min_flt = fallos menores (pagina en RAM pero sin mapear)
# maj_flt = fallos mayores (pagina en disco)
```

### 3.4.3 Practica Python: Comparador de algoritmos de reemplazo

```python
#!/usr/bin/env python3
"""
Simulador comparativo de algoritmos de reemplazo de paginas.
Implementa FIFO, LRU, Optimo y Clock.
Demuestra la anomalia de Belady.

Ejecutar: python3 algoritmos_reemplazo.py
"""

from collections import deque


def fifo(secuencia, num_marcos):
    """Algoritmo FIFO: reemplaza la pagina que llego primero."""
    marcos = []
    cola = deque()
    fallos = 0
    historial = []

    for pagina in secuencia:
        if pagina in marcos:
            historial.append((pagina, list(marcos), False))
        else:
            fallos += 1
            if len(marcos) < num_marcos:
                marcos.append(pagina)
                cola.append(pagina)
            else:
                victima = cola.popleft()
                idx = marcos.index(victima)
                marcos[idx] = pagina
                cola.append(pagina)
            historial.append((pagina, list(marcos), True))

    return fallos, historial


def lru(secuencia, num_marcos):
    """Algoritmo LRU: reemplaza la pagina menos recientemente usada."""
    marcos = []
    uso_reciente = []  # orden de uso, mas reciente al final
    fallos = 0
    historial = []

    for pagina in secuencia:
        if pagina in marcos:
            uso_reciente.remove(pagina)
            uso_reciente.append(pagina)
            historial.append((pagina, list(marcos), False))
        else:
            fallos += 1
            if len(marcos) < num_marcos:
                marcos.append(pagina)
            else:
                victima = uso_reciente.pop(0)
                idx = marcos.index(victima)
                marcos[idx] = pagina
            uso_reciente.append(pagina)
            historial.append((pagina, list(marcos), True))

    return fallos, historial


def optimo(secuencia, num_marcos):
    """Algoritmo Optimo: reemplaza la que tardara mas en usarse."""
    marcos = []
    fallos = 0
    historial = []

    for i, pagina in enumerate(secuencia):
        if pagina in marcos:
            historial.append((pagina, list(marcos), False))
        else:
            fallos += 1
            if len(marcos) < num_marcos:
                marcos.append(pagina)
            else:
                futuro = secuencia[i + 1:]
                mas_lejano = -1
                victima_idx = 0
                for j, m in enumerate(marcos):
                    if m not in futuro:
                        victima_idx = j
                        break
                    prox_uso = futuro.index(m)
                    if prox_uso > mas_lejano:
                        mas_lejano = prox_uso
                        victima_idx = j
                marcos[victima_idx] = pagina
            historial.append((pagina, list(marcos), True))

    return fallos, historial


def clock(secuencia, num_marcos):
    """Algoritmo Clock (Segunda Oportunidad)."""
    marcos = [None] * num_marcos
    bits_ref = [0] * num_marcos
    manecilla = 0
    ocupados = 0
    fallos = 0
    historial = []

    for pagina in secuencia:
        # Verificar si la pagina ya esta en memoria
        paginas_actuales = marcos[:ocupados]
        if pagina in paginas_actuales:
            idx = marcos.index(pagina)
            bits_ref[idx] = 1
            historial.append((pagina, list(paginas_actuales), False))
        else:
            fallos += 1
            if ocupados < num_marcos:
                marcos[ocupados] = pagina
                bits_ref[ocupados] = 1
                ocupados += 1
            else:
                while bits_ref[manecilla] == 1:
                    bits_ref[manecilla] = 0
                    manecilla = (manecilla + 1) % num_marcos
                marcos[manecilla] = pagina
                bits_ref[manecilla] = 1
                manecilla = (manecilla + 1) % num_marcos
            historial.append((pagina, list(marcos[:ocupados]), True))

    return fallos, historial


def mostrar_historial(nombre, secuencia, fallos, historial, num_marcos):
    """Muestra el historial paso a paso de un algoritmo."""
    total = len(secuencia)
    tasa = fallos / total * 100

    print(f"\n{'=' * 60}")
    print(f"  {nombre}")
    print(f"{'=' * 60}")
    print(f"  {'Ref':>5} | {'Marcos':>30} | {'Fallo':>7}")
    print(f"  {'-' * 5}-+-{'-' * 30}-+-{'-' * 7}")

    for pagina, marcos, fallo in historial:
        marcos_str = str(marcos)
        marca = " *" if fallo else ""
        print(f"  {pagina:>5} | {marcos_str:>30} | {marca:>7}")

    print(f"  {'-' * 50}")
    print(f"  Fallos: {fallos}/{total} ({tasa:.1f}%)"
          f"  |  Aciertos: {total - fallos}/{total}"
          f" ({100 - tasa:.1f}%)")


def demostrar_anomalia_belady():
    """Demuestra la anomalia de Belady con FIFO."""
    secuencia = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

    print(f"\n{'=' * 60}")
    print("  ANOMALIA DE BELADY (FIFO)")
    print(f"{'=' * 60}")
    print(f"  Secuencia: {secuencia}\n")
    print(f"  {'Marcos':>8} | {'Fallos':>8} | {'Tasa':>8} |")
    print(f"  {'-' * 8}-+-{'-' * 8}-+-{'-' * 8}-+")

    fallos_previo = 0
    for m in range(2, 7):
        f, _ = fifo(secuencia, m)
        anomalia = "  <-- ANOMALIA!" if f > fallos_previo and m > 2 else ""
        tasa = f / len(secuencia) * 100
        print(f"  {m:>8} | {f:>8} | {tasa:>7.1f}% |{anomalia}")
        fallos_previo = f

    print(f"\n  Nota: Al pasar de 3 a 4 marcos, FIFO produce MAS fallos.")
    print(f"  Esto NO ocurre con LRU ni Optimo (algoritmos de pila).")


def main():
    # Cadena de referencias clasica (Silberschatz/Tanenbaum)
    secuencia = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    num_marcos = 3

    print("SIMULADOR COMPARATIVO DE ALGORITMOS DE REEMPLAZO")
    print(f"\n  Cadena de referencias: {secuencia}")
    print(f"  Numero de marcos: {num_marcos}")

    algoritmos = [
        ("FIFO", fifo),
        ("LRU", lru),
        ("Optimo (OPT)", optimo),
        ("Clock (Segunda Oportunidad)", clock),
    ]

    resultados = []
    for nombre, funcion in algoritmos:
        fallos, historial = funcion(secuencia, num_marcos)
        mostrar_historial(nombre, secuencia, fallos, historial, num_marcos)
        resultados.append((nombre, fallos))

    # Resumen comparativo
    print(f"\n{'=' * 50}")
    print(f"  RESUMEN COMPARATIVO")
    print(f"{'=' * 50}")
    print(f"  {'Algoritmo':<30} | {'Fallos':>6}")
    print(f"  {'-' * 30}-+-{'-' * 6}")
    for nombre, fallos in sorted(resultados, key=lambda x: x[1]):
        print(f"  {nombre:<30} | {fallos:>6}")
    print(f"\n  (Menor es mejor. Optimo es la cota inferior teorica.)")

    # Efecto del numero de marcos
    print(f"\n{'=' * 60}")
    print("  EFECTO DEL NUMERO DE MARCOS")
    print(f"{'=' * 60}")
    funciones = [fifo, lru, optimo, clock]
    nombres_cortos = ["FIFO", "LRU", "OPT", "Clock"]

    encabezado = f"  {'Marcos':>6}"
    for n in nombres_cortos:
        encabezado += f" | {n:>6}"
    print(encabezado)
    print(f"  {'-' * 6}" + ("-+-" + "-" * 6) * len(nombres_cortos))

    for m in range(1, 8):
        linea = f"  {m:>6}"
        for func in funciones:
            f, _ = func(secuencia, m)
            linea += f" | {f:>6}"
        print(linea)

    # Anomalia de Belady
    demostrar_anomalia_belady()


if __name__ == "__main__":
    main()
```

**Observa:**
- Optimo siempre tiene la menor cantidad de fallos (referencia teorica).
- LRU generalmente se acerca al Optimo.
- FIFO puede tener mas fallos que los demas.
- Clock es una buena aproximacion de LRU con menor costo de implementacion.

**Ejercicio:** Modifica `num_marcos` y la cadena de referencias para explorar diferentes escenarios. Intenta encontrar una cadena donde Clock se comporte significativamente diferente a LRU.

---
