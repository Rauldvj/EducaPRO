from typing import Any
from django.http.response import HttpResponseRedirect
from accounts.models import Profile
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from .forms import RegisterUserForm, UserForm, ProfileForm, UserCreationForm
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from .funciones import plural_singular # Importa la función plural_singular
from .models import Region, Comuna  # Importa los modelos Region y Comuna
from .decorators import add_group_name_to_context
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
from django.contrib.auth.views import LoginView # Importamos la clase LoginView
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
        user = self.request.user  # Obtenemos el usuario que está logeado

        # Obtener las opciones de región y comuna
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()

        context['user_form'] = UserForm(instance=user)  # Agregar el formulario de usuario al contexto
        context['profile_form'] = ProfileForm(instance=user.profile)  # Agregar el formulario de perfil al contexto

        # Agregar las opciones de región y comuna al contexto
        context['regiones'] = regiones
        context['comunas'] = comunas

        
    
    #LLAMAMOS A LOS GRUPOS PARA OBTENER LOS USUARIOS
        if user.groups.first().name == 'Coordinadores':

            #Obtenemos todos los usuarios
            all_users = User.objects.all()

            #Obtenemos todos los grupos
            all_groups = Group.objects.all()

            #Obtenemos cada perfil de usuario
            user_profiles = []

            #Iteramos en los perfiles
            for user in all_users:
                profile = user.profile
                user_groups = user.groups.all()
                processed_groups = [plural_singular(group.name) for group in user_groups]

                #Guardamos esta información en esta variable
                user_profiles.append({
                    'user': user,
                    'groups': processed_groups,
                    'profile': profile
                })
            context['user_profiles'] = user_profiles
            context['all_groups'] = all_groups
            

        return context
    
    #FUNCION PARA GRABAR LOS DATOS
    def post(self, request, *args, **kwargs):
        user = self.request.user # Obtenemos el usuario que está logeado
        user_form = UserForm(data=request.POST, instance=user) # Definimos el formulario con los datos del POST 
        profile_form = ProfileForm(data=request.POST, instance=user.profile) # Definimos el formulario con los datos del POST

        #Preguntamos si el user_form y el profile_form son validos
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Guardamos el formulario de usuario y obtenemos la instancia actualizada
            profile_form.save() # Guardamos el formulario de perfil
            messages.success(request, 'Perfil actualizado exitosamente') # Mostramos un mensaje de éxito
            return redirect('profile') # Redireccionamos al perfil
        
        # Si alguno de estos datos "NO SON VALIDOS"
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render (request, 'profiles/profile.html', context)


# ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA CAMBIAR LA CONTRASEÑA DEL USUARIO

@add_group_name_to_context
class ProfilePasswordChangeView(PasswordChangeView):
    template_name = 'profiles/change_password.html'
    success_url = reverse_lazy('profile')

    #Definimos la función para realizar el cambio de contraseña
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_changed'] = self.request.session.get('password_changed', False) #Obtenemos el valor de la variable de sesión
        return context
    
    #Validamos el formulario de cambio de contraseña
    def form_valid(self, form):

        #Actualizamos el campo "creado_por_coordinador" del modelo Profile
        profile = Profile.objects.get(user=self.request.user)
        profile.creado_por_coordinador = False
        profile.save()


        messages.success(self.request, 'Contraseña cambiada exitosamente')

        #Actualizamos la sesión logeada con la contraseña nueva cambiada
        update_session_auth_hash(self.request, form.user)
        self.request.session['profile_password_changed'] = True
        return super().form_valid(form)
    
    #Si el formulario no es valido
    def form_invalid(self, form):
        messages.error(self.request, 'Error al cambiar la contraseña')
        return super().form_invalid(form)


# ____________________________________________________________________________________________________________________________

#CREAMOS UN NUEVO USUARIO DESDE EL ROL DE UN COORDINADOR O ADMINISTRADOR

#VISTA BASADA EN CLASES DE REGISTRO DE USUARIOS (COORDINADORES Y ADMINISTRADORES)

@add_group_name_to_context
class AddUserView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'profiles/add_user.html'
    success_url = '/profile/'

    #Creamos una función para que solo el coordinador y el administrador puedan registrar usuarios
    def test_func(self):
        return self.request.user.groups.first().name == 'Coordinadores' or self.request.user.groups.first().name == 'Administradores'
    
    #Función si el usuario no tiene permiso
    def handle_no_permission(self):
        return redirect('error')


    #Recuperamos los grupos y su singular
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)

        return context
    
    #Función para validad y almacenar los datos del formulario
    def form_valid(self, form):

        #Obtener el grupo que se selecciono
        group_id = self.request.POST['group']

        #Obtener el grupo
        group = Group.objects.get(id=group_id)

        #Creamos un usuario sin guardarlo aun
        user = form.save(commit=False)

        #Al nuevo usuario se le asigna la contraseña por defecto "contraseña"
        user.set_password('contraseña')

        # Convertir al usuario a staff solo si el grupo es '2'(Administradores) o '3' (Coordinadores) 
        if group_id != ['2', '3']:
            user.is_staff = True

        #Creamos al nuevo usuario
        user.save()

        #Limpiamos o eliminamos al usuario que se crea por defecto en el grupo de "Funcionarios"
        user.groups.clear()

        #Agregamos al usuario al grupo seleccionado en el formulario
        user.groups.add(group)

        messages.success(self.request, 'Usuario creado exitosamente')

        return super().form_valid(form)
    

    # ____________________________________________________________________________________________________________________________

#VISTA BASADA EN CLASES PARA LA VIEW DE LOGIN PERSONALIZADO
#Este login evaluara si es nuevo usuario y si es asi lo va a redireccionar a cambiar la contraseña
@add_group_name_to_context
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)

        #Accedemos al perfil de usuario
        profile = self.request.user.profile

        #Verificamos el valor del campo "creado por el coordinador del modelo Profile"
        if profile.creado_por_coordinador:
            messages.warning(self.request, 'Bienvenido, debe cambiar su contraseña ahora!')
            response['Location'] = reverse_lazy('profile_password_change')
            response.status_code = 302

        return response
    
    def get_success_url(self):
        return super().get_success_url()


# ____________________________________________________________________________________________________________________________