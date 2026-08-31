"""
1.2-1.3 — TDA Grafo

Caso de uso: una red social donde las amistades no tienen "padre" ni
"hijo" — solo conexiones. Un grafo permite responder
"¿a cuántos pasos de amistad está esta persona de otra?".
"""

from collections import deque


class RedSocial:
    def __init__(self):
        self._conexiones = {}   # persona -> lista de amigos

    def agregar_persona(self, nombre):
        self._conexiones.setdefault(nombre, [])

    def conectar(self, persona_a, persona_b):
        self._conexiones[persona_a].append(persona_b)
        self._conexiones[persona_b].append(persona_a)   # relación bidireccional

    def amigos_de(self, persona):
        return self._conexiones.get(persona, [])

    def pasos_entre(self, origen, destino):
        """BFS — distancia más corta en número de amistades."""
        if origen == destino:
            return 0
        visitados = {origen}
        cola = deque([(origen, 0)])
        while cola:
            actual, distancia = cola.popleft()
            for amigo in self._conexiones.get(actual, []):
                if amigo == destino:
                    return distancia + 1
                if amigo not in visitados:
                    visitados.add(amigo)
                    cola.append((amigo, distancia + 1))
        return -1  # no conectados


if __name__ == "__main__":
    red = RedSocial()
    for persona in ["Ana", "Luis", "Marco", "Sofía", "Elena"]:
        red.agregar_persona(persona)

    red.conectar("Ana", "Luis")
    red.conectar("Luis", "Marco")
    red.conectar("Marco", "Sofía")

    print("Amigos de Luis:", red.amigos_de("Luis"))
    print("Pasos de Ana a Sofía:", red.pasos_entre("Ana", "Sofía"))   # 3
    print("Pasos de Ana a Elena:", red.pasos_entre("Ana", "Elena"))   # -1, no conectados
