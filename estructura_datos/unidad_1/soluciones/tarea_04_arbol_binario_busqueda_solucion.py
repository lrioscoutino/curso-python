"""Solución de referencia — Tarea 4: Árbol Binario de Búsqueda."""


class NodoABB:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

    def insertar(self, valor):
        if valor == self.valor:
            return  # ya existe, no hacer nada
        if valor < self.valor:
            if self.izquierda is None:
                self.izquierda = NodoABB(valor)
            else:
                self.izquierda.insertar(valor)
        else:
            if self.derecha is None:
                self.derecha = NodoABB(valor)
            else:
                self.derecha.insertar(valor)

    def buscar(self, valor) -> bool:
        if valor == self.valor:
            return True
        if valor < self.valor:
            return self.izquierda.buscar(valor) if self.izquierda else False
        return self.derecha.buscar(valor) if self.derecha else False


if __name__ == "__main__":
    raiz = NodoABB(50)
    for v in [30, 70, 20, 40, 60, 80]:
        raiz.insertar(v)

    for valor in [40, 60, 99, 50]:
        print(f"buscar({valor}) = {raiz.buscar(valor)}")
