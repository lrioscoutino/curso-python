"""
Tarea 4 — Decorador @reintentar (1.2)

Implementa un decorador `reintentar(intentos)` que, si la función
decorada lanza una excepción, la vuelva a llamar hasta `intentos`
veces antes de dejar propagar el error. Si tiene éxito en cualquier
intento, devuelve el resultado inmediatamente.

Usa functools.wraps para preservar el nombre de la función original.

Corre este archivo para verificar tu solución:
    python3 tarea_04_decorator_retry.py
"""

import functools


def reintentar(intentos: int):
    """TODO: implementa el decorador.

    - Debe intentar llamar a la función hasta `intentos` veces.
    - Si tiene éxito, devuelve el resultado inmediatamente (no sigue reintentando).
    - Si TODOS los intentos fallan, deja que la última excepción se propague.
    """
    def decorador(func):
        @functools.wraps(func)
        def envoltura(*args, **kwargs):
            # TODO: tu código aquí
            raise NotImplementedError
        return envoltura
    return decorador


# --- Caso de prueba — no modifiques ---

_contador_llamadas = {"conexion_inestable": 0}


@reintentar(intentos=3)
def conexion_inestable():
    """Falla las primeras 2 veces, funciona a la 3ra."""
    _contador_llamadas["conexion_inestable"] += 1
    if _contador_llamadas["conexion_inestable"] < 3:
        raise ConnectionError("fallo simulado")
    return "conectado"


@reintentar(intentos=2)
def siempre_falla():
    raise ValueError("esto siempre falla")


if __name__ == "__main__":
    try:
        resultado = conexion_inestable()
        if resultado == "conectado" and _contador_llamadas["conexion_inestable"] == 3:
            print(f"[OK] conexion_inestable() reintentó y tuvo éxito: {resultado}")
        else:
            print(f"[FALLO] resultado={resultado}, llamadas={_contador_llamadas}")

        try:
            siempre_falla()
            print("[FALLO] siempre_falla() debió lanzar ValueError")
        except ValueError:
            print("[OK] siempre_falla() agotó los intentos y propagó ValueError")

    except NotImplementedError:
        print("[PENDIENTE] reintentar() sin implementar")
