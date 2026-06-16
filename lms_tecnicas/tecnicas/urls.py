from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_estudiante, name='dashboard_estudiante'),
    path('profesor/', views.dashboard_profesor, name='dashboard_profesor'),
    path('tecnica/<int:tecnica_id>/', views.tecnica_detail, name='tecnica_detail'),
    path('api/progreso/<int:tecnica_id>/', views.guardar_progreso_api, name='guardar_progreso_api'),
]
