"""
1.2-1.3 — TDA Árbol

Caso de uso: representar un sistema de archivos. Cada carpeta es un
nodo con cero o más subcarpetas — una jerarquía natural, no una
secuencia.
"""


class NodoCarpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        self.subcarpetas = []

    def agregar(self, subcarpeta):
        self.subcarpetas.append(subcarpeta)

    def listar(self, nivel=0):
        print("  " * nivel + f"[dir] {self.nombre}")
        for hijo in self.subcarpetas:
            hijo.listar(nivel + 1)

    def contar_carpetas(self) -> int:
        total = 1  # se cuenta a sí misma
        for hijo in self.subcarpetas:
            total += hijo.contar_carpetas()
        return total


if __name__ == "__main__":
    raiz = NodoCarpeta("Documentos")
    trabajo = NodoCarpeta("Trabajo")
    personal = NodoCarpeta("Personal")

    raiz.agregar(trabajo)
    raiz.agregar(personal)
    trabajo.agregar(NodoCarpeta("Reportes"))
    trabajo.agregar(NodoCarpeta("Facturas"))

    raiz.listar()
    print(f"\nTotal de carpetas: {raiz.contar_carpetas()}")
