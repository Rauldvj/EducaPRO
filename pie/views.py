from typing import Any
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.decorators import add_group_name_to_context
from localidad.models import Region, Comuna
from estudiantes.models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos
from .models import RegistroPie
from .forms import AddRegistroPieForm
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

# VISTA BASADA EN CLASES PARA LISTAR REGISTRO DEL PIE
@add_group_name_to_context
class ListPieView(ListView):
    model = RegistroPie
    template_name = 'pie/pie.html'
    context_object_name = 'pies'  # Nombre del objeto de contexto
    paginate_by = 10  # Número de elementos por página

    def get_context_data(self, **kwargs):
        # Recuperamos todos los registros de PIE
        context = super().get_context_data(**kwargs)
        
        # Obtener el filtro de curso desde la solicitud GET
        curso_filtro = self.request.GET.get('curso_filtro')
        
        # Filtrar los registros de PIE según el curso seleccionado
        if curso_filtro:
            pies_list = RegistroPie.objects.filter(curso=curso_filtro)
        else:
            pies_list = RegistroPie.objects.all()
        
        # Paginación
        paginator = Paginator(pies_list, self.paginate_by)
        number_page = self.request.GET.get('page')
        
        try:
            pies_paginated = paginator.page(number_page)
        except PageNotAnInteger:
            pies_paginated = paginator.page(1)
        except EmptyPage:
            pies_paginated = paginator.page(paginator.num_pages)
        
        context['pies'] = pies_paginated
        
        # Agregar las opciones de curso al contexto
        context['all_cursos'] = RegistroPie.objects.values_list('curso', flat=True).distinct()
        context['opciones_curso'] = Estudiante._meta.get_field('cursos').choices
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        
        return context
    

    
    


#_________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA AGREGAR REGISTRO DEL PIE

@add_group_name_to_context
class AddRegistroPieView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = RegistroPie
    template_name = 'pie/pie_detail.html'
    form_class = AddRegistroPieForm  # Aquí debe ser la clase del formulario, no una cadena de texto
    success_url = reverse_lazy('pie')

    #Creamos una función para que solo el coordinador y el administrador puedan registrar usuarios
    def test_func(self):
        return self.request.user.groups.first().name == 'Coordinadores' or self.request.user.groups.first().name == 'Administradores'
    
    #Función si el usuario no tiene permiso
    def handle_no_permission(self):
        return redirect('error')
    
     #Recuperamos los objetos del modelo PIE
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #Obtenemos el contexto

        context['pies'] = RegistroPie.objects.all()

        return context

    
    

    
