from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from estudiantes.models import Estudiante, ApoderadoTitular, ApoderadoSuplente1, ApoderadoSuplente2
from .opciones import opcion_nivel_educativo, opcion_curso, opcion_letra_curso



#MODELO QUE CREA NIVEL ACADÉMICO DEL CURSO  


#____________________________________________________________________________________________________________

#MODELO PARA CREAR UN CURSO

class Curso(models.Model):
    nivel_academico = models.CharField(max_length=100, choices=opcion_nivel_educativo, verbose_name='Nivel Académico')
    curso = models.CharField(max_length=100, choices=opcion_curso, verbose_name='Curso')
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
        return f'{self.estudiante}'
    
    class Meta: 
        verbose_name = 'Pie'
        verbose_name_plural = 'Pies'
#____________________________________________________________________________________________________________
