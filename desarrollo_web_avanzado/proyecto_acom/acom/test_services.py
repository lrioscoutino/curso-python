from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .exceptions import LimiteCreditosError, TransicionInvalidaError
from .models import ActividadComplementaria, CategoriaActividad, EstadoInscripcion
from .services import CreditosService, InscripcionService

User = get_user_model()


class FlujoAcomTest(TestCase):
    def setUp(self):
        self.estudiante = User.objects.create_user("estudiante1", password="x")
        self.responsable = User.objects.create_user("docente1", password="x")
        self.depto = User.objects.create_user("depto1", password="x")
        self.actividad = ActividadComplementaria.objects.create(
            nombre="Verano de Investigación 2026",
            categoria=CategoriaActividad.INVESTIGACION,
            responsable=self.responsable,
            creditos_valor=Decimal("2.00"),
        )

    def test_flujo_completo_hasta_registro_de_creditos(self):
        inscripcion = InscripcionService.inscribir(self.estudiante, self.actividad)
        self.assertEqual(inscripcion.estado, EstadoInscripcion.INSCRITO)

        InscripcionService.evaluar(inscripcion, aprobado=True, responsable=self.responsable)
        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.estado, EstadoInscripcion.EVALUADO_APROBADO)

        constancia = InscripcionService.emitir_constancia(inscripcion, emitida_por=self.responsable)
        self.assertEqual(constancia.folio, f"ACOM-{inscripcion.id:06d}")
        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.estado, EstadoInscripcion.CONSTANCIA_EMITIDA)

        registro = InscripcionService.validar_y_registrar(inscripcion, validado_por=self.depto)
        self.assertEqual(registro.creditos_otorgados, Decimal("2.00"))
        inscripcion.refresh_from_db()
        self.assertEqual(inscripcion.estado, EstadoInscripcion.VALIDADO)

        self.assertEqual(CreditosService.total_validado(self.estudiante), Decimal("2.00"))
        self.assertEqual(CreditosService.faltantes(self.estudiante), Decimal("3.00"))

    def test_no_se_puede_emitir_constancia_sin_evaluar(self):
        inscripcion = InscripcionService.inscribir(self.estudiante, self.actividad)
        with self.assertRaises(TransicionInvalidaError):
            InscripcionService.emitir_constancia(inscripcion, emitida_por=self.responsable)

    def test_solo_el_responsable_de_la_actividad_puede_evaluar(self):
        inscripcion = InscripcionService.inscribir(self.estudiante, self.actividad)
        otro_docente = User.objects.create_user("docente2", password="x")
        with self.assertRaises(TransicionInvalidaError):
            InscripcionService.evaluar(inscripcion, aprobado=True, responsable=otro_docente)

    def test_no_se_registran_creditos_pasado_el_limite(self):
        inscripcion1 = InscripcionService.inscribir(self.estudiante, self.actividad)
        InscripcionService.evaluar(inscripcion1, aprobado=True, responsable=self.responsable)
        InscripcionService.emitir_constancia(inscripcion1, emitida_por=self.responsable)
        InscripcionService.validar_y_registrar(inscripcion1, validado_por=self.depto)

        actividad_grande = ActividadComplementaria.objects.create(
            nombre="Diplomado",
            categoria=CategoriaActividad.CURSO,
            responsable=self.responsable,
            creditos_valor=Decimal("5.00"),
        )
        inscripcion2 = InscripcionService.inscribir(self.estudiante, actividad_grande)
        InscripcionService.evaluar(inscripcion2, aprobado=True, responsable=self.responsable)
        InscripcionService.emitir_constancia(inscripcion2, emitida_por=self.responsable)
        InscripcionService.validar_y_registrar(inscripcion2, validado_por=self.depto)
        # ahora tiene 2.00 + 5.00 = 7.00, ya por encima de la meta de 5.00

        actividad_extra = ActividadComplementaria.objects.create(
            nombre="Actividad extra",
            categoria=CategoriaActividad.TUTORIA,
            responsable=self.responsable,
            creditos_valor=Decimal("1.00"),
        )
        inscripcion3 = InscripcionService.inscribir(self.estudiante, actividad_extra)
        InscripcionService.evaluar(inscripcion3, aprobado=True, responsable=self.responsable)
        InscripcionService.emitir_constancia(inscripcion3, emitida_por=self.responsable)
        with self.assertRaises(LimiteCreditosError):
            InscripcionService.validar_y_registrar(inscripcion3, validado_por=self.depto)
