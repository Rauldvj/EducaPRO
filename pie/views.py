from typing import Any
from django.http.response import HttpResponseRedirect
from app.decorators import add_group_name_to_context
from .models import RegistroPie
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
from django.contrib.auth.views import LoginView # Importamos la clase LoginView
# ____________________________________________________________________________________
# Create your views here.

@add_group_name_to_context
class ListPieView(ListView):
    model = RegistroPie
    template_name = 'pie/pie.html'
    context_object_name = 'pies'  # Nombre del objeto de contexto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


#_________________________________________________________________________________________________________________
