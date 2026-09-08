"""Capa de servicios — la lógica de negocio del flujo ACOM vive aquí,
no en las vistas ni en los modelos (Service Layer, visto en la Unidad 1).
"""

from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from .exceptions import LimiteCreditosError, TransicionInvalidaError
from .models import Constancia, EstadoInscripcion, Inscripcion, RegistroCreditos
from .signals import inscripcion_validada

META_CREDITOS_ACOM = Decimal("5.00")


class InscripcionService:
    @staticmethod
    def inscribir(estudiante, actividad):
        if not actividad.activa:
            raise TransicionInvalidaError("Esta actividad ya no está activa.")
        return Inscripcion.objects.create(estudiante=estudiante, actividad=actividad)

    @staticmethod
    def evaluar(inscripcion: Inscripcion, aprobado: bool, responsable, observaciones: str = ""):
        if inscripcion.estado != EstadoInscripcion.INSCRITO:
            raise TransicionInvalidaError(
                f"No se puede evaluar una inscripción en estado '{inscripcion.estado}'."
            )
        if inscripcion.actividad.responsable_id != responsable.id:
            raise TransicionInvalidaError("Solo el responsable de la actividad puede evaluarla.")

        inscripcion.estado = (
            EstadoInscripcion.EVALUADO_APROBADO if aprobado else EstadoInscripcion.EVALUADO_RECHAZADO
        )
        inscripcion.fecha_evaluacion = timezone.now()
        inscripcion.observaciones = observaciones
        inscripcion.save(update_fields=["estado", "fecha_evaluacion", "observaciones"])
        return inscripcion

    @staticmethod
    def emitir_constancia(inscripcion: Inscripcion, emitida_por) -> Constancia:
        if inscripcion.estado != EstadoInscripcion.EVALUADO_APROBADO:
            raise TransicionInvalidaError(
                "Solo se emite constancia para inscripciones aprobadas en la evaluación."
            )

        folio = f"ACOM-{inscripcion.id:06d}"
        with transaction.atomic():
            constancia = Constancia.objects.create(
                inscripcion=inscripcion, folio=folio, emitida_por=emitida_por
            )
            inscripcion.estado = EstadoInscripcion.CONSTANCIA_EMITIDA
            inscripcion.save(update_fields=["estado"])
        return constancia

    @staticmethod
    def validar_y_registrar(inscripcion: Inscripcion, validado_por) -> RegistroCreditos:
        if inscripcion.estado != EstadoInscripcion.CONSTANCIA_EMITIDA:
            raise TransicionInvalidaError(
                "Solo se registra una inscripción con constancia ya emitida."
            )

        creditos_previos = CreditosService.total_validado(inscripcion.estudiante)
        if creditos_previos >= META_CREDITOS_ACOM:
            raise LimiteCreditosError(
                f"El estudiante ya cubrió los {META_CREDITOS_ACOM} créditos ACOM requeridos."
            )

        with transaction.atomic():
            registro = RegistroCreditos.objects.create(
                inscripcion=inscripcion,
                creditos_otorgados=inscripcion.actividad.creditos_valor,
                validado_por=validado_por,
            )
            inscripcion.estado = EstadoInscripcion.VALIDADO
            inscripcion.save(update_fields=["estado"])

        inscripcion_validada.send(sender=InscripcionService, inscripcion=inscripcion)
        return registro


class CreditosService:
    @staticmethod
    def total_validado(estudiante) -> Decimal:
        total = RegistroCreditos.objects.filter(
            inscripcion__estudiante=estudiante
        ).aggregate(total=Sum("creditos_otorgados"))["total"]
        return total or Decimal("0")

    @staticmethod
    def faltantes(estudiante) -> Decimal:
        return max(Decimal("0"), META_CREDITOS_ACOM - CreditosService.total_validado(estudiante))
