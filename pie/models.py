from django.db import models
from estudiantes.models import *
from .opciones import *



#MODELO QUE CREA NIVEL ACADÉMICO DEL CURSO  


#____________________________________________________________________________________________________________

#MODELO PARA CREAR UN CURSO

class Curso(models.Model):
    nivel_academico = models.CharField(max_length=100, choices=opcion_nivel_educativo, verbose_name='Nivel Académico')
    curso = models.CharField(max_length=100, verbose_name='Curso')
    letra_curso = models.CharField(max_length=1, choices=opcion_letra_curso, verbose_name='Letra')
    
    class Meta:
        abstract = True
#____________________________________________________________________________________________________________


#MODELO PARA UNA Registro en el PIE

class RegistroPie(Curso):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    apoderado = models.ForeignKey(ApoderadoTitular, on_delete=models.CASCADE, verbose_name='Apoderado')
    ApoderadoSuplente1 = models.ForeignKey(ApoderadoSuplente1, on_delete=models.CASCADE, verbose_name='Apoderado Suplente 1')
    ApoderadoSuplente2 = models.ForeignKey(ApoderadoSuplente2, on_delete=models.CASCADE, verbose_name='Apoderado Suplente 2')
    enable = models.BooleanField(default=True, null=True, verbose_name='Alumno Regular')
    def __str__(self):
        return f'{self.estudiante} {self.estudiante}'
    
    class Meta: 
        verbose_name = 'Pie'
        verbose_name_plural = 'Pies'
#____________________________________________________________________________________________________________

# Definición del modelo Asistencia
# class Asistencia(models.Model):
#     curso = models.ForeignKey(
#         Curso,
#         on_delete=models.CASCADE,
#         verbose_name='Curso',
#         # Aquí limitamos las opciones del curso al que deseamos asignar
#         # Asegúrate de reemplazar '1' con el ID correcto del curso específico
#         limit_choices_to={'id': 1}  
#     )
#     estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
#     fecha = models.DateField(null=True, blank=True, verbose_name='Fecha')
#     presente = models.BooleanField(default=False, null=True, blank=True, verbose_name='Presente')

#     def __str__(self):
#         return f'Asistencia {self.id}'
    
#     class Meta: 
#         verbose_name = 'Asistencia'
#         verbose_name_plural = 'Asistencias'

#____________________________________________________________________________________________________________