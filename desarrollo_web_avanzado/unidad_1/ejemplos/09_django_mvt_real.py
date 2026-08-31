"""
1.2 — Patrón MVT con Django REAL (Modelo - Vista - Template)

Ejemplo completo de un CRUD mínimo de "Artículo" siguiendo la
estructura MVT real de Django: models.py, views.py, urls.py y
template. NO es standalone — requiere un proyecto Django con la app
`blog` registrada en INSTALLED_APPS.

Aquí se combinan los 4 archivos en uno solo (separados por comentarios)
únicamente para fines didácticos. En un proyecto real cada bloque va
en su propio archivo dentro de la app.
"""

# ============================================================
# blog/models.py — el MODELO: estructura de datos
# ============================================================
"""
from django.db import models
from django.urls import reverse


class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("articulo_detalle", kwargs={"pk": self.pk})
"""

# ============================================================
# blog/views.py — la VISTA: lógica de negocio + orquestación
# ============================================================
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Articulo
from .forms import ArticuloForm


def lista_articulos(request):
    articulos = Articulo.objects.filter(publicado=True)
    return render(request, "blog/lista.html", {"articulos": articulos})


def articulo_detalle(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk, publicado=True)
    return render(request, "blog/detalle.html", {"articulo": articulo})


@login_required
def crear_articulo(request):
    if request.method == "POST":
        form = ArticuloForm(request.POST)
        if form.is_valid():
            articulo = form.save()
            return redirect(articulo.get_absolute_url())
    else:
        form = ArticuloForm()
    return render(request, "blog/formulario.html", {"form": form})
"""

# ============================================================
# blog/urls.py — enrutamiento (el "Controlador" en la variante MVT)
# ============================================================
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_articulos, name="lista_articulos"),
    path("articulo/<int:pk>/", views.articulo_detalle, name="articulo_detalle"),
    path("nuevo/", views.crear_articulo, name="crear_articulo"),
]
"""

# ============================================================
# blog/templates/blog/lista.html — la PLANTILLA: presentación,
# sin lógica de negocio
# ============================================================
"""
{% extends "base.html" %}

{% block content %}
  <h1>Artículos publicados</h1>
  <ul>
    {% for articulo in articulos %}
      <li>
        <a href="{% url 'articulo_detalle' articulo.pk %}">{{ articulo.titulo }}</a>
        <span>{{ articulo.fecha_publicacion|date:"d/m/Y" }}</span>
      </li>
    {% empty %}
      <li>No hay artículos publicados todavía.</li>
    {% endfor %}
  </ul>
{% endblock %}
"""

# ============================================================
# Por qué es MVT y no MVC clásico
# ============================================================
"""
- Modelo (Articulo)   -> gestiona los datos, no sabe nada de HTTP ni de HTML.
- Vista (views.py)     -> contiene la lógica: qué datos traer, qué hacer con
                          el formulario, a qué template mandar el resultado.
- Template (lista.html) -> solo presentación: recorre `articulos`, nunca
                          decide QUÉ artículos mostrar (eso ya lo filtró la vista).
- El "Controlador" en MVT lo cumple el propio Django: urls.py enruta la
  petición HTTP a la función/vista correcta — el desarrollador no escribe
  un controlador aparte como en MVC clásico.
"""
