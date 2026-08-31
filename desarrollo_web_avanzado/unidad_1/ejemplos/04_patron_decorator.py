"""
1.2 — Patrón Decorator

Envuelve una función/vista con comportamiento adicional sin tocar su
cuerpo — autenticación, caché, límites de tasa. En Django:
@login_required, @require_http_methods, @cache_page.
"""

import functools
import time


def login_required(vista):
    """Equivalente simplificado de @login_required de Django."""
    @functools.wraps(vista)
    def envoltura(request, *args, **kwargs):
        if not request.get("usuario_autenticado"):
            return {"status": 302, "redirect": "/login/"}
        return vista(request, *args, **kwargs)
    return envoltura


def cache_resultado(segundos: int):
    """Equivalente simplificado de @cache_page de Django."""
    def decorador(vista):
        cache = {}

        @functools.wraps(vista)
        def envoltura(request, *args, **kwargs):
            clave = str(args) + str(kwargs)
            if clave in cache:
                resultado, timestamp = cache[clave]
                if time.time() - timestamp < segundos:
                    print("[cache] resultado servido desde caché")
                    return resultado
            resultado = vista(request, *args, **kwargs)
            cache[clave] = (resultado, time.time())
            return resultado
        return envoltura
    return decorador


@login_required
def crear_pedido(request):
    return {"status": 200, "mensaje": "Pedido creado"}


@cache_resultado(segundos=5)
def reporte_ventas(request):
    print("[vista] calculando reporte de ventas (operación costosa)...")
    return {"status": 200, "total_ventas": 15000}


if __name__ == "__main__":
    print("--- login_required ---")
    print(crear_pedido({"usuario_autenticado": False}))
    print(crear_pedido({"usuario_autenticado": True}))

    print("\n--- cache_resultado ---")
    print(reporte_ventas({}))  # calcula
    print(reporte_ventas({}))  # sirve desde caché
