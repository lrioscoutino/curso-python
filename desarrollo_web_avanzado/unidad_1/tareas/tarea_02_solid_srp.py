"""
Tarea 2 — Single Responsibility Principle (1.1)

La clase `Factura` de abajo viola SRP: calcula totales, los guarda en
"base de datos", y genera un PDF — tres razones distintas para cambiar
en una sola clase.

Completa las 3 clases separadas: CalculadoraFactura, FacturaRepository
y GeneradorPDF — cada una con una sola responsabilidad. Usa la misma
lógica que ya está en FacturaMal (cópiala, no la reinventes).

Corre este archivo para verificar tu solución:
    python3 tarea_02_solid_srp.py
"""


class FacturaMal:
    """NO modificar — referencia de la lógica que debes separar."""

    def __init__(self, items):
        self.items = items

    def calcular_total(self):
        return sum(item["precio"] * item["cantidad"] for item in self.items)

    def guardar(self, total):
        print(f"[BD] Guardando factura por ${total}")

    def generar_pdf(self, total):
        return f"--- FACTURA ---\nTotal: ${total}\n---------------"


class CalculadoraFactura:
    """TODO: responsabilidad única -> calcular el total de una lista de items."""

    def calcular(self, items: list[dict]) -> float:
        # TODO: tu código aquí (misma lógica que FacturaMal.calcular_total)
        raise NotImplementedError


class FacturaRepository:
    """TODO: responsabilidad única -> persistir la factura."""

    def guardar(self, total: float) -> None:
        # TODO: tu código aquí (misma lógica que FacturaMal.guardar)
        raise NotImplementedError


class GeneradorPDF:
    """TODO: responsabilidad única -> generar la representación en texto/PDF."""

    def generar(self, total: float) -> str:
        # TODO: tu código aquí (misma lógica que FacturaMal.generar_pdf)
        raise NotImplementedError


# --- Caso de prueba — no modifiques ---

if __name__ == "__main__":
    items = [{"precio": 100, "cantidad": 2}, {"precio": 50, "cantidad": 1}]

    try:
        total = CalculadoraFactura().calcular(items)
        FacturaRepository().guardar(total)
        pdf = GeneradorPDF().generar(total)

        total_esperado = FacturaMal(items).calcular_total()
        pdf_esperado = FacturaMal(items).generar_pdf(total_esperado)

        if total == total_esperado and pdf == pdf_esperado:
            print("[OK] Las 3 clases reproducen el comportamiento de FacturaMal")
            print(pdf)
        else:
            print(f"[FALLO] total={total} (esperado {total_esperado})")
    except NotImplementedError:
        print("[PENDIENTE] una o más clases sin implementar")
