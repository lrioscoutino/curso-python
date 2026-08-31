"""
1.1 — Principios SOLID

Cinco principios de diseño orientado a objetos — la base de por qué
Django separa modelos, vistas y serializers.
"""


# --- S: Single Responsibility Principle ---
# MAL: el modelo valida reglas de negocio complejas además de representar datos
class PedidoMal:
    def __init__(self, total):
        self.total = total

    def guardar_en_bd(self):
        print(f"[BD] Guardando pedido por ${self.total}")

    def enviar_email_confirmacion(self, email):
        print(f"[EMAIL] Confirmación enviada a {email}")

    def calcular_impuestos(self):
        return self.total * 0.16


# BIEN: cada clase tiene una sola razón para cambiar
class Pedido:
    def __init__(self, total):
        self.total = total


class PedidoRepository:
    def guardar(self, pedido: Pedido):
        print(f"[BD] Guardando pedido por ${pedido.total}")


class NotificadorEmail:
    def enviar_confirmacion(self, pedido: Pedido, email: str):
        print(f"[EMAIL] Confirmación enviada a {email}")


class CalculadoraImpuestos:
    def calcular(self, pedido: Pedido) -> float:
        return pedido.total * 0.16


# --- O: Open/Closed Principle ---
# Extender comportamiento con nuevas clases, sin modificar la existente
class Descuento:
    def aplicar(self, total: float) -> float:
        return total


class DescuentoVIP(Descuento):
    def aplicar(self, total: float) -> float:
        return total * 0.9


class DescuentoTemporada(Descuento):
    def aplicar(self, total: float) -> float:
        return total * 0.85


def calcular_total_con_descuento(total: float, descuento: Descuento) -> float:
    return descuento.aplicar(total)


# --- L: Liskov Substitution Principle ---
# Un CustomUser debe poder usarse en cualquier lugar donde se espera un User
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

    def obtener_permisos(self) -> list[str]:
        return ["ver_perfil"]


class UsuarioAdministrador(Usuario):
    def obtener_permisos(self) -> list[str]:
        return ["ver_perfil", "editar_todo", "eliminar_usuarios"]


def mostrar_permisos(usuario: Usuario):
    print(f"{usuario.nombre}: {usuario.obtener_permisos()}")


# --- I: Interface Segregation Principle ---
# Serializers específicos por caso de uso, no uno gigante que todos importan
class SerializadorListaUsuarios:
    def serializar(self, usuario: Usuario) -> dict:
        return {"nombre": usuario.nombre}


class SerializadorDetalleUsuario:
    def serializar(self, usuario: Usuario) -> dict:
        return {"nombre": usuario.nombre, "permisos": usuario.obtener_permisos()}


# --- D: Dependency Inversion Principle ---
# Las vistas dependen de una interfaz de servicio, no directamente de una API externa
class ServicioDePago:
    def cobrar(self, monto: float) -> bool:
        raise NotImplementedError


class ServicioStripe(ServicioDePago):
    def cobrar(self, monto: float) -> bool:
        print(f"[Stripe] Cobrando ${monto}")
        return True


class ServicioPayPal(ServicioDePago):
    def cobrar(self, monto: float) -> bool:
        print(f"[PayPal] Cobrando ${monto}")
        return True


def procesar_cobro(servicio: ServicioDePago, monto: float):
    # esta función no sabe (ni le importa) si es Stripe o PayPal
    return servicio.cobrar(monto)


if __name__ == "__main__":
    print("--- S: Single Responsibility ---")
    pedido = Pedido(1000)
    PedidoRepository().guardar(pedido)
    NotificadorEmail().enviar_confirmacion(pedido, "ana@example.com")
    print("Impuestos:", CalculadoraImpuestos().calcular(pedido))

    print("\n--- O: Open/Closed ---")
    print("Con descuento VIP:", calcular_total_con_descuento(1000, DescuentoVIP()))
    print("Con descuento temporada:", calcular_total_con_descuento(1000, DescuentoTemporada()))

    print("\n--- L: Liskov Substitution ---")
    mostrar_permisos(Usuario("Luis"))
    mostrar_permisos(UsuarioAdministrador("Ana"))

    print("\n--- I: Interface Segregation ---")
    print(SerializadorListaUsuarios().serializar(Usuario("Marco")))
    print(SerializadorDetalleUsuario().serializar(UsuarioAdministrador("Sofía")))

    print("\n--- D: Dependency Inversion ---")
    procesar_cobro(ServicioStripe(), 500)
    procesar_cobro(ServicioPayPal(), 250)
