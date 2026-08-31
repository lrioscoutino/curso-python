"""
1.2-1.3 — TDA Pila (Stack), LIFO

Caso de uso: función "deshacer" (Ctrl+Z) de un editor de texto.
Cada acción se apila; deshacer significa quitar la última acción y
revertirla — exactamente el comportamiento LIFO: lo último que pasó
es lo primero que se deshace.
"""


class Pila:
    """El TDA Pila solo promete estas operaciones — no importa si por
    dentro usa una lista de Python o un arreglo fijo."""

    def __init__(self):
        self._datos = []

    def apilar(self, valor):
        self._datos.append(valor)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("pila vacía")
        return self._datos.pop()

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("pila vacía")
        return self._datos[-1]

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0

    def __len__(self):
        return len(self._datos)


class EditorConDeshacer:
    def __init__(self):
        self.texto = ""
        self._historial = Pila()

    def escribir(self, fragmento):
        self._historial.apilar(self.texto)   # guarda el estado ANTES del cambio
        self.texto += fragmento

    def deshacer(self):
        if not self._historial.esta_vacia():
            self.texto = self._historial.desapilar()


if __name__ == "__main__":
    editor = EditorConDeshacer()
    editor.escribir("Hola")
    editor.escribir(" mundo")
    print("Texto:", editor.texto)          # "Hola mundo"

    editor.deshacer()
    print("Después de deshacer:", editor.texto)   # "Hola"

    print("\n--- Otro caso: verificación de paréntesis balanceados ---")

    def parentesis_balanceados(expresion: str) -> bool:
        pares = {")": "(", "]": "[", "}": "{"}
        pila = Pila()
        for caracter in expresion:
            if caracter in "([{":
                pila.apilar(caracter)
            elif caracter in ")]}":
                if pila.esta_vacia() or pila.desapilar() != pares[caracter]:
                    return False
        return pila.esta_vacia()

    for expr in ["(a + b) * [c - d]", "(a + b] * [c)", "((("]:
        print(f"{expr!r} -> {parentesis_balanceados(expr)}")
