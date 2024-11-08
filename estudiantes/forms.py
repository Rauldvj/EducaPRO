from django import forms #IMPORTAMOS LOS FORMULARIOS
from .models import * #IMPORTAMOS LOS MODELOS
from estudiantes.models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos
from app.models import BitacoraEstudiante


#_____________________________________________________________________________________________________________

#FORMULARIO PARA DE UN ESTUDIANTE

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['cursos', 'rut', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'region', 'comuna', 'etnia', 'comorbilidad']

        def clean_rut(self):
            rut = self.cleaned_data.get('rut')
            if Estudiante.objects.filter(rut=rut).exists():
                raise forms.ValidationError('Ya existe un estudiante con este RUT.')
            return rut

#FORM APODERADO TITULAR
class ApoderadoTitularForm(forms.ModelForm):
    class Meta:
        model = ApoderadoTitular
        fields = ['rut', 'etnia', 'fecha_nacimiento', 'nombres', 'apellido_paterno', 'apellido_materno', 'direccion', 'telefono', 'salud', 'renta', 'email', 'region', 'comuna']

#_____________________________________________________________________________________________________________
#FORM APODERADO SUPLENTE UNO
class ApoderadoSuplenteUnoForm(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplenteUno
        fields = ['rut', 'fecha_nacimiento', 'nombres', 'apellido_paterno', 'apellido_materno', 'direccion', 'telefono', 'region', 'comuna']

#_____________________________________________________________________________________________________________
#FORM APODERADO SUPLENTE DOS
class ApoderadoSuplenteDosForm(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplenteDos
        fields = ['rut', 'fecha_nacimiento', 'nombres', 'apellido_paterno', 'apellido_materno', 'direccion', 'telefono', 'region', 'comuna']


class AddApoderadoSuplenteUnoForm(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplenteUno
        fields = '__all__'

class AddApoderadoSuplenteDosForm(forms.ModelForm):
    class Meta:
        model = ApoderadoSuplenteDos
        fields = '__all__'


#_____________________________________________________________________________________________________________

# FORMULARIO PARA REGISTRO DE BITÁCORA DE UN ESTUDIANTE
class BitacoraEstudianteForm(forms.ModelForm):
    class Meta:
        model = BitacoraEstudiante
        fields = ['estudiante', 'asignatura', 'actividad', 'observaciones']
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'form-control'}),
        }

