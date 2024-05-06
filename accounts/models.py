from django.db import models
from localidad.models import Region, Comuna
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#____________________________________________________________________________________________________________

# PERFIL DE USUARIO

class Profile(models.Model): #Modelo para el perfil
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    image = models.ImageField(default='default.png', upload_to='users/', verbose_name='Imagen de perfil')
    rut = models.CharField(max_length=12, null=True, blank=True, verbose_name='Rut')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Region')
    comuna = models.ForeignKey(Comuna, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Comuna')
    telefono = models.CharField(max_length=9, null=True, blank=True, verbose_name='Teléfono')
    creado_por_coordinador = models.BooleanField(default=True, blank=True, null=True, verbose_name='Creado por el Coordinador')
    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


def create_user_profile(sender, instance, created, **kwargs): #Función para crear el perfil de usuario
    if created:
        default_region = Region.objects.first()  # Obtener la primera región por defecto
        default_comuna = Comuna.objects.first() # Obtener la primera comuna por defecto
        Profile.objects.create(user=instance, region=default_region, comuna=default_comuna)

def save_user_profile(sender, instance, **kwargs): #Función para guardar el perfil de usuario
    instance.profile.save()

post_save.connect(create_user_profile, sender=User) #Conectar la función
post_save.connect(save_user_profile, sender=User) #Conectar la función