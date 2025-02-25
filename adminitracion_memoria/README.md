# Políticas de Administración de Memoria en Sistemas Operativos

Las políticas de administración de memoria son conjuntos de reglas y estrategias que los sistemas operativos utilizan para controlar cómo se asigna, utiliza y libera la memoria disponible entre los diferentes procesos y el propio sistema. Estas políticas son fundamentales para el rendimiento, eficiencia y estabilidad del sistema operativo.

## Principales políticas de administración de memoria:

### 1. Políticas de asignación
- **Asignación contigua vs. no contigua**: Determina si a un proceso se le debe asignar bloques de memoria contiguos o si puede utilizar bloques dispersos.
- **Asignación fija vs. variable**: Define si se asigna una cantidad predeterminada de memoria a cada proceso o si varía según sus necesidades.

### 2. Políticas de ubicación
- **First-fit**: Asigna el primer bloque disponible que sea suficientemente grande.
- **Best-fit**: Busca el bloque más pequeño que pueda acomodar el proceso.
- **Worst-fit**: Selecciona el bloque más grande disponible.
- **Next-fit**: Similar a first-fit, pero comienza la búsqueda desde la última asignación.

### 3. Políticas de reemplazo (para memoria virtual)
- **FIFO (First-In-First-Out)**: Reemplaza la página más antigua.
- **LRU (Least Recently Used)**: Elimina la página que no se ha usado por más tiempo.
- **LFU (Least Frequently Used)**: Reemplaza la página menos utilizada.
- **NRU (Not Recently Used)**: Considera tanto el uso reciente como la modificación.
- **Algoritmo óptimo**: Reemplaza la página que no se utilizará por más tiempo en el futuro.

### 4. Políticas de carga
- **Demand paging/loading**: Carga páginas solo cuando son solicitadas.
- **Prepaging/loading**: Carga páginas anticipadamente basándose en predicciones de uso.

### 5. Políticas de limpieza
- **Demand cleaning**: Escribe páginas modificadas a disco solo cuando es necesario liberarlas.
- **Precleaning**: Escribe páginas modificadas a disco antes de que sea necesario.

### 6. Políticas de control de tamaño de working set
- **Working set**: Conjunto de páginas que un proceso usa activamente.
- **Page fault frequency**: Ajusta la memoria asignada basándose en la frecuencia de fallos de página.

## Importancia de las políticas de administración de memoria:

1. **Eficiencia del sistema**: Maximizan el uso efectivo de la memoria disponible.
2. **Rendimiento**: Minimizan el tiempo de espera y maximizan el throughput.
3. **Equidad**: Garantizan que todos los procesos tengan acceso adecuado a los recursos.
4. **Prevención de problemas**: Evitan situaciones como fragmentación, thrashing y deadlocks.
5. **Adaptabilidad**: Permiten al sistema responder a diferentes cargas de trabajo y patrones de uso.