from django import forms
from .models import RegistroPie

class ListPieForm(forms.ModelForm):
    class Meta:
        model = RegistroPie
        fields = ['estudiante', 'apoderado_titular', 'apoderado_suplente_uno', 'apoderado_suplente_dos', 'enable']

class AddRegistroPieForm(forms.ModelForm):
    class Meta:
        model = RegistroPie
        fields = ['estudiante', 'apoderado_titular', 'apoderado_suplente_uno', 'apoderado_suplente_dos', 'enable']


