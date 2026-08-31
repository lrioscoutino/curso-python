"""
1.2-1.3 — TDA Lista

Caso de uso: lista de reproducción de música. Se necesita mantener el
orden, insertar una canción en medio (siguiente a reproducir), quitar
una y recorrerla en orden.
"""


class ListaReproduccion:
    def __init__(self):
        self._canciones = []

    def agregar(self, cancion):
        self._canciones.append(cancion)

    def insertar_siguiente(self, posicion_actual, cancion):
        self._canciones.insert(posicion_actual + 1, cancion)

    def quitar(self, cancion):
        self._canciones.remove(cancion)

    def __iter__(self):
        return iter(self._canciones)

    def __len__(self):
        return len(self._canciones)


if __name__ == "__main__":
    playlist = ListaReproduccion()
    playlist.agregar("Intro")
    playlist.agregar("Track 2")
    playlist.insertar_siguiente(0, "Interludio")   # justo después de "Intro"

    for cancion in playlist:
        print(cancion)
    # Intro, Interludio, Track 2

    playlist.quitar("Interludio")
    print("\nDespués de quitar 'Interludio':")
    for cancion in playlist:
        print(cancion)
