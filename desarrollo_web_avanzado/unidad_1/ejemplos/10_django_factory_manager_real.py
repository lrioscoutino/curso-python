"""
1.2 — Patrón Factory Method con Django REAL (Manager personalizado)

A diferencia de 03_patron_factory_manager.py (que simula el ORM con
listas en memoria para correr sin Django), este archivo muestra un
Manager personalizado real, usando el ORM de Django de verdad.

NO es standalone: requiere un proyecto Django con la app `blog`
registrada y su migración aplicada.
"""

# ============================================================
# blog/models.py — Manager personalizado real
# ============================================================
"""
from django.db import models


class ArticuloQuerySet(models.QuerySet):
    '''QuerySet personalizado — permite encadenar filtros propios
    junto con los del ORM estándar: Articulo.objects.publicados().order_by("titulo")'''

    def publicados(self):
        return self.filter(publicado=True)

    def borradores(self):
        return self.filter(publicado=False)

    def del_autor(self, usuario):
        return self.filter(autor=usuario)


class ArticuloManager(models.Manager):
    '''El Manager es la fábrica: encapsula CÓMO se construyen los
    querysets filtrados, en vez de repetir el mismo `.filter(...)`
    en cada vista.'''

    def get_queryset(self):
        return ArticuloQuerySet(self.model, using=self._db)

    def publicados(self):
        return self.get_queryset().publicados()

    def borradores(self):
        return self.get_queryset().borradores()


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    publicado = models.BooleanField(default=False)

    objects = ArticuloManager()   # reemplaza el manager por defecto

    def __str__(self):
        return self.titulo
"""

# ============================================================
# blog/views.py — uso del Manager personalizado en una vista real
# ============================================================
"""
from django.shortcuts import render
from .models import Articulo


def lista_articulos(request):
    # Sin el Manager, cada vista repetiría:
    #   Articulo.objects.filter(publicado=True)
    # Con el Manager, la "fábrica" ya sabe construir ese queryset:
    articulos = Articulo.objects.publicados().order_by("-id")
    return render(request, "blog/lista.html", {"articulos": articulos})


def mis_borradores(request):
    articulos = Articulo.objects.borradores().del_autor(request.user)
    return render(request, "blog/borradores.html", {"articulos": articulos})
"""

# ============================================================
# Test real (requiere Django configurado)
# ============================================================
"""
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Articulo


class ArticuloManagerTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create(username="ana")
        Articulo.objects.create(titulo="Publicado", autor=self.usuario, publicado=True)
        Articulo.objects.create(titulo="Borrador", autor=self.usuario, publicado=False)

    def test_manager_publicados_filtra_correctamente(self):
        publicados = Articulo.objects.publicados()
        self.assertEqual(publicados.count(), 1)
        self.assertEqual(publicados.first().titulo, "Publicado")

    def test_manager_borradores_filtra_correctamente(self):
        borradores = Articulo.objects.borradores()
        self.assertEqual(borradores.count(), 1)
        self.assertEqual(borradores.first().titulo, "Borrador")
"""

# ============================================================
# Por qué es Factory Method
# ============================================================
"""
El Manager (Articulo.objects) es responsable de "fabricar" los
QuerySets ya filtrados según reglas de negocio (publicados, borradores,
del autor X) — el código que llama (la vista) no construye el filtro
a mano, solo pide el "producto" ya armado: `Articulo.objects.publicados()`.
Esa es exactamente la idea del Factory Method: delegar la construcción
de un objeto (aquí, un QuerySet) a un método dedicado, en vez de
repetir la lógica de construcción en cada punto de uso.
"""
