"""
Tarea 3 — Cola de Prioridad simple (1.2-1.3)

Una Cola de Prioridad es una variante del TDA Cola donde cada elemento
tiene una prioridad, y `desencolar()` siempre devuelve el elemento con
MAYOR prioridad (no necesariamente el primero en llegar).

Implementa la clase ColaDePrioridad con:
  - encolar(valor, prioridad): agrega un elemento con su prioridad
  - desencolar(): quita y devuelve el valor de mayor prioridad
  - esta_vacia(): True si no hay elementos

Pista: puedes usar una lista interna de tuplas (prioridad, valor) y
buscar/quitar el máximo cada vez que se desencola. No necesitas usar
un heap todavía — esta unidad busca reforzar el concepto de TDA, no
la estructura interna óptima.

Corre este archivo para probar tu solución:
    python3 tarea_03_cola_prioridad.py
"""


class ColaDePrioridad:
    def __init__(self):
        self._elementos = []  # lista de tuplas (prioridad, valor)

    def encolar(self, valor, prioridad):
        # TODO: agrega (prioridad, valor) a self._elementos
        raise NotImplementedError

    def desencolar(self):
        # TODO: quita y devuelve el VALOR con mayor prioridad.
        # Si está vacía, lanza IndexError("cola vacía")
        raise NotImplementedError

    def esta_vacia(self) -> bool:
        return len(self._elementos) == 0


# --- Caso de prueba — no modifiques ---

if __name__ == "__main__":
    cp = ColaDePrioridad()
    try:
        cp.encolar("ticket normal", prioridad=1)
        cp.encolar("ticket urgente", prioridad=10)
        cp.encolar("ticket medio", prioridad=5)

        orden_esperado = ["ticket urgente", "ticket medio", "ticket normal"]
        obtenido = []
        while not cp.esta_vacia():
            obtenido.append(cp.desencolar())

        if obtenido == orden_esperado:
            print(f"[OK] Orden correcto: {obtenido}")
        else:
            print(f"[FALLO] obtuviste {obtenido}, se esperaba {orden_esperado}")
    except NotImplementedError:
        print("[PENDIENTE] ColaDePrioridad sin implementar")
