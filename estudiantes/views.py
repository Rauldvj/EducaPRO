# Importaciones de Django core
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import (
    ListView, 
    TemplateView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
)

# Importaciones de terceros
from weasyprint import HTML

# Importaciones del proyecto
from accounts.models import Profile
from app.decorators import add_group_name_to_context
from app.funciones import plural_singular
from app.models import Asignatura, BitacoraEstudiante
from localidad.models import Region, Comuna
from pie.models import RegistroPie
from .forms import (
    EstudianteForm, 
    ApoderadoTitularForm, 
    ApoderadoSuplenteUnoForm, 
    ApoderadoSuplenteDosForm, 
    BitacoraEstudianteForm
)
from .models import (
    Estudiante, 
    ApoderadoTitular, 
    ApoderadoSuplenteUno, 
    ApoderadoSuplenteDos
)

# Importaciones de Python estándar
import json
import os
from datetime import datetime
# ____________________________________________________________________________________

    # Create your views here.

    # VISTA BASADA EN CLASES PARA AGREGAR UN ESTUDIANTE


@add_group_name_to_context
class AddEstudianteView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Estudiante  # Modelo que se utilizará para crear al estudiante.
    template_name = 'pie/add_estudiante.html'  # Template que se utilizará para mostrar el formulario de registro del estudiante.
    form_class = EstudianteForm  #Especificamos la clase de formulario que se utilizará para el estudiante.
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
        context['opciones_curso'] = Estudiante._meta.get_field('cursos').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        return context
        
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
#VISTA BASADA EN CLASES PARA EDITAR A  UN ESTUDIANTE
@add_group_name_to_context
class EstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Estudiante
    template_name = 'pie/estudiante_edit.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('estudiante')

    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']
    
    def handle_no_permission(self):
        return redirect('error')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiante'] = self.object
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['opciones_curso'] = Estudiante._meta.get_field('cursos').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Estudiante actualizado exitosamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.pk})


# -------------------------------------------------------------------------------------------------------------------
#VISTA BASADA EN CLASES PARA VER EL DETALLE DE UN ESTUDIANTE Y LOS APODERADOS
@add_group_name_to_context
class EstudianteDetailView(LoginRequiredMixin, DetailView):
    model = Estudiante
    template_name = 'pie/estudiante.html'
    context_object_name = 'estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtenemos el Estudiante
        estudiante = self.get_object()

        # Obtener el apoderado titular del estudiante
        apoderado_titular = estudiante.apoderadotitular

        # Obtener el apoderado suplente uno del estudiante
        apoderado_suplente_uno = estudiante.apoderadosuplenteuno

        # Obtener el apoderado suplente dos del estudiante
        apoderado_suplente_dos = estudiante.apoderadosuplentedos

        # Agregar los apoderados al contexto
        context['apoderado_titular'] = apoderado_titular
        context['apoderado_suplente_uno'] = apoderado_suplente_uno
        context['apoderado_suplente_dos'] = apoderado_suplente_dos
        context['opciones_curso'] = Estudiante._meta.get_field('cursos').choices
        context['opciones_etnia'] = Estudiante._meta.get_field('etnia').choices
        context['opciones_salud'] = ApoderadoTitular._meta.get_field('salud').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        return context


# -------------------------------------------------------------------------------------------------------------------
# VISTA BASADA EN CLASES PARA DETALLE DE UN APODERADO TITULAR
@add_group_name_to_context
class ApoderadoTitularDetailView(LoginRequiredMixin, DetailView):
    model = ApoderadoTitular
    template_name = 'pie/apoderado_titular_edit.html'
    context_object_name = 'apoderado_titular'
