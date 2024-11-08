from django.db.models.signals import post_save
from django.dispatch import receiver
from estudiantes.models import Estudiante, ApoderadoTitular, ApoderadoSuplenteUno, ApoderadoSuplenteDos
from pie.models import RegistroPie
from app.models import Anamnesis

@receiver(post_save, sender=Estudiante)
def crear_registro_estudiante_pie(sender, instance, created, **kwargs):
    if created:
        # Verifica si ya existen instancias antes de crearlas
        if not ApoderadoTitular.objects.filter(estudiante=instance).exists():
            ApoderadoTitular.objects.create(estudiante=instance)

        if not ApoderadoSuplenteUno.objects.filter(estudiante=instance).exists():
            ApoderadoSuplenteUno.objects.create(estudiante=instance)

        if not ApoderadoSuplenteDos.objects.filter(estudiante=instance).exists():
            ApoderadoSuplenteDos.objects.create(estudiante=instance)

        if not RegistroPie.objects.filter(estudiante=instance).exists():
            RegistroPie.objects.create(estudiante=instance, curso=instance.cursos)
    else:
        # Actualiza el campo curso en RegistroPie si el estudiante ya existe
        registro_pie = RegistroPie.objects.filter(estudiante=instance).first()
        if registro_pie:
            registro_pie.curso = instance.cursos
            registro_pie.save()
            

    # -------------------------------------------------------------------------------------------------
    #Actualizar registros en simultaneo con el registro PIE del Apoderado Titular

@receiver(post_save, sender=ApoderadoTitular)
def actualizar_apoderado_titular_registro_pie(sender, instance, **kwargs):
    try:
        registro_pie = RegistroPie.objects.get(estudiante=instance.estudiante)
        registro_pie.apoderado_titular = instance  # Actualiza el apoderado titular
        registro_pie.save()  # Guarda los cambios en el registro PIE
    except RegistroPie.DoesNotExist:
        pass  # Si no existe un registro PIE, no hace nada

    # -------------------------------------------------------------------------------------------------
    #Actualizar registros en simultaneo con el registro PIE del Apoderado Suplente Uno

@receiver(post_save, sender=ApoderadoSuplenteUno)
def actualizar_apoderado_suplente_uno_registro_pie(sender, instance, **kwargs):
    try:
        registro_pie = RegistroPie.objects.get(estudiante=instance.estudiante)
        registro_pie.apoderado_suplente_uno = instance  # Actualiza el Apoderado Suplente Uno
        registro_pie.save()  # Guarda los cambios en el registro PIE
    except RegistroPie.DoesNotExist:
        pass  # Si no existe un registro PIE, no hace nada

    # -------------------------------------------------------------------------------------------------
    #Actualizar registros en simultaneo con el registro PIE del Apoderado Suplente Dos

@receiver(post_save, sender=ApoderadoSuplenteDos)
def actualizar_apoderado_suplente_dos_registro_pie(sender, instance, **kwargs):
    try:
        registro_pie = RegistroPie.objects.get(estudiante=instance.estudiante)
        registro_pie.apoderado_suplente_dos = instance  # Actualiza el Apoderado Suplente Dos
        registro_pie.save()  # Guarda los cambios en el registro PIE
    except RegistroPie.DoesNotExist:
        pass  # Si no existe un registro PIE, no hace nada