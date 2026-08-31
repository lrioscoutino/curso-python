"""Solución de referencia — Tarea 2: Single Responsibility Principle."""


class CalculadoraFactura:
    def calcular(self, items: list[dict]) -> float:
        return sum(item["precio"] * item["cantidad"] for item in items)


class FacturaRepository:
    def guardar(self, total: float) -> None:
        print(f"[BD] Guardando factura por ${total}")


class GeneradorPDF:
    def generar(self, total: float) -> str:
        return f"--- FACTURA ---\nTotal: ${total}\n---------------"


if __name__ == "__main__":
    items = [{"precio": 100, "cantidad": 2}, {"precio": 50, "cantidad": 1}]

    total = CalculadoraFactura().calcular(items)
    FacturaRepository().guardar(total)
    print(GeneradorPDF().generar(total))
