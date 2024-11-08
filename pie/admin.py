from django.contrib import admin
from .models import RegistroPie


class RegistroPieAdmin(admin.ModelAdmin):
    list_display = ('curso', 'estudiante', 'apoderado_titular', 'apoderado_suplente_uno', 'apoderado_suplente_dos', 'enable')


admin.site.register(RegistroPie, RegistroPieAdmin)
#____________________________________________________________________________________________________________



#____________________________________________________________________________________________________________
    



#____________________________________________________________________________________________________________


#_____________________________________________________________________________________________________________