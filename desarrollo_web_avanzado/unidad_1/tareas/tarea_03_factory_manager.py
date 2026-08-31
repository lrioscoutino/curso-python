"""
Tarea 3 — Manager personalizado (Factory Method) (1.2)

Implementa ProductoManager, similar al ejemplo de ArticuloManager,
pero para una tienda: debe poder devolver solo los productos
"disponibles" (stock > 0) y solo los "agotados" (stock == 0).

Corre este archivo para verificar tu solución:
    python3 tarea_03_factory_manager.py
"""


class Producto:
    def __init__(self, nombre, stock):
        self.nombre = nombre
        self.stock = stock

    def __repr__(self):
        return f"<Producto {self.nombre!r} stock={self.stock}>"


class ProductoManager:
    def __init__(self, productos):
        self._productos = productos

    def disponibles(self):
        """TODO: devuelve solo los productos con stock > 0."""
        # TODO: tu código aquí
        raise NotImplementedError

    def agotados(self):
        """TODO: devuelve solo los productos con stock == 0."""
        # TODO: tu código aquí
        raise NotImplementedError


# --- Caso de prueba — no modifiques ---

if __name__ == "__main__":
    productos = [
        Producto("Teclado", 5),
        Producto("Mouse", 0),
        Producto("Monitor", 3),
        Producto("Cable HDMI", 0),
    ]

    manager = ProductoManager(productos)

    try:
        disponibles = manager.disponibles()
        agotados = manager.agotados()

        nombres_disponibles = sorted(p.nombre for p in disponibles)
        nombres_agotados = sorted(p.nombre for p in agotados)

        esperado_disponibles = ["Monitor", "Teclado"]
        esperado_agotados = ["Cable HDMI", "Mouse"]

        if nombres_disponibles == esperado_disponibles and nombres_agotados == esperado_agotados:
            print("[OK] disponibles:", nombres_disponibles)
            print("[OK] agotados:", nombres_agotados)
        else:
            print(f"[FALLO] disponibles={nombres_disponibles} agotados={nombres_agotados}")
    except NotImplementedError:
        print("[PENDIENTE] ProductoManager sin implementar")
