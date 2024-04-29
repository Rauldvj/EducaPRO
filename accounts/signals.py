from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import  post_save, post_delete
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_funcionarios_group(sender, instance, created, **kwargs):
    if created:
        try:
            group1 = Group.objects.get(name='Funcionarios')
        except Group.DoesNotExist:
            group1 = Group.objects.create(name='Funcionarios')
            group2 = Group.objects.create(name='Administradores')
            group3 = Group.objects.create(name='Coordinadores')
            group4 = Group.objects.create(name='Psicopedagógos')
            group5 = Group.objects.create(name='Psicólogos')
            group6 = Group.objects.create(name='Terapeutas Ocupacionales')
            group7 = Group.objects.create(name='Fonoaudiologos')
            group8 = Group.objects.create(name='Técnicos Diferenciales')
            group9 = Group.objects.create(name='Técnicos Parvularios')
        instance.user.groups.add(group1)