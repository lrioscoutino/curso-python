"""
1.1 — PEP 8 y legibilidad

El estándar de estilo de Python. Django lo asume como base y añade
convenciones propias (apps en minúsculas, modelos en PascalCase,
campos y funciones en snake_case).
"""


# --- MAL: nombres ambiguos, sin tipado, condicional confusa ---
def calc(x, y, z=None):
    if z == None:
        z = 0
    return x*y+z


# --- BIEN: nombres explícitos, tipado, sin ambigüedad ---
def calcular_total(precio: float, cantidad: int, descuento: float = 0) -> float:
    """Calcula el total de una compra aplicando un descuento fijo."""
    return precio * cantidad - descuento


# --- MAL: función que hace demasiadas cosas, difícil de testear ---
def procesar_pedido_mal(pedido):
    total = 0
    for item in pedido["items"]:
        total += item["precio"] * item["cantidad"]
    if pedido["cliente"]["vip"]:
        total *= 0.9
    print("Total:", total)
    pedido["total"] = total
    return pedido


# --- BIEN: responsabilidades separadas, sin efectos secundarios ocultos ---
def calcular_subtotal(items: list[dict]) -> float:
    return sum(item["precio"] * item["cantidad"] for item in items)


def aplicar_descuento_vip(subtotal: float, es_vip: bool) -> float:
    return subtotal * 0.9 if es_vip else subtotal


def procesar_pedido(pedido: dict) -> dict:
    subtotal = calcular_subtotal(pedido["items"])
    total = aplicar_descuento_vip(subtotal, pedido["cliente"]["vip"])
    return {**pedido, "total": total}


if __name__ == "__main__":
    print("calcular_total(100, 3, 20) =", calcular_total(100, 3, 20))

    pedido = {
        "cliente": {"nombre": "Ana", "vip": True},
        "items": [
            {"precio": 50, "cantidad": 2},
            {"precio": 20, "cantidad": 1},
        ],
    }
    resultado = procesar_pedido(pedido)
    print("Total con descuento VIP:", resultado["total"])
