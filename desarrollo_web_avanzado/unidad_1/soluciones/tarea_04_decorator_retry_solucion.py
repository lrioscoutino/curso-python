"""Solución de referencia — Tarea 4: Decorador @reintentar."""

import functools


def reintentar(intentos: int):
    def decorador(func):
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            ultimo_error = None
            for intento in range(1, intentos + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    ultimo_error = e
                    print(f"[reintentar] intento {intento}/{intentos} falló: {e}")
            raise ultimo_error
        return envoltura
    return decorador


_contador = {"conexion_inestable": 0}


@reintentar(intentos=3)
def conexion_inestable():
    _contador["conexion_inestable"] += 1
    if _contador["conexion_inestable"] < 3:
        raise ConnectionError("fallo simulado")
    return "conectado"


if __name__ == "__main__":
    print(conexion_inestable())
