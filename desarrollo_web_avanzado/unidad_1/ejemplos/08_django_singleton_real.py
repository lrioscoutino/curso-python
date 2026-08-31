"""
1.2 — Patrón Singleton con Django REAL (django.conf.settings)

A diferencia de 06_patron_singleton_settings.py (que simula el patrón
con una metaclase propia para correr sin Django), este archivo muestra
el patrón tal como Django lo implementa de verdad.

NO es standalone: requiere un proyecto Django con DJANGO_SETTINGS_MODULE
configurado. Se documenta como referencia de código real, no como script
para ejecutar con `python3 archivo.py`.
"""

# ============================================================
# settings.py (raíz del proyecto)
# ============================================================
"""
DEBUG = True
DATABASE_URL = "postgres://localhost/miapp"
SECRET_KEY = "..."
INSTALLED_APPS = [...]
"""

# ============================================================
# Cualquier módulo del proyecto — app/services.py
# ============================================================
from django.conf import settings


def enviar_notificacion(mensaje: str):
    if settings.DEBUG:
        print(f"[DEBUG] Simulando envío: {mensaje}")
    else:
        # en producción, usar el backend de email real
        print(f"[PROD] Enviando: {mensaje}")


# ============================================================
# otro_modulo.py — importa settings de forma independiente
# ============================================================
from django.conf import settings as config


def obtener_conexion_bd():
    # `settings` y `config` son la MISMA instancia — Django la carga
    # una sola vez por proceso, sin importar cuántas veces se importe.
    return config.DATABASE_URL


# ============================================================
# Por qué es Singleton
# ============================================================
"""
django.conf.settings es una instancia de LazySettings (django/conf/__init__.py).
Se instancia UNA sola vez a nivel de módulo:

    settings = LazySettings()

Cualquier `from django.conf import settings` en cualquier archivo del
proyecto obtiene una referencia a ese mismo objeto — exactamente el
comportamiento Singleton: una sola instancia compartida por todo el
proceso, cargada de forma perezosa (lazy) la primera vez que se accede
a un atributo.
"""

# ============================================================
# Test real (requiere Django configurado) — pytest-django o
# manage.py test
# ============================================================
"""
from django.conf import settings
from django.test import TestCase


class SingletonSettingsTest(TestCase):
    def test_misma_instancia_en_todo_el_proceso(self):
        from django.conf import settings as settings_a
        from django.conf import settings as settings_b
        self.assertIs(settings_a, settings_b)
"""
