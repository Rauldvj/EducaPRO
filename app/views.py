from typing import Any
from django.shortcuts import redirect, render # Importamos render y redirect
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import TemplateView # Importamos la vista basada en clases
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from .forms import RegisterUserForm
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from .funciones import plural_singular

# ____________________________________________________________________________________________________________________________
#AQUÍ CREAREMOS UNA VISTA CUSTOMIZADA, A CUAL SE REUTILIZARA LAS VISTAS BASADAS EN CLASES

class CustomTemplateView(TemplateView):
    group_name = None # Variable para saber el grupo al que pertenece el usuario
    group_name_singular = None # Variable para saber el singular del grupo
    color = None # Variable para saber el color del grupo

    # FUNCION PARA SABER EL GRUPO AL QUE PERTENECE EL USUARIO Y DARLE EL COLOR ASIGNADO A ESE GRUPO
    def get_context_data(self, **kwargs): # Función para obtener la data
        context = super().get_context_data(**kwargs) # Obtenemos la data de la superclase
        user = self.request.user # Obtenemos el usuario que esta logeado
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first() # Obtenemos el grupo al que pertenece el usuario
            if group: # Si el grupo existe

                #PREGUNTAMOS POR EL GRUPO Y COLOR
                if group.name == 'Funcionarios':
                    self.color = 'bg-zinc-950'
                elif group.name == 'Administradores':
                    self.color = 'bg-gradient-to-tr from-gray-600 to-gray-900'
                elif group.name == 'Coordinadores':
                    self.color = 'bg-gradient-to-tr from-lime-600 to-lime-900'
                elif group.name == 'Psicopedagógos':
                    self.color = 'bg-gradient-to-tr from-purple-600 to-purple-900'
                elif group.name == 'Psicólogo':
                    self.color = 'bg-gradient-to-tr from-indigo-600 to-indigo-900'
                elif group.name == 'Terapeutas Ocupacionales':
                    self.color = 'red-600'
                elif group.name == 'Fonoaudiologos':
                    self.color = 'bg-gradient-to-tr from-amber-600 to-amber-900'
                elif group.name == 'Técnicos Diferenciales':
                    self.color = 'bg-gradient-to-tr from-pink-600 to-pink-900'
                elif group.name == 'Técnicos Parvularios':
                    self.color = 'bg-gradient-to-tr from-green-600 to-green-900'


                self.group_name = group.name # Asignamos el nombre del grupo
                self.group_name_singular = plural_singular(group.name) # Obtenemos el singular del grupo
        context['group_name'] = self.group_name # Asignamos el nombre del grupo
        context['group_name_singular'] = self.group_name_singular # Asignamos el singular del grupo
        context['color'] = self.color # Asignamos el color

        return context # Retornamos el context

# ____________________________________________________________________________________________________________________________


# VISTA BASADA EN CLASES DEL INDEX
class IndexView(TemplateView):
    template_name = 'index.html'
# ____________________________________________________________________________________________________________________________

# VISTA BASADA EN CLASES DEL HOME

class HomeView(CustomTemplateView):
    template_name = 'home.html'

# ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES DEL REGISTRO DE USUARIOS

class RegisterView(View):
    def get(self, request): #Definimos la función para mostrar el formulario de registro
        data = {
            'form': RegisterUserForm() #Definimos el formulario
        }
        return render(request, 'registration/registro.html', data) #Retornamos la vista con el formulario
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
#VISTA BASADA EN CLASES PARA EL PERFIL DEL USUARIO

class ProfileView(CustomTemplateView):  
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user #Obtenemos el usuario que esta logeado

        return context


# ____________________________________________________________________________________________________________________________
