"""
1.2 — Service Layer

No es parte del framework, pero es la práctica que evita que la
lógica de negocio viva en las vistas: una capa `services.py` entre
la vista y el "ORM".
"""


class Pedido:
    def __init__(self, id, usuario, items, total=0):
        self.id = id
        self.usuario = usuario
        self.items = items
        self.total = total


class PedidoRepository:
    """Simula el ORM: guarda pedidos en memoria."""

    def __init__(self):
        self._pedidos = {}
        self._siguiente_id = 1

    def crear(self, usuario, items):
        pedido = Pedido(self._siguiente_id, usuario, items)
        self._pedidos[pedido.id] = pedido
        self._siguiente_id += 1
        return pedido

    def obtener(self, id):
        return self._pedidos.get(id)


class PedidoService:
    """Orquesta la lógica de negocio — la vista solo llama a este servicio."""

    def __init__(self, repository: PedidoRepository):
        self.repository = repository

    def crear_pedido(self, usuario, items):
        if not items:
            raise ValueError("El pedido debe tener al menos un item")

        pedido = self.repository.crear(usuario, items)
        pedido.total = sum(item["precio"] * item["cantidad"] for item in items)

        print(f"[EMAIL] Confirmación de pedido #{pedido.id} enviada a {usuario}")
        return pedido


# --- Vista (simulada) — delgada, solo orquesta ---
def vista_crear_pedido(request, service: PedidoService):
    usuario = request["usuario"]
    items = request["items"]
    try:
        pedido = service.crear_pedido(usuario, items)
        return {"status": 201, "pedido_id": pedido.id, "total": pedido.total}
    except ValueError as e:
        return {"status": 400, "error": str(e)}


if __name__ == "__main__":
    repository = PedidoRepository()
    service = PedidoService(repository)

    request_valido = {
        "usuario": "ana@example.com",
        "items": [{"precio": 100, "cantidad": 2}, {"precio": 50, "cantidad": 1}],
    }
    print(vista_crear_pedido(request_valido, service))

    request_invalido = {"usuario": "luis@example.com", "items": []}
    print(vista_crear_pedido(request_invalido, service))
