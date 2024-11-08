from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from estudiantes.models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos



#MODELO QUE CREA NIVEL ACADÉMICO DEL CURSO  


#____________________________________________________________________________________________________________

#MODELO PARA CREAR UN CURSO

# Modelo de RegistroPie
class RegistroPie(models.Model):
    curso = models.CharField(max_length=150, choices=Estudiante._meta.get_field('cursos').choices, verbose_name='Curso')
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    apoderado_titular = models.ForeignKey(ApoderadoTitular, on_delete=models.CASCADE, verbose_name='Apoderado', null=True, blank=True)
    apoderado_suplente_uno = models.OneToOneField(ApoderadoSuplenteUno, on_delete=models.CASCADE, verbose_name='Apoderado Suplente 1', null=True, blank=True)
    apoderado_suplente_dos = models.OneToOneField(ApoderadoSuplenteDos, on_delete=models.CASCADE, verbose_name='Apoderado Suplente 2', null=True, blank=True)
    enable = models.BooleanField(default=True, null=True, verbose_name='Alumno Regular')

    def __str__(self):
        return f'{self.estudiante}'
    
    class Meta:
        verbose_name = 'Pie'
        verbose_name_plural = 'Pies'
#____________________________________________________________________________________________________________
