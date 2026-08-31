"""
1.4 — Manejo de memoria: estática vs dinámica

En Python no se gestiona memoria manualmente (hay recolector de
basura), pero el concepto sigue aplicando: una lista se comporta
como estructura dinámica; un array de tamaño fijo ilustra mejor
la idea de memoria estática.
"""

from array import array


def memoria_estatica():
    # Tamaño fijo, reservado desde su creación — no puede "crecer"
    fija = array('i', [1, 2, 3])
    print("Arreglo estático:", fija, "tamaño fijo:", len(fija))
    # fija.append(4) SÍ existe en array, pero conceptualmente representa
    # el caso "tamaño se define antes de ejecutar y no cambia"


def memoria_dinamica():
    # Crece sola, pidiendo memoria sobre la marcha
    dinamica = []
    for i in range(5):
        dinamica.append(i)
        print(f"tamaño={len(dinamica)} id={id(dinamica)}")


class Nodo:
    """Nodo enlazado — cada bloque de memoria se reserva individualmente
    y se conecta al siguiente por referencia (típico de listas enlazadas,
    árboles, etc.)."""

    def __init__(self, valor, siguiente=None):
        self.valor = valor
        self.siguiente = siguiente


def lista_enlazada_manual():
    primero = Nodo(10)
    primero.siguiente = Nodo(20)
    primero.siguiente.siguiente = Nodo(30)

    actual = primero
    while actual is not None:
        print(actual.valor, end=" -> " if actual.siguiente else "\n")
        actual = actual.siguiente


if __name__ == "__main__":
    print("--- Memoria estática ---")
    memoria_estatica()

    print("\n--- Memoria dinámica ---")
    memoria_dinamica()

    print("\n--- Lista enlazada manual (nodos con memoria dinámica) ---")
    lista_enlazada_manual()
