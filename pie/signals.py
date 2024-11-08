from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RegistroPie, ApoderadoTitular

@receiver(post_save, sender=ApoderadoTitular)
def update_registro_pie(sender, instance, **kwargs):
    print(f'Señal activada para: {instance}')  # Mensaje de depuración
    # Busca el RegistroPie relacionado al apoderado
    try:
        registro_pie = RegistroPie.objects.get(apoderado_titular=instance)
        # Actualiza los campos necesarios en RegistroPie
        registro_pie.apoderado_titular = instance
        registro_pie.save()  # Guarda los cambios
        print(f'Registro actualizado: {registro_pie}')  # Mensaje de depuración
    except RegistroPie.DoesNotExist:
          print('No se encontró RegistroPie asociado.')  # Mensaje de depuración
        # No hay RegistroPie relacionado, puedes manejar esto si es necesario
    pass
