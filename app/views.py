from typing import Any
from django.utils import timezone # Importamos la zona horaria
from django.http.response import HttpResponseRedirect
from accounts.models import Profile # Importamos el modelo Profile
from pie.models import Estudiante # Importamos el modelo Estudiante
from .models import Region, Comuna  # Importa los modelos Region y Comuna
from .models import BitacoraEstudiante, Asignatura
from app.models import Anamnesis, BitacoraEstudiante
from django.shortcuts import redirect, render # Importamos render y redirect
from django.urls import reverse_lazy, reverse # Importamos reverse_lazy
from django.views import View # Importamos la vista basada en clases
from django.contrib import messages  # Importamos mensajes
from django.views.generic import ListView, TemplateView, CreateView, DetailView # Importamos ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.models import Group # Importamos la estructura de los grupos de Django
from .forms import RegisterUserForm, UserForm, ProfileForm, UserCreationForm, AnamnesisForm
from django.contrib.auth.models import User # Importamos el modelo de usuario
from django.contrib.auth import authenticate, login, logout # Importamos la autenticación
from .funciones import plural_singular # Importa la función plural_singular

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
        return user.groups.filter(name__in=['Coordinadores', 'Coordinadores Suplentes', 'Administradores']).exists()
    
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

        # Obtenemos todos los grupos disponibles, excluyendo los grupos 'Funcionarios' y 'Administradores'
        groups = Group.objects.exclude(name__in=['Administradores', 'Funcionarios'])
        singular_groups = [plural_singular(group.name).capitalize() for group in groups] # Obtener los nombres singulares de los grupos
        context['groups'] = zip(groups, singular_groups) # Unimos las 2 variables de grupos para obtener el singular del grupo


        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        context['regiones'] = regiones
        context['comunas'] = comunas

        if user.groups.first().name in ['Coordinadores', 'Coordinadores Suplentes']:
            coordinadores_groups = Group.objects.get(name='Coordinadores')
            all_users = User.objects.exclude(groups__in=[coordinadores_groups])
            all_users = all_users.exclude(groups__name='Administradores')
            
            selected_group = self.request.GET.get('group')
            if selected_group:
                all_users = all_users.filter(groups__name=selected_group)

            all_groups = Group.objects.exclude(name__in=['Coordinadores', 'Administradores', 'Funcionarios'])
            user_profiles = []

            for user in all_users:
                profile = user.profile
                user_groups = user.groups.all()
                processed_groups = [plural_singular(group.name) for group in user_groups]

                user_profiles.append({
                    'user': user,
                    'groups': processed_groups,
                    'profile': profile
                })
                
            context['user_profiles'] = user_profiles
            context['all_groups'] = all_groups
            
            profiles_pages = 6
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

#VISTA PARA RESET DE CONTRASEÑA

class ResetPasswordView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes']).exists()

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.set_password('contraseña')
            user.save()

            # Verificar y establecer is_staff y creado_por_coordinador
            group_id = user.groups.first().id
            if group_id not in [2, 3]:
                user.is_staff = True
                user.save()

            profile = Profile.objects.get(user=user)
            profile.creado_por_coordinador = True
            profile.save()

            messages.success(request, 'Contraseña restablecida exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        return redirect('profile_detail', pk=user_id)

# ____________________________________________________________________________________________________________________________
#VISTA PARA ELIMINAR UN USUARIO

class DeleteUserView(UserPassesTestMixin, LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administradores', 'Coordinadores', 'Coordinadores Suplentes']).exists()

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            messages.success(request, 'Usuario eliminado exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        return redirect('profile')

#____________________________________________________________________________________________________________________________
#CREAMOS UN NUEVO USUARIO DESDE EL ROL DE UN COORDINADOR O ADMINISTRADOR

#VISTA BASADA EN CLASES DE REGISTRO DE USUARIOS (COORDINADORES Y ADMINISTRADORES)

@add_group_name_to_context
class AddUserView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'profiles/add_user.html'
    success_url = '/profile/'

    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores', 'Coordinadores Suplentes']
    
    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.exclude(name__in=['Administradores', 'Funcionarios', 'Coordinadores'])
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        return context
    
    def form_valid(self, form):
        group_id = self.request.POST['group']
        group = Group.objects.get(id=group_id)
        user = form.save(commit=False)
        user.set_password('contraseña')
        if group_id not in ['2', '3']:
            user.is_staff = True
        user.save()
        user.groups.clear()
        user.groups.add(group)
        messages.success(self.request, 'Usuario creado exitosamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        if User.objects.filter(username=form.data.get('username')).exists():
            messages.error(self.request, 'El usuario ya existe.')
        else:
            messages.error(self.request, 'Error en el formulario. Por favor, revise los datos ingresados.')
        return redirect('profile')
    

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
        current_user = self.request.user
        group_id, group_name, group_name_singular, color = get_group_and_color(user)
        
        # Obtener las opciones de región y comuna
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()

        # Obtenemos todos los grupos disponibles, excluyendo los grupos 'Funcionarios' y 'Administradores'
        groups = Group.objects.exclude(name__in=['Coordinadores', 'Administradores', 'Funcionarios'])
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)

        context['regiones'] = regiones
        context['comunas'] = comunas
        context['group_id_user'] = group_id
        context['group_name_user'] = group_name
        context['group_name_singular_user'] = group_name_singular
        context['color_user'] = color

        # Verificar si el usuario actual es un "Coordinador Suplente"
        context['is_coordinador_suplente'] = current_user.groups.filter(name='Coordinadores Suplentes').exists()

        return context

# Editamos un usuario según su pk
def superuser_edit(request, user_id):
    user = User.objects.get(pk=user_id)
    current_user = request.user

    # Verificamos si es Super Usuario o "Coordinador Suplente"
    if not current_user.is_superuser and not current_user.groups.filter(name='Coordinadores Suplentes').exists():
        return redirect('error')

    # Verificamos los datos que ingresamos en el formulario
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        group = request.POST.get('group')

        # Validación del formulario
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Evitar que los "Coordinadores Suplentes" cambien su propio grupo
            if current_user != user or current_user.is_superuser:
                user.groups.clear()
                user.groups.add(group)

            messages.success(request, 'Usuario editado exitosamente')
            return redirect('profile_detail', pk=user.pk)

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_coordinador_suplente': current_user.groups.filter(name='Coordinadores Suplentes').exists()
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
    

# ____________________________________________________________________________________________________________________________






# ____________________________________________________________________________________________________________________________