# -------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA EDITAR UN APODERADO TITULAR
@add_group_name_to_context
class ApoderadoTitularUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = ApoderadoTitular
    template_name = 'pie/apoderado_titular_edit.html'
    form_class = ApoderadoTitularForm
    success_url = reverse_lazy('estudiante')  # Lo ajustaremos más abajo

    # Verifica si el usuario actual tiene permiso para acceder a esta vista
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Redirige a una página de error si el usuario no tiene permisos
    def handle_no_permission(self):
        return redirect('error')

    # Añadir datos adicionales al contexto, como opciones de etnia y salud, regiones y comunas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_titular'] = self.object
        context['opciones_etnia'] = ApoderadoTitular._meta.get_field('etnia').choices
        context['opciones_salud'] = ApoderadoTitular._meta.get_field('salud').choices
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        return context

    # Actualiza también el apoderado titular en el RegistroPie correspondiente cuando el formulario es válido
    def form_valid(self, form):
        # Guardar los cambios en el ApoderadoTitular
        response = super().form_valid(form)
        
        # Buscar y actualizar el RegistroPie correspondiente al estudiante
        try:
            registro_pie = RegistroPie.objects.get(estudiante=self.object.estudiante)
            registro_pie.apoderado_titular = self.object  # Asigna el apoderado titular actualizado
            registro_pie.save()  # Guarda los cambios en RegistroPie
        except RegistroPie.DoesNotExist:
            pass  # Si no existe un registro PIE, no hace nada
        
        # Mensaje de éxito
        messages.success(self.request, 'Apoderado Titular actualizado exitosamente.')
        return response

    # Manejar el caso de un formulario inválido
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    # Redirigir al detalle del estudiante tras una actualización exitosa
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})  # Redirige al detalle del estudiante


# -------------------------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA DETALLE DE UN APODERADO SUPLENTE UN***********************************************
@add_group_name_to_context
class ApoderadoSuplenteUnoDetailView(LoginRequiredMixin, DetailView):
    model = ApoderadoSuplenteUno
    template_name = 'pie/apoderado_suplente_uno.html'
    context_object_name = 'apoderado_suplente_uno'

#---------------------------------------------------------------------------------------********************************************************************************************----------------------------------------------
#VISTA BASADA EN CLASES PARA EDITAR UN APODERADO SUPLENTE UNO
@add_group_name_to_context
class ApoderadoSuplenteUnoUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = ApoderadoSuplenteUno
    template_name = 'pie/apoderado_suplente_uno_edit.html'
    form_class = ApoderadoSuplenteUnoForm
    success_url = reverse_lazy('estudiante')  # Lo ajustaremos más abajo

    # Verifica si el usuario actual tiene permiso para acceder a esta vista
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Redirige a una página de error si el usuario no tiene permisos
    def handle_no_permission(self):
        return redirect('error')
    
    # Añadir datos adicionales al contexto, como regiones y comunas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_suplente_uno'] = self.object
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        return context
    
    # Actualiza también el apoderado titular en el RegistroPie correspondiente cuando el formulario es válido
    def form_valid(self, form):
        # Guardar los cambios en el ApoderadoSuplenteUno
        response = super().form_valid(form)
        
        # Buscar y actualizar el RegistroPie correspondiente al estudiante
        try:
            registro_pie = RegistroPie.objects.get(estudiante=self.object.estudiante)
            registro_pie.apoderado_suplente_uno = self.object  # Asigna el apoderado suplente uno actualizado
            registro_pie.save()  # Guarda los cambios en RegistroPie
        except RegistroPie.DoesNotExist:
            pass  # Si no existe un registro PIE, no hace nada
        
        # Mensaje de éxito 
        messages.success(self.request, 'Apoderado Suplente Uno actualizado exitosamente.')
        return response
    
    # Manejar el caso de un formulario inválido
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    # Redirigir al detalle del estudiante tras una actualización exitosa
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})

# -------------------------------------------------------------------------------------------------------------------

# VISTA BASADA EN CLASES PARA DETALLE DE UN APODERADO SUPLENTE 2
@add_group_name_to_context
class ApoderadoSuplenteDosDetailView(LoginRequiredMixin, DetailView):
    model = ApoderadoSuplenteDos
    template_name = 'pie/apoderado_suplente_dos.html'
    context_object_name = 'apoderado_suplente_dos'
