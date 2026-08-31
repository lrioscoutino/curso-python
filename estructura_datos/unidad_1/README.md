# Estructura de Datos — Unidad 1: Introducción

Código de ejemplo y tareas para la Unidad 1 (clasificación de estructuras de datos, Tipos de Datos Abstractos, manejo de memoria y análisis de algoritmos). Todo el código es Python 3, ejecutable directamente con `python3 archivo.py`.

## Estructura

```
unidad_1/
├── ejemplos/     # código de referencia, resuelto y comentado — para estudiar y correr
├── tareas/       # ejercicios con TODO — el estudiante completa las funciones marcadas
└── soluciones/   # soluciones de referencia de cada tarea (no ver antes de intentarlo)
```

## Ejemplos (`ejemplos/`)

| Archivo | Tema |
|---|---|
| `01_tipos_datos.py` | Tipos de datos en Python: numéricos, secuencias, mutable vs inmutable |
| `02_pila_tda.py` | TDA Pila (LIFO) — caso de uso: deshacer/rehacer |
| `03_cola_tda.py` | TDA Cola (FIFO) — caso de uso: cola de impresión |
| `04_lista_tda.py` | TDA Lista — caso de uso: lista de reproducción |
| `05_arbol_tda.py` | TDA Árbol — caso de uso: sistema de archivos |
| `06_grafo_tda.py` | TDA Grafo — caso de uso: red social |
| `07_diccionario_tda.py` | TDA Diccionario — caso de uso: frecuencia de palabras |
| `08_memoria_estatica_dinamica.py` | Memoria estática vs dinámica |
| `09_analisis_algoritmos.py` | Complejidad Big-O: búsqueda secuencial vs binaria |

Correr cualquiera:

```bash
python3 ejemplos/02_pila_tda.py
```

## Tareas (`tareas/`)

Cada archivo tiene funciones/clases con `# TODO` y `raise NotImplementedError` — hay que completarlas. Cada archivo incluye pruebas al final (`if __name__ == "__main__":`) que confirman si la tarea quedó bien resuelta.

| Archivo | Qué se pide |
|---|---|
| `tarea_01_clasificacion.py` | Clasificar estructuras dadas según los 4 ejes (organización, memoria, homogeneidad, nivel) |
| `tarea_02_pila_calculadora.py` | Usar una Pila para evaluar expresiones postfijas (notación polaca inversa) |
| `tarea_03_cola_prioridad.py` | Implementar una Cola de Prioridad simple sobre el TDA Cola |
| `tarea_04_arbol_binario_busqueda.py` | Implementar un Árbol Binario de Búsqueda (insertar y buscar) |
| `tarea_05_analisis_complejidad.py` | Calcular y justificar la complejidad de funciones dadas |

Correr una tarea (ejecuta sus propias pruebas):

```bash
python3 tareas/tarea_02_pila_calculadora.py
```

## Soluciones (`soluciones/`)

Un archivo espejo por cada tarea, con la implementación completa. Úsalas solo después de intentar la tarea — comparar tu solución con la de referencia es parte del aprendizaje, copiarla sin intentarlo no.
