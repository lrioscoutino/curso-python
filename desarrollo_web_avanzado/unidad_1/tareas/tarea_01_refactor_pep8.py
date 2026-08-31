"""
Tarea 1 — Refactorizar a PEP 8 (1.1)

La función `procesar_datos_mal` funciona, pero viola varias reglas
de PEP 8 y buenas prácticas: nombres de una letra, comparación con
None usando ==, línea densa sin espacios, sin tipado.

Completa `procesar_datos_bien` para que haga EXACTAMENTE lo mismo
pero con nombres descriptivos, comparaciones correctas (`is None`),
espaciado PEP 8 y anotaciones de tipo.

Corre este archivo para verificar tu solución:
    python3 tarea_01_refactor_pep8.py
"""


def procesar_datos_mal(l, d=None):
    if d == None:
        d = 0
    r = []
    for i in l:
        if i>0:
            r.append(i-d)
    return r


def procesar_datos_bien(numeros: list[float], descuento: float = 0) -> list[float]:
    """TODO: reescribe la lógica de procesar_datos_mal con buen estilo.

    Debe: filtrar los números positivos y restarles `descuento` a cada uno,
    devolviendo la lista resultante — mismo comportamiento, mejor forma.
    """
    # TODO: tu código aquí
    raise NotImplementedError


# --- Casos de prueba — no modifiques ---

CASOS = [
    ([10, -5, 20, 0, 15], 5, [5, 15, 10]),
    ([1, 2, 3], 0, [1, 2, 3]),
    ([-1, -2, -3], 1, []),
]

if __name__ == "__main__":
    aciertos = 0
    for entrada, descuento, esperado in CASOS:
        try:
            resultado = procesar_datos_bien(entrada, descuento)
        except NotImplementedError:
            print("[PENDIENTE] procesar_datos_bien() sin implementar")
            break

        # Verifica que el comportamiento coincida con la versión "mal"
        resultado_referencia = procesar_datos_mal(entrada, descuento)
        if resultado == esperado == resultado_referencia:
            print(f"[OK] procesar_datos_bien({entrada}, {descuento}) = {resultado}")
            aciertos += 1
        else:
            print(f"[FALLO] obtuviste {resultado}, se esperaba {esperado}")
    else:
        print(f"\n{aciertos}/{len(CASOS)} correctas")
