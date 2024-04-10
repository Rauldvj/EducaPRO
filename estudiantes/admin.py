from django.contrib import admin
from .models import Estudiante, ApoderadoTitular, ApoderadoSuplente1, ApoderadoSuplente2

#____________________________________________________________________________________________________________________________________________________________________________________________
#Registrar en el Administrador
#Registrar Estudiante

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'comorbilidad')
admin.site.register(Estudiante, EstudianteAdmin)

#____________________________________________________________________________________________________________________________________________________________________________________________________________
#Registrar Apoderado Titular

class ApoderadoTitularAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'salud', 'renta')
admin.site.register(ApoderadoTitular, ApoderadoTitularAdmin)
#____________________________________________________________________________________________________________________________________________________________________________________________

#Registrar Apoderado Suplente 1

class ApoderadoSuplente1Admin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'region', 'comuna')
admin.site.register(ApoderadoSuplente1, ApoderadoSuplente1Admin)

#___________________________________________________________________________________________________________________________________________________________________________________________

#Registrar Apoderado Suplente 2

class ApoderadoSuplente2Admin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'region', 'comuna')
    fieldsets = (
        (None, {
            'fields': ('rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono'),
        }),
        ('Localidad', {
            'fields': ('region', 'comuna'),
        })
    )

admin.site.register(ApoderadoSuplente2, ApoderadoSuplente2Admin)

