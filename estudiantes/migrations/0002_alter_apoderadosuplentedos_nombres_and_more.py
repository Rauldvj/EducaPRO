# Generated by Django 4.2.6 on 2024-05-06 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estudiantes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apoderadosuplentedos',
            name='nombres',
            field=models.CharField(max_length=100, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='apoderadosuplenteuno',
            name='nombres',
            field=models.CharField(max_length=100, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='apoderadotitular',
            name='nombres',
            field=models.CharField(max_length=100, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='nombres',
            field=models.CharField(max_length=100, verbose_name='Nombres'),
        ),
    ]