# -------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------********************************************************************************************----------------------------------------------
#VISTA BASADA EN CLASES PARA EDITAR UN APODERADO SUPLENTE DOS
@add_group_name_to_context
class ApoderadoSuplenteDosUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = ApoderadoSuplenteDos
    template_name = 'pie/apoderado_suplente_dos_edit.html'
    form_class = ApoderadoSuplenteDosForm
    success_url = reverse_lazy('estudiante')  # Lo ajustaremos más abajo

    # Verifica si el usuario actual tiene permiso para acceder a esta vista
    def test_func(self):
        return self.request.user.groups.first().name in ['Coordinadores', 'Administradores']

    # Redirige a una página de error si el usuario no tiene permisos
    def handle_no_permission(self):
        return redirect('error')
    
    # Añadir datos adicionales al contexto, como regiones y comunas
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apoderado_suplente_dos'] = self.object
        context['regiones'] = Region.objects.all()
        context['comunas'] = Comuna.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        return context
    
    # Actualiza también el apoderado titular en el RegistroPie correspondiente cuando el formulario es válido
    def form_valid(self, form):
        # Guardar los cambios en el ApoderadoSuplenteUno
        response = super().form_valid(form)
        
        # Buscar y actualizar el RegistroPie correspondiente al estudiante
        try:
            registro_pie = RegistroPie.objects.get(estudiante=self.object.estudiante)
            registro_pie.apoderado_suplente_dos = self.object  # Asigna el apoderado suplente uno actualizado
            registro_pie.save()  # Guarda los cambios en RegistroPie
        except RegistroPie.DoesNotExist:
            pass  # Si no existe un registro PIE, no hace nada
        
        # Mensaje de éxito 
        messages.success(self.request, 'Apoderado Suplente Dos actualizado exitosamente.')
        return response
    
    # Manejar el caso de un formulario inválido
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    # Redirigir al detalle del estudiante tras una actualización exitosa
    def get_success_url(self):
        return reverse('estudiante', kwargs={'pk': self.object.estudiante.pk})
    

# -------------------------------------------------------------------------------------------------------------------

#VISTA BASA EN CLASES PARA BITÁCORAS
# VISTA BASADA EN CLASES PARA REGISTRAR UNA BITACORA
# 
@add_group_name_to_context  
class AddBitacoraEstudianteView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = BitacoraEstudiante
    form_class = BitacoraEstudianteForm
    template_name = 'informes/add_bitacora_estudiante.html'

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        context['asignaturas'] = Asignatura.objects.all()
        context['profesionales'] = Profile.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['usuario_logueado'] = self.request.user  # Agrega el usuario logueado al contexto
        context['fecha_actual'] = timezone.now().date()  # Agrega la fecha actual al contexto
        context['estudiante'] = get_object_or_404(Estudiante, id=self.kwargs['estudiante_id'])  # Recupera el estudiante según el ID
        return context
    
    def form_valid(self, form):
        form.instance.profesional = Profile.objects.get(user=self.request.user)  # Asigna el profesional como el usuario logueado
        form.instance.estudiante_id = self.kwargs['estudiante_id']  # Asigna el ID del estudiante al formulario
        messages.success(self.request, 'Bitácora registrada exitosamente')  # Mensaje de éxito
        return super().form_valid(form)  # Guarda la bitácora
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario, corrija los errores')  # Mensaje de error
        return super().form_invalid(form)  # Retorna el formulario

    def get_success_url(self):
        return reverse('bitacora_estudiante_list', kwargs={'estudiante_id': self.kwargs['estudiante_id']})

# -------------------------------------------------------------------------------------------------------------------

#LISTA DE BITÁCORAS DE ESTUDIANTES


@add_group_name_to_context
class BitacoraEstudianteListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = BitacoraEstudiante
    template_name = 'informes/bitacoras_list.html'
    context_object_name = 'bitacoras'
    paginate_by = 6

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_queryset(self):
        estudiante_id = self.kwargs['estudiante_id']
        queryset = BitacoraEstudiante.objects.filter(estudiante_id=estudiante_id).order_by('-fecha')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profesionales'] = Profile.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['asignaturas'] = Asignatura.objects.all()
        context['estudiante'] = get_object_or_404(Estudiante, id=self.kwargs['estudiante_id'])
        context['bitacoras'] = self.get_queryset()
        context['bitacoras_json'] = json.dumps(list(self.get_queryset().values('id', 'actividad', 'fecha')), cls=DjangoJSONEncoder)
        return context
    


# -------------------------------------------------------------------------------------------------------------------


