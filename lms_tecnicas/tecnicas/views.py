from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Tecnica, ProgresoEstudiante
import json

Usuario = get_user_model()

def es_profesor(user):
    return user.is_authenticated and user.is_staff

@login_required
def dashboard_estudiante(request):
    tecnicas = Tecnica.objects.all()
    progresos = {p.tecnica_id: p for p in ProgresoEstudiante.objects.filter(estudiante=request.user)}
    return render(request, 'dashboard_estudiante.html', {
        'tecnicas': tecnicas,
        'progresos': progresos
    })

@login_required
@user_passes_test(es_profesor)
def dashboard_profesor(request):
    estudiantes = Usuario.objects.filter(es_estudiante=True)
    stats = []
    for est in estudiantes:
        total = Tecnica.objects.count()
        completadas = ProgresoEstudiante.objects.filter(estudiante=est, completada=True).count()
        stats.append({
            'nombre': est.get_full_name() or est.username,
            'completadas': completadas,
            'total': total,
            'porcentaje': round(completadas/total*100, 1) if total else 0
        })
    return render(request, 'dashboard_profesor.html', {'estadisticas': stats})

@login_required
def tecnica_detail(request, tecnica_id):
    tecnica = get_object_or_404(Tecnica, id=tecnica_id)
    progreso, _ = ProgresoEstudiante.objects.get_or_create(
        estudiante=request.user, tecnica=tecnica
    )
    return render(request, 'tecnica_detail.html', {
        'tecnica': tecnica,
        'progreso': progreso
    })

@login_required
def guardar_progreso_api(request, tecnica_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        completada = data.get('completada', False)
        respuesta = data.get('respuesta', '')
        progreso, _ = ProgresoEstudiante.objects.get_or_create(
            estudiante=request.user, tecnica_id=tecnica_id
        )
        progreso.completada = completada
        progreso.ultima_respuesta = respuesta
        progreso.intentos = progreso.intentos + 1
        progreso.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
