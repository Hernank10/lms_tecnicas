from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Tecnica, ProgresoEstudiante

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'es_profesor', 'es_estudiante')
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('es_profesor', 'es_estudiante')}),
    )

admin.site.register(Tecnica)
admin.site.register(ProgresoEstudiante)
