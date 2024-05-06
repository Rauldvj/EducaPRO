from typing import Any
from django.http.response import HttpResponseRedirect
from app.decorators import add_group_name_to_context
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from localidad.models import Region, Comuna
from .models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos
from .forms import AddEstudianteForm, AddApoderadoTitularForm, AddApoderadoSuplenteUnoForm, AddApoderadoSuplenteDosForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
# ____________________________________________________________________________________

# Create your views here.

# VISTA BASADA EN CLASES PARA AGREGAR UN ESTUDIANTE


@add_group_name_to_context
class AddEstudianteView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Estudiante  # Modelo que se utilizará para crear al estudiante.
    template_name = 'pie/add_estudiante.html'  # Template que se utilizará para mostrar el formulario de registro del estudiante.
    form_class = AddEstudianteForm  #Especificamos la clase de formulario que se utilizará para el estudiante.
    success_url = reverse_lazy('pie')  # Especificamos la URL a la que se redirigirá después de un registro exitoso.

    # Función  que verifica si el usuario actual tiene permiso para acceder a esta vista.
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Función que se ejecuta cuando un usuario no tiene permiso para acceder a esta vista y lo redirige a una página de error.
    def handle_no_permission(self):
        return redirect('error')

    # Función que agrega datos adicionales al contexto opciones de etnia, regiones y comunas.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        
        return context

    # Función que se ejecuta cuando el formulario es válido, muestra un mensaje de éxito y procede con la operación de registro.
    def form_valid(self, form):
        messages.success(self.request, 'Estudiante agregado exitosamente')
        return super().form_valid(form)

    # Función que se ejecuta cuando el formulario es inválido, muestra un mensaje de error y vuelve a mostrar el formulario.
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

# -------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA REGISTRAR UN APODERADO TITULAR

@add_group_name_to_context
class AddApoderadoTitularView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = ApoderadoTitular  # Modelo apoderado titular.
    template_name = 'pie/add_apoderado_titular.html'  # Template que se utilizará para mostrar el formulario de registro.
    form_class = AddApoderadoTitularForm  # Especificamos el formulario que se utilizará para registrar un apoderado.
    success_url = reverse_lazy('pie')  # Se especifica la URL a la que se redirigirá después de un registro exitoso.

    # Función que verifica si el usuario actual tiene permiso para acceder a esta vista.
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Función que se ejecuta cuando un usuario no tiene permiso para acceder a esta vista y lo redirige a una página de error.
    def handle_no_permission(self):
        return redirect('error')

    # La siguiente función agrega datos adicionales al contexto del formulario antes de que se muestre.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opciones_etnia'] = ApoderadoTitular._meta.get_field('etnia').choices
        context['apoderado_titular'] = ApoderadoTitular.objects.all()
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['opciones_salud'] = ApoderadoTitular._meta.get_field('salud').choices
        
        return context

    # Función que se ejecuta cuando el formulario es válido, muestra un mensaje de éxito y procede con la operación de registro.
    def form_valid(self, form):
        messages.success(self.request, 'Apoderado Titular agregado exitosamente')
        return super().form_valid(form)

    # Función que se ejecuta cuando el formulario es inválido, muestra un mensaje de error y vuelve a mostrar el formulario.
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    

# -------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA AGREGAR UN APODERADO SUPLENTE UNO

@add_group_name_to_context
class AddApoderadoSuplenteUnoView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = ApoderadoSuplenteUno  # Modelo que se utilizará para crear al apoderado suplente dos.
    template_name = 'pie/add_apoderado_suplente_uno.html'  #Template que se utilizará para mostrar el formulario de registro del apoderado suplente uno.
    form_class = AddApoderadoSuplenteUnoForm  # Especificamos la clase de formulario que se utilizará para el apoderado suplente uno.
    success_url = reverse_lazy('pie')  # URL a la que se redirigirá después de un registro exitoso.

    # Función que verifica si el usuario actual tiene permiso para acceder a esta vista.
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Función que se ejecuta cuando un usuario no tiene permiso para acceder a esta vista y lo redirige a una página de error.
    def handle_no_permission(self):
        return redirect('error')

    # Función que agrega datos adicionales al contexto del formulario antes de que se muestre.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_suplente_uno'] = ApoderadoSuplenteUno.objects.all()
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        
        return context

    # Función que se ejecuta cuando el formulario es válido, muestra un mensaje de éxito y procede con la operación de registro.
    def form_valid(self, form):
        messages.success(self.request, 'Apoderado Suplente Uno agregado exitosamente')
        return super().form_valid(form)

    #Función que se ejecuta cuando el formulario es inválido, muestra un mensaje de error y vuelve a mostrar el formulario.
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)
    

# -------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA AGREGAR UN APODERADO SUPLENTE DOS

@add_group_name_to_context
class AddApoderadoSuplenteDosView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = ApoderadoSuplenteDos  # Modelo que se utilizará para crear al apoderado suplente dos.
    template_name = 'pie/add_apoderado_suplente_dos.html'  #Template que se utilizará para mostrar el formulario de registro del apoderado suplente dos.
    form_class = AddApoderadoSuplenteDosForm  # Especificamos la clase de formulario que se utilizará para el apoderado suplente dos.
    success_url = reverse_lazy('pie')  # URL a la que se redirigirá después de un registro exitoso.

    # Función que verifica si el usuario actual tiene permiso para acceder a esta vista.
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Función que se ejecuta cuando un usuario no tiene permiso para acceder a esta vista y lo redirige a una página de error.
    def handle_no_permission(self):
        return redirect('error')

    # Función que agrega datos adicionales al contexto del formulario antes de que se muestre.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_suplente_uno'] = ApoderadoSuplenteDos.objects.all()
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        
        return context

    # Función que se ejecuta cuando el formulario es válido, muestra un mensaje de éxito y procede con la operación de registro.
    def form_valid(self, form):
        messages.success(self.request, 'Apoderado Suplente Uno agregado exitosamente')
        return super().form_valid(form)

    #Función que se ejecuta cuando el formulario es inválido, muestra un mensaje de error y vuelve a mostrar el formulario.
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)
