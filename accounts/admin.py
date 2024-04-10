from django.contrib import admin
from .models import *

#---------------------------------------------------------------------
# PROFILE DETALLADO
class ProfileAdmin(admin.ModelAdmin):
    list_display =('user', 'rut', 'direccion', 'region', 'comuna','telefono', 'creado_por_coordinador')
    search_fields =('rut', 'user__username')
    list_filter = ('rut', )


admin.site.register(Profile, ProfileAdmin)