from django import forms
from .models import ListPieView

class ListPieForm(forms.ModelForm):
    class Meta:
        model = ListPieView
        fields = ['estudiante', 'apoderado', 'ApoderadoSuplente1', 'ApoderadoSuplente2', 'enable']
