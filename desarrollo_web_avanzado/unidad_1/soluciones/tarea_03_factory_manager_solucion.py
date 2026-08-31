"""Solución de referencia — Tarea 3: Manager personalizado (Factory Method)."""


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
        return [p for p in self._productos if p.stock > 0]

    def agotados(self):
        return [p for p in self._productos if p.stock == 0]


if __name__ == "__main__":
    productos = [
        Producto("Teclado", 5),
        Producto("Mouse", 0),
        Producto("Monitor", 3),
        Producto("Cable HDMI", 0),
    ]

    manager = ProductoManager(productos)
    print("Disponibles:", manager.disponibles())
    print("Agotados:", manager.agotados())
