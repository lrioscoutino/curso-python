"""Solución de referencia — Tarea 1: Refactorizar a PEP 8."""


def procesar_datos_mal(l, d=None):
    if d == None:
        d = 0
    r = []
    for i in l:
        if i > 0:
            r.append(i - d)
    return r


def procesar_datos_bien(numeros: list[float], descuento: float = 0) -> list[float]:
    positivos = [numero for numero in numeros if numero > 0]
    return [numero - descuento for numero in positivos]


if __name__ == "__main__":
    print(procesar_datos_bien([10, -5, 20, 0, 15], 5))   # [5, 15, 10]
    print(procesar_datos_bien([1, 2, 3], 0))               # [1, 2, 3]
    print(procesar_datos_bien([-1, -2, -3], 1))             # []
