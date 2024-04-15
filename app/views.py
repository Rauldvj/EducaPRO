from typing import Any
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render # Importamos render y redirect
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import TemplateView # Importamos la vista basada en clases
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from .forms import RegisterUserForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from .funciones import plural_singular
from .models import Region, Comuna  # Importa los modelos Region y Comuna
from .decorators import add_group_name_to_context
from django.contrib.auth.mixins import UserPassesTestMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
# ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA LA VIEW DE ERROR
@add_group_name_to_context
class ErrorView(TemplateView):
    template_name = 'error.html'

    #FUNCIÓN PARA MOSTRAR LA IMAGEN DE ERROR
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_image = os.path.join(settings.MEDIA_ROOT, 'error.png')
        context['error_image'] = error_image
        return context

# ____________________________________________________________________________________________________________________________


# VISTA BASADA EN CLASES DEL INDEX
class IndexView(TemplateView):
    template_name = 'index.html'
# ____________________________________________________________________________________________________________________________

# VISTA BASADA EN CLASES DEL HOME

@add_group_name_to_context # Decorador
class HomeView(TemplateView):
    template_name = 'home.html'

# ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES DEL REGISTRO DE USUARIOS

class RegisterView(UserPassesTestMixin, View):
    def get(self, request): #Definimos la función para mostrar el formulario de registro
        data = {
            'form': RegisterUserForm() #Definimos el formulario
        }
        return render(request, 'registration/registro.html', data) #Retornamos la vista con el formulario
    
    #ESTA FUNCION VERIFICA SI ERES COORDINADOR O ADMIN, SINO ARROGARA ERROR
    def test_func(self):
        user = self.request.user
        return user.groups.filter(name__in=['Coordinadores', 'Administradores']).exists()
    
    #FUNCION PARA REDIRIGIR A LA PAGINA QUE MUESTRA EL ERRO
    def handle_no_permission(self):
        return redirect('error')

    def post(self, request): #Definimos la función para registrar el usuario
        user_creation_form = RegisterUserForm(data=request.POST) #Definimos el formulario con los datos del POST
        if user_creation_form.is_valid(): #Preguntamos si el formulario es valido
            user_creation_form.save() #Guardamos el formulario
            user = authenticate(username=user_creation_form.cleaned_data['username'] , password=user_creation_form.cleaned_data['password1']) #Autenticamos el usuario y la contraseña
            login(request, user) #Logeamos el usuario
            messages.success(request, 'Usuario registrado exitosamente') #Mostramos un mensaje de éxito
            return redirect('home') #Redireccionamos al home
        
        data = { #Si el formulario no es valido
            'form': user_creation_form #Definimos el formulario
        }
        return render(request, "registration/registro.html", data) #Retornamos la vista con el formulario

# ____________________________________________________________________________________________________________________________


@add_group_name_to_context # Decorador Personalizado
class ProfileView(TemplateView):  
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Obtenemos el usuario que está logueado

        # Obtener las opciones de región y comuna
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()

        context['user_form'] = UserForm(instance=user)  # Agregar el formulario de usuario al contexto
        context['profile_form'] = ProfileForm(instance=user.profile)  # Agregar el formulario de perfil al contexto

        # Agregar las opciones de región y comuna al contexto
        context['regiones'] = regiones
        context['comunas'] = comunas

        return context
    
    #FUNCION PARA GRABAR LOS DATOS
    def post(self, request, *args, **kwargs):
        user = self.request.user # Obtenemos el usuario que está logueado
        user_form = UserForm(data=request.POST, instance=user) # Definimos el formulario con los datos del POST 
        profile_form = ProfileForm(data=request.POST, instance=user.profile) # Definimos el formulario con los datos del POST

        #Preguntamos si el user_form y el profile_form son validos
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Guardamos el formulario de usuario y obtenemos la instancia actualizada
            profile_form.save() # Guardamos el formulario de perfil
            messages.success(request, 'Perfil actualizado exitosamente') # Mostramos un mensaje de éxito
            return redirect('perfil') # Redireccionamos al perfil
        
        # Si alguno de estos datos "NO SON VALIDOS"
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render (request, 'profiles/profile.html', context)


# ____________________________________________________________________________________________________________________________
