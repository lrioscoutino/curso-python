"""Solución de referencia — Tarea 5: Sistema de eventos tipo Observer."""


class EventBus:
    def __init__(self):
        self._suscriptores = {}

    def suscribir(self, evento: str, callback):
        self._suscriptores.setdefault(evento, []).append(callback)

    def emitir(self, evento: str, **datos):
        for callback in self._suscriptores.get(evento, []):
            callback(**datos)


if __name__ == "__main__":
    bus = EventBus()

    bus.suscribir("usuario_registrado", lambda usuario, email: print(f"Bienvenida a {usuario} ({email})"))
    bus.suscribir("usuario_registrado", lambda usuario, email: print(f"Analytics: nuevo registro {usuario}"))

    bus.emitir("usuario_registrado", usuario="ana", email="ana@example.com")
