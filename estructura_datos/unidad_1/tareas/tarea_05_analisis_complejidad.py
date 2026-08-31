"""
Tarea 5 — Análisis de complejidad (1.5)

Para cada función en `FUNCIONES_A_ANALIZAR`, escribe en `RESPUESTAS`
la complejidad en tiempo Big-O que corresponde. Usa el formato exacto:
"O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)".

Corre este archivo para verificar tus respuestas:
    python3 tarea_05_analisis_complejidad.py
"""


def funcion_a(lista):
    return lista[0] if lista else None


def funcion_b(lista):
    total = 0
    for x in lista:
        total += x
    return total


def funcion_c(lista):
    for i in range(len(lista)):
        for j in range(len(lista)):
            if lista[i] == lista[j] and i != j:
                return True
    return False


def funcion_d(lista_ordenada, objetivo):
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


def funcion_e(lista):
    return sorted(lista)  # Python usa Timsort


FUNCIONES_A_ANALIZAR = {
    "funcion_a": funcion_a,
    "funcion_b": funcion_b,
    "funcion_c": funcion_c,
    "funcion_d": funcion_d,
    "funcion_e": funcion_e,
}

# TODO: completa con la complejidad de cada función.
RESPUESTAS = {
    "funcion_a": None,   # TODO
    "funcion_b": None,   # TODO
    "funcion_c": None,   # TODO
    "funcion_d": None,   # TODO
    "funcion_e": None,   # TODO
}


# --- No modifiques nada debajo de esta línea ---

_SOLUCION_ESPERADA = {
    "funcion_a": "O(1)",
    "funcion_b": "O(n)",
    "funcion_c": "O(n^2)",
    "funcion_d": "O(log n)",
    "funcion_e": "O(n log n)",
}

if __name__ == "__main__":
    aciertos = 0
    for nombre in FUNCIONES_A_ANALIZAR:
        respuesta = RESPUESTAS.get(nombre)
        esperado = _SOLUCION_ESPERADA[nombre]
        if respuesta is None:
            print(f"[PENDIENTE] {nombre}")
        elif respuesta == esperado:
            print(f"[OK] {nombre} = {respuesta}")
            aciertos += 1
        else:
            print(f"[FALLO] {nombre}: obtuviste {respuesta!r}, se esperaba {esperado!r}")

    print(f"\n{aciertos}/{len(FUNCIONES_A_ANALIZAR)} correctas")
