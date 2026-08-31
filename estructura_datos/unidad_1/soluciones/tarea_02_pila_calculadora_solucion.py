"""Solución de referencia — Tarea 2: Calculadora postfija con Pila."""


class Pila:
    def __init__(self):
        self._datos = []

    def apilar(self, valor):
        self._datos.append(valor)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("pila vacía")
        return self._datos.pop()

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0


def evaluar_postfija(expresion: str) -> float:
    OPERADORES = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    pila = Pila()
    for token in expresion.split():
        if token in OPERADORES:
            derecha = pila.desapilar()   # el último apilado es el operando derecho
            izquierda = pila.desapilar()
            pila.apilar(OPERADORES[token](izquierda, derecha))
        else:
            pila.apilar(float(token))

    resultado = pila.desapilar()
    return int(resultado) if resultado == int(resultado) else resultado


if __name__ == "__main__":
    for expr in ["3 4 +", "3 4 + 2 *", "5 1 2 + 4 * + 3 -", "10 2 /"]:
        print(f"{expr} = {evaluar_postfija(expr)}")
