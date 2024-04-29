from typing import Any
from .decorators import add_color_to_context
from django.http.response import HttpResponseRedirect
from .decorators import add_color_to_context
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from localidad.models import Region, Comuna
from .models import Estudiante
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
# ____________________________________________________________________________________

# Create your views here.
@add_color_to_context
class EstudianteView(View):
    estudiantes = Estudiante
    def get(self, request):
        estudiantes = Estudiante.objects.all()
        print(estudiantes)  # Esto imprimirá la consulta de estudiantes en la consola del servidor
        context = {'estudiantes': estudiantes}
        print(context)  # Esto imprimirá el contexto en la consola del servidor
        return render(request, 'pie/estudiantes.html', context)
