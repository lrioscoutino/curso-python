from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ActividadComplementaria, CategoriaActividad, Inscripcion

User = get_user_model()


class FlujoHttpTest(TestCase):
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

    def test_flujo_completo_via_http(self):
        # 1. Estudiante ve la lista y se inscribe
        self.client.force_login(self.estudiante)
        resp = self.client.get(reverse("acom:lista_actividades"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Verano de Investigación 2026")

        resp = self.client.post(reverse("acom:inscribirse", args=[self.actividad.id]))
        self.assertRedirects(resp, reverse("acom:mis_inscripciones"))

        inscripcion = Inscripcion.objects.get(estudiante=self.estudiante, actividad=self.actividad)

        resp = self.client.get(reverse("acom:mis_inscripciones"))
        self.assertContains(resp, "Inscrito")
        self.assertContains(resp, "0.00 / 5.00")

        # 2. Responsable evalúa y emite constancia
        self.client.force_login(self.responsable)
        resp = self.client.post(
            reverse("acom:panel_responsable", args=[inscripcion.id]),
            {"evaluar": "1", "aprobado": "1", "observaciones": "Excelente desempeño"},
        )
        self.assertRedirects(resp, reverse("acom:panel_responsable", args=[inscripcion.id]))

        resp = self.client.post(
            reverse("acom:panel_responsable", args=[inscripcion.id]),
            {"emitir_constancia": "1"},
        )
        self.assertRedirects(resp, reverse("acom:panel_responsable", args=[inscripcion.id]))

        inscripcion.refresh_from_db()
        self.assertTrue(hasattr(inscripcion, "constancia"))

        # 3. Departamento valida y registra créditos
        self.client.force_login(self.depto)
        resp = self.client.get(reverse("acom:panel_departamento", args=[inscripcion.id]))
        self.assertContains(resp, inscripcion.constancia.folio)

        resp = self.client.post(reverse("acom:panel_departamento", args=[inscripcion.id]))
        self.assertRedirects(resp, reverse("acom:panel_departamento", args=[inscripcion.id]))

        # 4. El estudiante ya ve sus créditos actualizados
        self.client.force_login(self.estudiante)
        resp = self.client.get(reverse("acom:mis_inscripciones"))
        self.assertContains(resp, "2.00 / 5.00")
        self.assertContains(resp, "Validado")
