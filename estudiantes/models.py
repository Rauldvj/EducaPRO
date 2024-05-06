from django.db import models
from localidad.models import *
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .opciones import *
from django.core.validators import EmailValidator

# Create your models here.

#CREAREMOS UNA CLASE ABSTRACTA QUE NO CREARA UNA TABLA, 
# SINO QUE SERA UNA MODELO BASE PARA CUALQUIER OTRO MODELO QUE LO REQUIERA

class Persona(models.Model):
    rut= models.CharField(max_length=12, unique=True, verbose_name="Rut")
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    direccion = models.CharField(max_length=100, verbose_name='Dirección')
    telefono = models.CharField(max_length=9, verbose_name='Teléfono')

    class Meta:
        abstract = True  # Hace que este modelo sea abstracto y no se cree una tabla en la base de datos

#________________________________________________________________________________________________________

class Estudiante(Persona): #Heredamos de la clase Persona(Modelo Abstracto)
    correo = models.EmailField(validators=[EmailValidator()], verbose_name='Correo Electrónico')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region' )
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna')
    etnia = models.CharField(max_length=100, default='No Posee', choices=opciones_ascendencia, verbose_name='Ascendencia')
    comorbilidad = models.TextField(verbose_name='Comorbilidad')

    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

# Definición de la señal pre_save para estandarizar el formato de las cadenas
@receiver(pre_save, sender=Estudiante)
def estudiante_pre_save(sender, instance, *args, **kwargs):
    instance.nombres = instance.nombres.title()
    instance.apellido_paterno = instance.apellido_paterno.title()
    instance.apellido_materno = instance.apellido_materno.title()
    instance.direccion = instance.direccion.title()  # Asegura la primera letra en mayúscula en cada palabra de la dirección
    # Asegura que la comorbilidad esté en minúsculas
    instance.comorbilidad = instance.comorbilidad.lower()


#-------------------------------------------------------------------------------------------------
# SECCIÓN PARA CREAR MODELOS DE LOS APODERADOS ---------------------------------------------------

class ApoderadoTitular(Persona):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    correo = models.EmailField(validators=[EmailValidator()], verbose_name='Correo Electrónico')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region' )
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna')
    etnia = models.CharField(max_length=100, default='No Posee', choices=opciones_ascendencia, verbose_name='Ascendencia')
    salud = models.CharField(max_length=100, default='Seleccione', choices=opciones_salud, verbose_name='Salud')
    renta = models.PositiveIntegerField(verbose_name='Renta')
    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'

    class Meta:
        verbose_name = 'Apoderado Titular'
        verbose_name_plural = 'Apoderados Titulares'

#-------------------------------------------------------------------------------------------------

#____________________________________________________________________________________________________________
#MODELO PARA REGISTRAR UN APODERADO SUPLENTE 1

class ApoderadoSuplenteUno(Persona):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region' )
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna')
    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'
    
    class Meta:
        verbose_name = 'Apoderado Suplente 1'
        verbose_name_plural = 'Apoderados Suplentes 1'

#____________________________________________________________________________________________________________
#MODELO PARA REGISTRAR UN APODERADO SUPLENTE 2

class ApoderadoSuplenteDos(Persona):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='Region' )
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='Comuna')
    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'
    

    class Meta:
        verbose_name = 'Apoderado Suplente 2'
        verbose_name_plural = 'Apoderados Suplentes 2'

#____________________________________________________________________________________________________________
