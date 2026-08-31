"""
1.0 — Tipos de datos en Python

Antes de construir estructuras de datos hay que conocer los tipos básicos
que Python ofrece: son los "ladrillos" con los que se arman los TDA's.
"""


def numericos_y_booleano():
    edad = 20                 # int — precisión arbitraria
    promedio = 8.75           # float — doble precisión (IEEE 754)
    z = 2 + 3j                # complex
    es_mayor = edad >= 18     # bool — subtipo de int

    print("int:", edad, type(edad))
    print("float:", promedio, type(promedio))
    print("complex:", z, type(z))
    print("bool:", es_mayor, "| True == 1 ->", True == 1)


def mutable_vs_inmutable():
    # Inmutable: una operación que "modifica" en realidad crea un objeto nuevo
    s = "hola"
    s_mayus = s.upper()
    print("str original:", s, "| nueva:", s_mayus)

    # Mutable: se modifica en el mismo objeto
    lista_a = [1, 2, 3]
    lista_b = lista_a          # misma referencia, no una copia
    lista_b.append(4)
    print("lista_a:", lista_a, "<- cambió aunque solo tocamos lista_b")

    # tuple: inmutable, pero si contiene un objeto mutable, ese sí cambia
    t = ([1, 2], 3)
    t[0].append(9)
    print("tuple con lista interna:", t, "<- la lista interna sí cambió")


def secuencias_conjuntos_mapeos():
    nombre = "Ana"             # str, inmutable
    numeros = [1, 2, 3]        # list, mutable
    punto = (10, 20)           # tuple, inmutable
    vistos = {1, 2, 3}         # set, sin duplicados
    edades = {"Ana": 20, "Luis": 22}  # dict, clave-valor

    print("str:", nombre)
    print("list:", numeros)
    print("tuple:", punto)
    print("set:", vistos, "| 2 in vistos ->", 2 in vistos)
    print("dict:", edades, "| edades['Ana'] ->", edades["Ana"])


if __name__ == "__main__":
    print("--- Numéricos y booleano ---")
    numericos_y_booleano()

    print("\n--- Mutable vs inmutable ---")
    mutable_vs_inmutable()

    print("\n--- Secuencias, conjuntos y mapeos ---")
    secuencias_conjuntos_mapeos()
