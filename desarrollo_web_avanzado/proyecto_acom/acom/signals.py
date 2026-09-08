"""Signal propia (Observer, visto en la Unidad 1): el servicio que valida
una inscripción no necesita saber quién reacciona a eso — solo avisa.
"""

import django.dispatch

inscripcion_validada = django.dispatch.Signal()