#VISTA BASADA EN CLASES PARA DETALLE DE UNA BITÁCORA DE UN ESTUDIANTE
@add_group_name_to_context
class BitacoraEstudianteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = BitacoraEstudiante
    template_name = 'informes/bitacora_estudiante.html'
    context_object_name = 'bitacora'

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bitacora = self.get_object()
        fecha_seleccionada = bitacora.fecha
        context['estudiante'] = bitacora.estudiante
        context['bitacoras'] = BitacoraEstudiante.objects.filter(estudiante=bitacora.estudiante, fecha=fecha_seleccionada)
        context['profesional'] = bitacora.profesional
        context['asignaturas'] = Asignatura.objects.all()
        context['logo_url'] = self.request.build_absolute_uri(static('Imagenes/logo_politecnico.jpg'))
        
        # Agregar el nombre del grupo en singular al contexto
        for bitacora in context['bitacoras']:
            bitacora.profesional.group_name_singular = plural_singular(bitacora.profesional.user.groups.first().name)
        
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'download' in request.GET:
            return self.download_pdf()
        return super().get(request, *args, **kwargs)

    def download_pdf(self):
        bitacora = self.get_object()
        context = self.get_context_data(object=bitacora)
        html_string = render_to_string('informes/bitacora_estudiante_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        estudiante = bitacora.estudiante
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        filename = f'bitacora_{estudiante.nombres}_{estudiante.apellido_paterno}_{estudiante.apellido_materno}_{fecha_actual}.pdf'

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
# -------------------------------------------------------------------------------------------------------------------

#VISTA BASADA EN CLASES PARA EDITAR UNA BITÁCORA DE UN ESTUDIANTE
@add_group_name_to_context
class BitacoraEstudianteUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = BitacoraEstudiante
    template_name = 'informes/bitacora_estudiante_edit.html'
    form_class = BitacoraEstudianteForm
    success_url = reverse_lazy('bitacora_estudiante_list')  # Ajusta la URL de éxito según sea necesario

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        context['asignaturas'] = Asignatura.objects.all()
        context['profesionales'] = Profile.objects.all()
        context['estudiantes'] = Estudiante.objects.all()
        context['usuario_logueado'] = self.request.user  # Agrega el usuario logueado al contexto
        context['fecha_actual'] = timezone.now().date()  # Agrega la fecha actual al contexto
        context['estudiante'] = self.object.estudiante  # Recupera el estudiante relacionado con la bitácora
        context['bitacora'] = self.object  # Agrega la bitácora actual al contexto

        # Obtener todas las bitácoras del mismo día
        bitacoras_del_dia = BitacoraEstudiante.objects.filter(estudiante=self.object.estudiante, fecha=self.object.fecha).order_by('id')
        bitacora_index = list(bitacoras_del_dia).index(self.object)

        # Obtener la bitácora anterior y siguiente
        context['previous_bitacora'] = bitacoras_del_dia[bitacora_index - 1] if bitacora_index > 0 else None
        context['next_bitacora'] = bitacoras_del_dia[bitacora_index + 1] if bitacora_index < len(bitacoras_del_dia) - 1 else None

        # Agregar el índice del registro actual al contexto
        context['registro_numero'] = bitacora_index + 1

        return context

    def form_valid(self, form):
        messages.success(self.request, 'Bitácora actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('bitacora_estudiante_list', kwargs={'estudiante_id': self.object.estudiante.id})


# -------------------------------------------------------------------------------------------------------------------
#VISTA REDIRECCIONAR LA BITACORA
@add_group_name_to_context
class BitacoraRedirectView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get(self, request, *args, **kwargs):
        fecha = request.GET.get('fecha')
        estudiante_id = kwargs.get('estudiante_id')
        bitacora = BitacoraEstudiante.objects.filter(estudiante_id=estudiante_id, fecha=fecha).first()
        if bitacora:
            return redirect(reverse('bitacora_estudiante', kwargs={'pk': bitacora.pk}))
        else:
            messages.error(request, 'No se encontraron bitácoras para la fecha seleccionada.')
            return redirect('calendario_bitacoras')



# -------------------------------------------------------------------------------------------------------------------
#VISTA BASADA EN CLASES PARA EL TEMPLATE DE VISTA DE LOS INFORMES DEL ESTUDIANTES

@add_group_name_to_context
class InformesEstudianteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Estudiante
    template_name = 'informes/informes_estudiante.html'
    context_object_name = 'estudiante'
    

    def test_func(self):
        return self.request.user.groups.exists()

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudiante = self.get_object()
        context['bitacoras'] = BitacoraEstudiante.objects.all()
        context['profesionales'] = Profile.objects.all()
        return context
    

# -------------------------------------------------------------------------------------------------------------------
#VISTA PARA DESCARGAR UN PDF DE UNA BITÁCORA DE UN ESTUDIANTE