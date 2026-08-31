"""
1.5 — Análisis de algoritmos: complejidad en tiempo y espacio

Compara búsqueda secuencial O(n) contra búsqueda binaria O(log n)
midiendo tiempo real de ejecución para distintos tamaños de entrada.
"""

import time
import random


def busqueda_secuencial(lista, objetivo):   # O(n)
    for i, valor in enumerate(lista):
        if valor == objetivo:
            return i
    return -1


def busqueda_binaria(lista_ordenada, objetivo):   # O(log n)
    izq, der = 0, len(lista_ordenada) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista_ordenada[medio] == objetivo:
            return medio
        if lista_ordenada[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1


def tiene_duplicados_n2(lista):   # O(n²)
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False


def tiene_duplicados_n(lista):   # O(n) tiempo, O(n) espacio
    vistos = set()
    for x in lista:
        if x in vistos:
            return True
        vistos.add(x)
    return False


def medir(func, *args):
    inicio = time.perf_counter()
    resultado = func(*args)
    duracion = time.perf_counter() - inicio
    return resultado, duracion


if __name__ == "__main__":
    for tamano in [1_000, 10_000, 100_000]:
        datos = list(range(tamano))
        objetivo = tamano - 1  # peor caso para secuencial: al final

        _, t_secuencial = medir(busqueda_secuencial, datos, objetivo)
        _, t_binaria = medir(busqueda_binaria, datos, objetivo)

        print(f"n={tamano:>7}  secuencial={t_secuencial*1000:.4f}ms  "
              f"binaria={t_binaria*1000:.4f}ms")

    print("\n--- Detección de duplicados: O(n²) vs O(n) ---")
    datos_grandes = [random.randint(0, 1_000_000) for _ in range(5_000)]

    _, t_n2 = medir(tiene_duplicados_n2, datos_grandes)
    _, t_n = medir(tiene_duplicados_n, datos_grandes)
    print(f"O(n²): {t_n2*1000:.2f}ms   O(n): {t_n*1000:.2f}ms")
