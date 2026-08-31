"""
Tarea 2 — Calculadora de notación postfija (RPN) usando el TDA Pila (1.2-1.3)

La notación postfija (o polaca inversa) escribe el operador DESPUÉS
de sus operandos: "3 4 +" significa 3 + 4.

Algoritmo (usa una Pila):
  - Recorre los tokens de la expresión de izquierda a derecha.
  - Si el token es un número, apílalo.
  - Si el token es un operador (+, -, *, /), desapila los DOS últimos
    valores, aplica el operador (el primero desapilado es el operando
    derecho) y apila el resultado.
  - Al final, el único valor en la pila es el resultado.

Ejemplo: "3 4 + 2 *" -> (3 + 4) * 2 -> 14

Completa `evaluar_postfija()`. Corre este archivo para probar tu solución:
    python3 tarea_02_pila_calculadora.py
"""


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
    """TODO: implementa la evaluación de una expresión postfija usando Pila.

    expresion: string con tokens separados por espacio, ej "3 4 + 2 *"
    return: el resultado numérico de la expresión
    """
    # TODO: tu código aquí
    raise NotImplementedError


# --- Casos de prueba — no modifiques ---

CASOS = [
    ("3 4 +", 7),
    ("3 4 + 2 *", 14),
    ("5 1 2 + 4 * + 3 -", 14),
    ("10 2 /", 5),
]

if __name__ == "__main__":
    aciertos = 0
    for expresion, esperado in CASOS:
        try:
            resultado = evaluar_postfija(expresion)
        except NotImplementedError:
            print("[PENDIENTE] evaluar_postfija() sin implementar")
            break

        if resultado == esperado:
            print(f"[OK] '{expresion}' = {resultado}")
            aciertos += 1
        else:
            print(f"[FALLO] '{expresion}': obtuviste {resultado}, se esperaba {esperado}")
    else:
        print(f"\n{aciertos}/{len(CASOS)} correctas")
