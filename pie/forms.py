from django import forms
from .models import RegistroPie

class ListPieForm(forms.ModelForm):
    class Meta:
        model = RegistroPie
        fields = ['estudiante', 'apoderado', 'ApoderadoSuplenteUno', 'ApoderadoSuplenteDos', 'enable']

class AddRegistroPieForm(forms.ModelForm):
    class Meta:
        model = RegistroPie
        fields = ['nivel_academico', 'curso', 'letra_curso', 'estudiante', 'apoderado', 'ApoderadoSuplenteUno', 'ApoderadoSuplenteDos', 'enable']


