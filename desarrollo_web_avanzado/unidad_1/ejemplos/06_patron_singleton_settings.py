"""
1.2 — Patrón Singleton (django.conf.settings)

`django.conf.settings` es un objeto único cargado una vez por proceso
— el ejemplo más directo del patrón en el framework. Cualquier módulo
que lo importe obtiene la MISMA instancia.
"""


class ConfiguracionMeta(type):
    """Metaclase que garantiza una sola instancia de Configuracion."""
    _instancia = None

    def __call__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super().__call__(*args, **kwargs)
        return cls._instancia


class Configuracion(metaclass=ConfiguracionMeta):
    def __init__(self):
        print("[Configuracion] Cargando settings desde disco (solo debería pasar UNA vez)")
        self.DEBUG = True
        self.DATABASE_URL = "postgres://localhost/miapp"


def modulo_a():
    config = Configuracion()
    return config


def modulo_b():
    config = Configuracion()
    return config


if __name__ == "__main__":
    config_a = modulo_a()   # imprime "Cargando settings..."
    config_b = modulo_b()   # NO vuelve a imprimir — es la misma instancia

    print("¿Misma instancia?", config_a is config_b)   # True
    print("DEBUG:", config_a.DEBUG)

    config_a.DEBUG = False
    print("config_b.DEBUG también cambió:", config_b.DEBUG)   # False — mismo objeto
