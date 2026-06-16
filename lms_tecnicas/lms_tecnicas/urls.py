from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('dashboard_estudiante')),
    path('', include('tecnicas.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
