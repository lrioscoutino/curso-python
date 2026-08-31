"""
Tarea 4 — Árbol Binario de Búsqueda (1.2-1.3)

Un Árbol Binario de Búsqueda (ABB) es un árbol donde, para cada nodo:
  - todos los valores del subárbol izquierdo son MENORES,
  - todos los valores del subárbol derecho son MAYORES.

Esto permite buscar un valor en O(log n) en el caso promedio, en vez
de O(n) como en una lista.

Completa NodoABB con:
  - insertar(valor): agrega un valor manteniendo la propiedad del ABB
  - buscar(valor): devuelve True si el valor existe en el árbol

Corre este archivo para probar tu solución:
    python3 tarea_04_arbol_binario_busqueda.py
"""


class NodoABB:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

    def insertar(self, valor):
        """TODO: inserta `valor` en el subárbol correcto (izquierda si es
        menor que self.valor, derecha si es mayor). Si ya existe, no
        hagas nada."""
        # TODO: tu código aquí
        raise NotImplementedError

    def buscar(self, valor) -> bool:
        """TODO: devuelve True si `valor` existe en este árbol (o subárboles)."""
        # TODO: tu código aquí
        raise NotImplementedError


# --- Caso de prueba — no modifiques ---

if __name__ == "__main__":
    try:
        raiz = NodoABB(50)
        for v in [30, 70, 20, 40, 60, 80]:
            raiz.insertar(v)

        pruebas = [(40, True), (60, True), (99, False), (50, True)]
        aciertos = 0
        for valor, esperado in pruebas:
            resultado = raiz.buscar(valor)
            if resultado == esperado:
                print(f"[OK] buscar({valor}) = {resultado}")
                aciertos += 1
            else:
                print(f"[FALLO] buscar({valor}): obtuviste {resultado}, se esperaba {esperado}")

        print(f"\n{aciertos}/{len(pruebas)} correctas")
    except NotImplementedError:
        print("[PENDIENTE] NodoABB sin implementar")
