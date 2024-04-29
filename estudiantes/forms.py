from django import forms #IMPORTAMOS LOS FORMULARIOS
from .models import * #IMPORTAMOS LOS MODELOS
from estudiantes.models import *

#_____________________________________________________________________________________________________________

#FORMULARIO PARA CREAR EL REGISTRO DE UN ESTUDIANTE

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'


class ApoderadoTitularForm(forms.ModelForm):
    class Meta:
        model = ApoderadoTitular
        fields = '__all__'


class ApoderadoSuplenteUno(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplente1
        fields = '__all__'

class ApoderadoSuplenteDos(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplente2
        fields = '__all__'
