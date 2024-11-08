from django.contrib import admin
from .models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos

#____________________________________________________________________________________________________________________________________________________________________________________________
#Registrar en el Administrador
#Registrar Estudiante

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('cursos', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'comorbilidad')
admin.site.register(Estudiante, EstudianteAdmin)

#____________________________________________________________________________________________________________________________________________________________________________________________________________
#Registrar Apoderado Titular

class ApoderadoTitularAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'region', 'comuna', 'etnia', 'salud', 'renta')
admin.site.register(ApoderadoTitular, ApoderadoTitularAdmin)
#____________________________________________________________________________________________________________________________________________________________________________________________

#Registrar Apoderado Suplente 1

class ApoderadoSuplenteUnoAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'region', 'comuna')
    fieldsets = (
        (None, {
            'fields': ('estudiante', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono'),
        }),
        ('Localidad', {
            'fields': ('region', 'comuna'),
        })
    )
admin.site.register(ApoderadoSuplenteUno, ApoderadoSuplenteUnoAdmin)

#___________________________________________________________________________________________________________________________________________________________________________________________

#Registrar Apoderado Suplente 2

class ApoderadoSuplenteDosAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'region', 'comuna')
    fieldsets = (
        (None, {
            'fields': ('estudiante', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono'),
        }),
        ('Localidad', {
            'fields': ('region', 'comuna'),
        })
    )

admin.site.register(ApoderadoSuplenteDos, ApoderadoSuplenteDosAdmin)

