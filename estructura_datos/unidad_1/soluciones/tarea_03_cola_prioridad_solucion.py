"""Solución de referencia — Tarea 3: Cola de Prioridad."""


class ColaDePrioridad:
    def __init__(self):
        self._elementos = []  # lista de tuplas (prioridad, valor)

    def encolar(self, valor, prioridad):
        self._elementos.append((prioridad, valor))

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("cola vacía")
        indice_max = max(range(len(self._elementos)), key=lambda i: self._elementos[i][0])
        _, valor = self._elementos.pop(indice_max)
        return valor

    def esta_vacia(self) -> bool:
        return len(self._elementos) == 0


if __name__ == "__main__":
    cp = ColaDePrioridad()
    cp.encolar("ticket normal", prioridad=1)
    cp.encolar("ticket urgente", prioridad=10)
    cp.encolar("ticket medio", prioridad=5)

    while not cp.esta_vacia():
        print(cp.desencolar())
