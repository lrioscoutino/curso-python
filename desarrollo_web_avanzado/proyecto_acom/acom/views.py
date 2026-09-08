from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .exceptions import LimiteCreditosError, TransicionInvalidaError
from .forms import EvaluacionForm
from .models import ActividadComplementaria, Inscripcion
from .services import CreditosService, InscripcionService


@login_required
def lista_actividades(request):
    """El estudiante ve las actividades disponibles y se inscribe (MVT: Vista)."""
    actividades = ActividadComplementaria.objects.filter(activa=True)
    return render(request, "acom/lista_actividades.html", {"actividades": actividades})


@login_required
def inscribirse(request, actividad_id):
    actividad = get_object_or_404(ActividadComplementaria, pk=actividad_id, activa=True)
    if request.method == "POST":
        InscripcionService.inscribir(request.user, actividad)
        return redirect("acom:mis_inscripciones")
    return render(request, "acom/confirmar_inscripcion.html", {"actividad": actividad})


@login_required
def mis_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(estudiante=request.user).select_related("actividad")
    creditos_totales = CreditosService.total_validado(request.user)
    creditos_faltantes = CreditosService.faltantes(request.user)
    return render(
        request,
        "acom/mis_inscripciones.html",
        {
            "inscripciones": inscripciones,
            "creditos_totales": creditos_totales,
            "creditos_faltantes": creditos_faltantes,
        },
    )


@login_required
def panel_responsable(request, inscripcion_id):
    """El docente/responsable evalúa y emite la constancia."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)

    if request.method == "POST" and "evaluar" in request.POST:
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            try:
                InscripcionService.evaluar(
                    inscripcion,
                    aprobado=form.cleaned_data["aprobado"],
                    responsable=request.user,
                    observaciones=form.cleaned_data["observaciones"],
                )
            except TransicionInvalidaError as e:
                return render(
                    request, "acom/panel_responsable.html",
                    {"inscripcion": inscripcion, "form": form, "error": str(e)},
                )
            return redirect("acom:panel_responsable", inscripcion_id=inscripcion.id)
    elif request.method == "POST" and "emitir_constancia" in request.POST:
        try:
            InscripcionService.emitir_constancia(inscripcion, emitida_por=request.user)
        except TransicionInvalidaError as e:
            return render(
                request, "acom/panel_responsable.html",
                {"inscripcion": inscripcion, "form": EvaluacionForm(), "error": str(e)},
            )
        return redirect("acom:panel_responsable", inscripcion_id=inscripcion.id)

    return render(
        request, "acom/panel_responsable.html",
        {"inscripcion": inscripcion, "form": EvaluacionForm()},
    )


@login_required
def panel_departamento(request, inscripcion_id):
    """El Departamento Académico valida la constancia y registra los créditos."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)
    error = None
    if request.method == "POST":
        try:
            InscripcionService.validar_y_registrar(inscripcion, validado_por=request.user)
            return redirect("acom:panel_departamento", inscripcion_id=inscripcion.id)
        except (TransicionInvalidaError, LimiteCreditosError) as e:
            error = str(e)

    return render(
        request, "acom/panel_departamento.html", {"inscripcion": inscripcion, "error": error}
    )
