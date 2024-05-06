from django import forms #IMPORTAMOS LOS FORMULARIOS
from .models import * #IMPORTAMOS LOS MODELOS
from estudiantes.models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos

#_____________________________________________________________________________________________________________

#FORMULARIO PARA CREAR EL REGISTRO DE UN ESTUDIANTE

class AddEstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'


class AddApoderadoTitularForm(forms.ModelForm):
    class Meta:
        model = ApoderadoTitular
        fields = '__all__'


class AddApoderadoSuplenteUnoForm(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplenteUno
        fields = '__all__'

class AddApoderadoSuplenteDosForm(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplenteDos
        fields = '__all__'
