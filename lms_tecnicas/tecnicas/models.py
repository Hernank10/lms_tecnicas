from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

class Usuario(AbstractUser):
    es_profesor = models.BooleanField(default=False)
    es_estudiante = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_lms',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_lms',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.username

class Tecnica(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    contenido_html = models.TextField(help_text="HTML completo de la técnica")
    grado = models.CharField(max_length=50, blank=True, null=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden']
        db_table = 'tecnicas'

    def __str__(self):
        return self.titulo

class ProgresoEstudiante(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tecnica = models.ForeignKey(Tecnica, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)
    ultima_respuesta = models.TextField(blank=True)
    intentos = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['estudiante', 'tecnica']
        db_table = 'progreso_estudiante'

    def __str__(self):
        return f"{self.estudiante.username} - {self.tecnica.titulo}"
