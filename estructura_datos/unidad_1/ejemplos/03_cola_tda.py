"""
1.2-1.3 — TDA Cola (Queue), FIFO

Caso de uso: cola de impresión de una oficina. El primer documento
enviado a imprimir es el primero en salir.
"""


class Cola:
    def __init__(self):
        self._datos = []

    def encolar(self, valor):
        self._datos.append(valor)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("cola vacía")
        return self._datos.pop(0)

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0

    def __len__(self):
        return len(self._datos)


class ColaDeImpresion:
    def __init__(self):
        self._trabajos = Cola()

    def enviar(self, documento):
        print(f"'{documento}' añadido a la cola")
        self._trabajos.encolar(documento)

    def imprimir_siguiente(self):
        if not self._trabajos.esta_vacia():
            doc = self._trabajos.desencolar()
            print(f"Imprimiendo: {doc}")
        else:
            print("No hay trabajos pendientes")


if __name__ == "__main__":
    impresora = ColaDeImpresion()
    impresora.enviar("reporte.pdf")
    impresora.enviar("factura.pdf")
    impresora.imprimir_siguiente()   # reporte.pdf — el primero en llegar
    impresora.imprimir_siguiente()   # factura.pdf
    impresora.imprimir_siguiente()   # cola vacía
