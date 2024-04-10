from django.contrib import admin
from .models import *



#____________________________________________________________________________________________________________



#____________________________________________________________________________________________________________
class RegistroPieAdmin(admin.ModelAdmin):
    list_display = ['curso', 'estudiante', 'apoderado', 'ApoderadoSuplente1', 'ApoderadoSuplente2', 'enable']
    search_fields = ['estudiante']
    list_filter = ['curso', 'estudiante']

    
admin.site.register(RegistroPie, RegistroPieAdmin)


#____________________________________________________________________________________________________________

# Definición de la clase AsistenciaAdmin para el panel de administración
# class AsistenciaAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         # Filtramos las opciones del campo de selección del curso en el panel de administración
#         if db_field.name == "curso":
#             # Reemplaza "1" con el ID del curso específico al que deseas restringir las opciones
#             kwargs["queryset"] = Curso.objects.filter(id=1)  
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#     list_display = ['curso', 'estudiante', 'fecha', 'presente']
#     search_fields = ['estudiante']
#     list_filter = ['curso', 'estudiante']

# # Registro del modelo Asistencia en el panel de administración
# admin.site.register(Asistencia, AsistenciaAdmin)



#_____________________________________________________________________________________________________________