"""
1.2 — Patrón Observer (signals de Django)

Las signals de Django desacoplan "qué pasó" de "quién reacciona" —
un modelo no necesita saber quién escucha su guardado. Este ejemplo
implementa un mini sistema de signals desde cero.
"""


class Signal:
    """Equivalente simplificado a django.db.models.signals.Signal."""

    def __init__(self, nombre):
        self.nombre = nombre
        self._receptores = []

    def connect(self, receptor):
        self._receptores.append(receptor)

    def send(self, sender, **kwargs):
        for receptor in self._receptores:
            receptor(sender=sender, **kwargs)


post_save_pedido = Signal("post_save_pedido")


def receiver(signal):
    """Decorador equivalente a @receiver de Django."""
    def decorador(func):
        signal.connect(func)
        return func
    return decorador


@receiver(post_save_pedido)
def notificar_email(sender, instance, created, **kwargs):
    if created:
        print(f"[EMAIL] Nuevo pedido #{instance['id']} — enviando confirmación")


@receiver(post_save_pedido)
def actualizar_inventario(sender, instance, created, **kwargs):
    if created:
        print(f"[INVENTARIO] Descontando stock del pedido #{instance['id']}")


class PedidoModel:
    """Simula el .save() de un modelo Django que dispara la signal."""

    def save(self, instance, created=True):
        print(f"[BD] Guardando pedido #{instance['id']}")
        post_save_pedido.send(sender=PedidoModel, instance=instance, created=created)


if __name__ == "__main__":
    pedido = {"id": 101, "total": 500}
    PedidoModel().save(pedido, created=True)

    # notificar_email y actualizar_inventario reaccionaron sin que
    # PedidoModel supiera que existían — ese es el punto del Observer.
