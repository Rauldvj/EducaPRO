# Generated by Django 4.2.6 on 2024-04-15 05:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('localidad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True, verbose_name='Rut')),
                ('nombres', models.CharField(max_length=50, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=50, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=50, verbose_name='Apellido Materno')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=9, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Correo Electrónico')),
                ('etnia', models.CharField(choices=[('No posee', 'No posee'), ('Aymara', 'Aymara'), ('Lickanantay', ' Lickanantay'), ('Colla', 'Colla'), ('Quechua', 'Quechua'), ('Diaguita', 'Diaguita'), ('Chango', 'Chango'), ('Rapa Nui', 'Rapa Nui'), ('Mapuche', 'Mapuche'), ('Kawesqar', 'Kawesqar'), ('Yagan', 'Yagan')], default='No Posee', max_length=100, verbose_name='Ascendencia')),
                ('comorbilidad', models.TextField(verbose_name='Comorbilidad')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.comuna', verbose_name='Comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Estudiante',
                'verbose_name_plural': 'Estudiantes',
            },
        ),
        migrations.CreateModel(
            name='ApoderadoTitular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True, verbose_name='Rut')),
                ('nombres', models.CharField(max_length=50, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=50, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=50, verbose_name='Apellido Materno')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=9, verbose_name='Teléfono')),
                ('correo', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Correo Electrónico')),
                ('etnia', models.CharField(choices=[('No posee', 'No posee'), ('Aymara', 'Aymara'), ('Lickanantay', ' Lickanantay'), ('Colla', 'Colla'), ('Quechua', 'Quechua'), ('Diaguita', 'Diaguita'), ('Chango', 'Chango'), ('Rapa Nui', 'Rapa Nui'), ('Mapuche', 'Mapuche'), ('Kawesqar', 'Kawesqar'), ('Yagan', 'Yagan')], default='No Posee', max_length=100, verbose_name='Ascendencia')),
                ('salud', models.CharField(choices=[('Seleccione', 'Seleccione'), ('Publica', 'Publica'), ('Privada', 'Privada')], default='Seleccione', max_length=100, verbose_name='Salud')),
                ('renta', models.PositiveIntegerField(verbose_name='Renta')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.comuna', verbose_name='Comuna')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiantes.estudiante', verbose_name='Estudiante')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Apoderado Titular',
                'verbose_name_plural': 'Apoderados Titulares',
            },
        ),
        migrations.CreateModel(
            name='ApoderadoSuplente2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True, verbose_name='Rut')),
                ('nombres', models.CharField(max_length=50, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=50, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=50, verbose_name='Apellido Materno')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=9, verbose_name='Teléfono')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.comuna', verbose_name='Comuna')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiantes.estudiante', verbose_name='Estudiante')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Apoderado Suplente 2',
                'verbose_name_plural': 'Apoderados Suplentes 2',
            },
        ),
        migrations.CreateModel(
            name='ApoderadoSuplente1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=10, unique=True, verbose_name='Rut')),
                ('nombres', models.CharField(max_length=50, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=50, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(max_length=50, verbose_name='Apellido Materno')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('direccion', models.CharField(max_length=100, verbose_name='Dirección')),
                ('telefono', models.CharField(max_length=9, verbose_name='Teléfono')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.comuna', verbose_name='Comuna')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estudiantes.estudiante', verbose_name='Estudiante')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='localidad.region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Apoderado Suplente 1',
                'verbose_name_plural': 'Apoderados Suplentes 1',
            },
        ),
    ]
