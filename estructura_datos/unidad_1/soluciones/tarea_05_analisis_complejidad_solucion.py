"""Solución de referencia — Tarea 5: Análisis de complejidad.

funcion_a: acceso directo al primer elemento -> O(1)
funcion_b: un solo recorrido de n elementos -> O(n)
funcion_c: doble ciclo anidado sobre n elementos -> O(n^2)
funcion_d: búsqueda binaria, descarta la mitad en cada paso -> O(log n)
funcion_e: sorted() en Python usa Timsort -> O(n log n)
"""

RESPUESTAS = {
    "funcion_a": "O(1)",
    "funcion_b": "O(n)",
    "funcion_c": "O(n^2)",
    "funcion_d": "O(log n)",
    "funcion_e": "O(n log n)",
}

if __name__ == "__main__":
    for nombre, complejidad in RESPUESTAS.items():
        print(f"{nombre}: {complejidad}")
