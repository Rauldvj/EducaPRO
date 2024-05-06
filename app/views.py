from typing import Any
from django.http.response import HttpResponseRedirect
from accounts.models import Profile
from app.models import Anamnesis
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from .forms import RegisterUserForm, UserForm, ProfileForm, UserCreationForm, AnamnesisForm
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from .funciones import plural_singular # Importa la función plural_singular
from .models import Region, Comuna  # Importa los modelos Region y Comuna
from .decorators import add_group_name_to_context, get_group_and_color
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin # Importamos la clase UserPassesTestMixin para proteger las vistas URLs
import os # Importamos la librería os
from django.conf import settings    # Importamos la configuración de Django
from django.contrib.auth.views import PasswordChangeView  # Importamos la clase PasswordChangeView
from django.contrib.auth import update_session_auth_hash # Importamos la clase update_session_auth_hash
from django.contrib.auth.views import LoginView # Importamos la clase LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


# Usamos el decorador `add_group_name_to_context` para agregar el nombre del grupo al contexto de la vista
@add_group_name_to_context
class ProfileView(TemplateView):  
    template_name = 'profiles/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()

        # Agregamos los formularios de usuario y perfil al contexto
        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        context['regiones'] = regiones
        context['comunas'] = comunas

        # Si el usuario pertenece al grupo 'Coordinadores', realizamos algunas operaciones adicionales
        if user.groups.first().name == 'Coordinadores':
            # Obtenemos el objeto del grupo 'Coordinadores'
            coordinadores_groups = Group.objects.get(name='Coordinadores')
            # Excluimos a los usuarios que pertenecen al grupo 'Coordinadores' y 'Administradores' para evitar duplicados
            all_users = User.objects.exclude(groups__in=[coordinadores_groups])
            all_users = all_users.exclude(groups__name='Administradores')
            
            # Obtenemos el grupo seleccionado del filtro, si existe
            selected_group = self.request.GET.get('group')
            if selected_group:
                all_users = all_users.filter(groups__name=selected_group)

            # Obtenemos todos los grupos disponibles, excluyendo 'Coordinadores' y 'Administradores'
            all_groups = Group.objects.exclude(name__in=['Coordinadores', 'Administradores', 'Funcionarios'])
            user_profiles = []

            # Iteramos sobre los usuarios obtenidos y construimos sus perfiles para mostrar en la vista
            for user in all_users:
                profile = user.profile
                user_groups = user.groups.all()
                processed_groups = [plural_singular(group.name) for group in user_groups]

                user_profiles.append({
                    'user': user,
                    'groups': processed_groups,
                    'profile': profile
                })
                
            # Agregamos los perfiles de usuario y grupos al contexto
            context['user_profiles'] = user_profiles
            context['all_groups'] = all_groups
            
            # Realizamos la paginación de los perfiles de usuario
            profiles_pages = 5
            paginator = Paginator(user_profiles, profiles_pages)
            number_page = self.request.GET.get('page')

            try:
                profiles_paginated = paginator.page(number_page)
            except PageNotAnInteger:
                profiles_paginated = paginator.page(1)
            except EmptyPage:
                profiles_paginated = paginator.page(paginator.num_pages)

            context['user_profiles'] = profiles_paginated

        return context
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = UserForm(data=request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('profile')

        # Si los formularios no son válidos, volvemos a Renderizar la vista con los datos y los errores
        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render(request, 'profiles/profile.html', context)


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
        context = super().get_context_data(**kwargs) #Obtenemos el contexto


        # Obtenemos todos los grupos disponibles, excluyendo los grupos 'Funcionarios' y 'Administradores'
        groups = Group.objects.exclude(name__in=['Administradores', 'Funcionarios'])
        singular_groups = [plural_singular(group.name).capitalize() for group in groups] # Obtener los nombres singulares de los grupos
        context['groups'] = zip(groups, singular_groups) #unimos las 2 variables de grupos para obtener el singular del grupo

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

#VISTA BASADA EN CLASES PARA LA VIEW DE PERFIL DETALLADO DE UN USUARIO

@add_group_name_to_context
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        group_id, group_name, group_name_singular, color = get_group_and_color(user)
        
        # Obtener las opciones de región y comuna
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()

        #Obtengo todos los grupos
        groups = Group.objects.all()
        singular_names = [plural_singular(group.name).capitalize() for group in groups] # Obtener los nombres singulares de los grupos
        groups_ids = [group.id for group in groups]
        singular_groups = zip(singular_names, groups_ids) #unimos las 2 variables de grupos para obtener el singular del grupo

        context['regiones'] = regiones
        context['comunas'] = comunas
        context['singular_groups'] = singular_groups
        context['group_id_user'] = group_id
        context['group_name_user'] = group_name
        context['group_name_singular_user'] = group_name_singular
        context['color_user'] = color

        return context

def superuser_edit(request, user_id):

    #Verificamos si es Super Usuario o no
    if not request.user.is_superuser:
        return redirect('error')

    user = User.objects.get(pk=user_id)

    #Verificamos los datos que ingresamos en el formulario
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        group = request.POST.get('group')

        #validación del formulario
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            user.groups.clear()
            user.groups.add(group)

            messages.success(request, 'Usuario editado exitosamente')
            return redirect('profile_detail', pk=user.pk)

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profiles/profile_detail.html', context)
    


    
# ___________________________________________________________________________________________________________________________

#VISTA BASADA EN FUNCIONES PARA EL FORMULARIO DEL ANAMNESIS
@add_group_name_to_context
class AnamnesisView(CreateView):
    model = Anamnesis #importamos el modelo Anamnesis
    form_class = AnamnesisForm
    template_name = 'informes/anamnesis.html'
    success_url = reverse_lazy('home')
    

    
    

