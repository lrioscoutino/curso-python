"""
1.2 — Patrón Factory Method (Manager de Django)

Un Manager personalizado es una fábrica de querysets. Encapsula cómo
se construyen "conjuntos filtrados de objetos" en vez de repetir el
mismo filtro por todo el código.

Este ejemplo simula el ORM de Django con listas en memoria, para
poder correrlo sin instalar Django.
"""


class Articulo:
    def __init__(self, titulo, estado):
        self.titulo = titulo
        self.estado = estado  # "borrador" | "publicado"

    def __repr__(self):
        return f"<Articulo {self.titulo!r} ({self.estado})>"


class ArticuloManager:
    """Equivalente a `Articulo.objects` en Django."""

    def __init__(self, articulos):
        self._articulos = articulos

    def todos(self):
        return list(self._articulos)

    def publicados(self):
        return [a for a in self._articulos if a.estado == "publicado"]

    def borradores(self):
        return [a for a in self._articulos if a.estado == "borrador"]


if __name__ == "__main__":
    articulos = [
        Articulo("Introducción a Django", "publicado"),
        Articulo("Patrones de diseño en Python", "publicado"),
        Articulo("Borrador sin terminar", "borrador"),
    ]

    manager = ArticuloManager(articulos)

    print("Todos:", manager.todos())
    print("Publicados:", manager.publicados())
    print("Borradores:", manager.borradores())

    # En Django real, esto sería:
    #   objects = models.Manager()
    #   publicados = PublicadoManager()
    #   Articulo.publicados.all()
