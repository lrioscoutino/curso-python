"""
Tarea 5 — Sistema de eventos tipo Observer (1.2)

Implementa la clase EventBus, similar al ejemplo de Signal, pero
genérica: debe permitir suscribirse a cualquier nombre de evento
(no solo "post_save_pedido") y emitir eventos con datos arbitrarios.

Métodos requeridos:
  - suscribir(evento: str, callback): registra callback para ese evento
  - emitir(evento: str, **datos): llama a TODOS los callbacks suscritos
    a ese evento, pasándoles **datos

Corre este archivo para verificar tu solución:
    python3 tarea_05_observer_eventos.py
"""


class EventBus:
    def __init__(self):
        self._suscriptores = {}  # evento -> lista de callbacks

    def suscribir(self, evento: str, callback):
        # TODO: registra `callback` para `evento`
        raise NotImplementedError

    def emitir(self, evento: str, **datos):
        # TODO: llama a todos los callbacks suscritos a `evento`, pasando **datos.
        # Si no hay suscriptores para ese evento, no hagas nada (no falles).
        raise NotImplementedError


# --- Caso de prueba — no modifiques ---

if __name__ == "__main__":
    bus = EventBus()
    recibidos = []

    def escuchar_registro(usuario, email):
        recibidos.append(("bienvenida", usuario, email))

    def escuchar_registro_analytics(usuario, email):
        recibidos.append(("analytics", usuario))

    try:
        bus.suscribir("usuario_registrado", escuchar_registro)
        bus.suscribir("usuario_registrado", escuchar_registro_analytics)

        bus.emitir("usuario_registrado", usuario="ana", email="ana@example.com")
        bus.emitir("evento_sin_suscriptores", x=1)  # no debe fallar

        esperado = [
            ("bienvenida", "ana", "ana@example.com"),
            ("analytics", "ana"),
        ]

        if recibidos == esperado:
            print("[OK] EventBus disparó ambos callbacks correctamente:", recibidos)
        else:
            print(f"[FALLO] obtuviste {recibidos}, se esperaba {esperado}")
    except NotImplementedError:
        print("[PENDIENTE] EventBus sin implementar")
