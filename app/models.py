from django.db import models
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MinValueValidator, MaxValueValidator

from django.dispatch import receiver
from django.contrib.auth.models import Group #Importamos los Groups de Autenticación
from accounts.models import *
from estudiantes.models import *
from .opciones import *

#AQUÍ CREAREMOS LOS MODELOS PARA NUESTRA APLICACIÓN


#Modelo para Bitacora

class Bitacora(models.Model):
    #BITACORA ESTUDIANTE
    fecha = models.DateField(verbose_name='Fecha')
    hora_entrada = models.TimeField(auto_now=False)
    hora_salida = models.TimeField(auto_now=False)
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, verbose_name='Estudiante')
    
    #PRIMER BLOQUE
    bloque1 = models.CharField(max_length=20, choices=opcionesBloque,default='Primer bloque', verbose_name='Bloque')
    objetivoClase1 = models.CharField(max_length=350, verbose_name='Objetivo de la Clase')  
    objetivoPaci1 = models.CharField(max_length=350, verbose_name='Objetivo del Paci')
    desarrolloActividad1 = models.TextField(verbose_name='Desarrollo de la actividad')
    material1= models.TextField(verbose_name='Material utilizado')
    personaMaterial1 = models.CharField(max_length=100, verbose_name='Persona que entrega el material')
    reaccion1 = models.CharField(max_length=350, verbose_name='Reacción del alumno frente a la actividad')
    estadoAprendizaje1 = models.CharField(max_length=20, default='Seleccione', choices=opciones_aprendizaje, verbose_name='Estado aprendizaje')
    apoyoDocente1 = models.CharField(max_length=20, default='Seleccione', choices=opciones_si_no, verbose_name='Apoyo del Docente durante la actividad')
    obervacionesGenerales1 = models.TextField(verbose_name='Observaciones generales', blank=True)
    
    #SEGUNDO BLOQUE
    bloque2b = models.CharField(max_length=20, choices=opcionesBloque,default='Segundo bloque', verbose_name='Bloque')
    objetivoClase2b = models.CharField(max_length=350, verbose_name='Objetivo de la Clase')  
    objetivoPaci2b = models.CharField(max_length=350, verbose_name='Objetivo del Paci')
    desarrolloActividad2b = models.TextField(verbose_name='Desarrollo de la actividad')
    material2b = models.TextField(verbose_name='Material utilizado')
    personaMaterial2b = models.CharField(max_length=100, verbose_name='Persona que entrega el material')
    reaccion2b = models.CharField(max_length=350, verbose_name='Reacción del alumno frente a la actividad')
    estadoAprendizaje2b = models.CharField(max_length=20, default='Seleccione', choices=opciones_aprendizaje, verbose_name='Estado aprendizaje')
    apoyoDocente2b = models.CharField(max_length=20, default='Seleccione', choices=opciones_si_no, verbose_name='Apoyo del Docente durante la actividad')
    obervacionesGenerales2b = models.TextField(verbose_name='Observaciones generales')
    
    #TERCER BLOQUE
    bloque3c = models.CharField(max_length=20, choices=opcionesBloque,default='Tercer bloque', verbose_name='Bloque')
    objetivoClase3c = models.CharField(max_length=350, verbose_name='Objetivo de la Clase')  
    objetivoPaci3c = models.CharField(max_length=350, verbose_name='Objetivo del Paci')
    desarrolloActividad3c = models.TextField(verbose_name='Desarrollo de la actividad')
    material3c = models.TextField(verbose_name='Material utilizado')
    personaMaterial3c = models.CharField(max_length=100, verbose_name='Persona que entrega el material')
    reaccion3c = models.CharField(max_length=350, verbose_name='Reaccion del alumno frente a la actividad')
    estadoAprendizaje3c = models.CharField(max_length=20, default='Seleccione', choices=opciones_aprendizaje, verbose_name='Estado aprendizaje')
    apoyoDocente3c = models.CharField(max_length=20, default='Seleccione', choices=opciones_si_no, verbose_name='Apoyo del Docente durante la actividad')
    obervacionesGenerales3c = models.TextField(verbose_name='Observaciones generales')

    #CUARTO BLOQUE
    bloque4d = models.CharField(max_length=20, choices=opcionesBloque,default='Cuarto bloque', verbose_name='Bloque')
    objetivoClase4d = models.CharField(max_length=350, verbose_name='Objetivo de la Clase')  
    objetivoPaci4d = models.CharField(max_length=350, verbose_name='Objetivo del Paci')
    desarrolloActividad4d = models.TextField(verbose_name='Desarrollo de la actividad')
    material4d = models.TextField(verbose_name='Material utilizado')
    personaMaterial4d= models.CharField(max_length=100, verbose_name='Persona que entrega el material')
    reaccion4d = models.CharField(max_length=350, verbose_name='Reaccion del alumno frente a la actividad')
    estadoAprendizaje4d = models.CharField(max_length=20, default='Seleccione', choices=opciones_aprendizaje, verbose_name='Estado aprendizaje')
    apoyoDocente4d = models.CharField(max_length=20, default='Seleccione', choices=opciones_si_no, verbose_name='Apoyo del Docente durante la actividad')
    obervacionesGenerales4d= models.TextField(verbose_name='Observaciones generales')

    def __str__(self):  
        return f'{self.fecha}, {self.hora_entrada}, {self.hora_salida} {self.estudiante}'
    
    class Meta: 
        verbose_name = 'Bitácora'
        verbose_name_plural = 'Bitácoras'

#___________________________________________________________________________________________________________________
#MODELOS ABSTRACTOS PARA REGISTRO DE ANAMNESIS

#Modelo para Registrar un Anamnesis
class LenguaMaterna(models.Model):
    lengua_materna = models.CharField(max_length=20, choices=opciones_lengua, default='Seleccione', verbose_name='Lengua Materna:')
    comprende_materna = models.BooleanField(max_length=10, default=False, verbose_name='Comprende:', blank=True)
    habla_materna = models.BooleanField(max_length=10, default=False, verbose_name='Habla:', blank=True)
    lee_materna = models.BooleanField(max_length=10, default=False, verbose_name='Lee:', blank=True)
    escribe_materna = models.BooleanField(max_length=10, default=False, verbose_name='Escribe:', blank=True)
    class Meta:
        abstract = True

class LenguaUso(models.Model):
    lengua_uso = models.CharField(max_length=20, choices=opciones_lengua, default='Seleccione', verbose_name='Lengua Uso:', blank=True)
    comprende_uso = models.BooleanField(max_length=10, default=False, verbose_name='Comprende:', blank=True)
    habla_uso = models.BooleanField(max_length=10, default=False, verbose_name='Habla:', blank=True)
    lee_uso = models.BooleanField(max_length=10, default=False, verbose_name='Lee:',blank=True)
    escribe_uso = models.BooleanField(max_length=10, default=False, verbose_name='Escribe:', blank=True)
    class Meta:
        abstract = True


    
#___________________________________________________________________________________________________________________

class Anamnesis(LenguaMaterna, LenguaUso):
    #1. IDENTIFICACIÓN DEL ESTUDIANTE 
    nombre = models.CharField(max_length=150, verbose_name='Nombre:')
    sexo = models.CharField(max_length=10, choices=opcionesSexo, default='masculino', verbose_name='Sexo:')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento:')
    #EDAD ACTUAL
    años = models.PositiveIntegerField(verbose_name='Años:')


    meses = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=12)
        ],
        verbose_name='Meses'
    )



    pais = models.CharField(max_length=50, verbose_name='País de natal:', blank=True)
    domicilio = models.CharField(max_length=100, verbose_name='Domicilio actual:', blank=True)
    telefono = models.CharField(max_length=8, verbose_name='Teléfono:', blank=True)
    escolaridad_actual = models.CharField(max_length=100, verbose_name='Escolaridad Actual:', blank=True)
    establecimiento = models.CharField(max_length=100, verbose_name='Establecimiento:', blank=True)

    #2. IDENTIFICACIÓN DEL O LOS INFORMANTES
    #ENTREVISTA 1
    # ENTREVISTA 1
    fecha_entrevista_1 = models.DateField(verbose_name='Fecha de la Entrevista 1:')
    nombres_entrevista_1 = models.CharField(max_length=150, verbose_name='Nombre:')
    relacion_estudiante_1 = models.CharField(max_length=100, choices=opcion_relacion, default='Seleccione', verbose_name='Relación del Estudiante:')
    en_presencia_de_1 = models.CharField(max_length=100, choices=opcion_presencia, default='Seleccione', verbose_name='En presencia de:')

    # ENTREVISTA 2
    fecha_entrevista_2 = models.DateField(null=True, blank=True, verbose_name='Fecha de la Entrevista 2:')
    nombres_entrevista_2 = models.CharField(blank=True, max_length=150, verbose_name='Nombre:')
    relacion_estudiante_2 = models.CharField(blank=True, max_length=100, choices=opcion_relacion, default='Seleccione', verbose_name='Relación del Estudiante:')
    en_presencia_de_2 = models.CharField(blank=True, max_length=100, choices=opcion_presencia, default='', verbose_name='En presencia de:')

    # ENTREVISTA 3
    fecha_entrevista_3 = models.DateField(null=True, blank=True, verbose_name='Fecha de la Entrevista 3:')
    nombres_entrevista_3 = models.CharField(blank=True, max_length=150, verbose_name='Nombre:')
    relacion_estudiante_3 = models.CharField(blank=True, max_length=100, choices=opcion_relacion, default='Seleccione', verbose_name='Relación del Estudiante:')
    en_presencia_de_3 = models.CharField(blank=True, max_length=100, choices=opcion_presencia, default='', verbose_name='En presencia de:')

    # ENTREVISTA 4
    fecha_entrevista_4 = models.DateField(null=True, blank=True, verbose_name='Fecha de la Entrevista 4:')
    nombres_entrevista_4 = models.CharField(blank=True, max_length=150, verbose_name='Nombre:')
    relacion_estudiante_4 = models.CharField(blank=True, max_length=100, choices=opcion_relacion, default='Seleccione', verbose_name='Relación del Estudiante:')
    en_presencia_de_4 = models.CharField(blank=True, max_length=100, choices=opcion_presencia, default='', verbose_name='En presencia de:')

    # ENTREVISTADOR 1
    fecha_entrevistador = models.DateField(verbose_name='Fecha de la Entrevista:')
    nombreApellidos = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Entrevistador:', related_name='entrevistador')
    rol = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol/Cargo:')

    # ENTREVISTADOR 2
    fecha_entrevistador_2 = models.DateField(null=True, blank=True, verbose_name='Fecha de la Entrevista 2')
    nombreApellidos_2 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Entrevistador 2:', related_name='entrevistador_2', null=True, blank=True)
    rol_2 = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol/Cargo 2:', related_name='rol_2',null=True, blank=True)

    # ENTREVISTADOR 3
    fecha_entrevistador_3 = models.DateField(null=True, blank=True, verbose_name='Fecha de la Entrevista 3')
    nombreApellidos_3 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Entrevistador 3:', related_name='entrevistador_3', null=True, blank=True )
    rol_3 = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol/Cargo 3:', related_name='rol_3', null=True, blank=True)

    # ENTREVISTADOR 4
    fecha_entrevistador_4 = models.DateField(null=True, blank=True, verbose_name='Fecha de la Entrevista 4:')
    nombreApellidos_4 = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Entrevistador 4:', related_name='entrevistador_4', null=True, blank=True)
    rol_4 = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol/Cargo 4:', related_name='rol_4', null=True, blank=True)
    


    #4. DEFINICIÓN DEL PROBLEMA O SITUACIÓN QUE MOTIVA LA ENTREVISTA
    definicionProblema = models.TextField(verbose_name='Definición del Problema o situación que motiva la entrevista:', blank=True)

    #5. ANTECEDENTES RELATIVOS AL DESARROLLO Y A LA SALUD DEL/LA ESTUDIANTE
    pediatria = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Pediatría:')
    kinesiologia = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Kinesiología:')
    genetico = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Genético:')
    fonoaudiologia = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Fonoaudiología:')
    neurologia = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Neurología:')
    psicologia = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Psicología:')
    psiquiatria = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Psiquiatría:')
    psicopedagogia = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Psicopedagogía:')
    terapiaocupacional = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Terapia Ocupacional:')
    otro = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Otro:')

    #5.1. Primer año de vida
    tipo_parto = models.CharField(max_length=100, choices=opcion_parto, default='', verbose_name='Tipo de Parto:')
    cesarea = models.CharField(max_length=300, verbose_name='Cesárea (Señalar Motivo)', blank=True)
    asistencia_medica_parto = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Tuvo asistencia médica durante el parto?:')
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso:')
    talla = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Talla:')
    antecedentes_embarazo_parto = models.TextField(verbose_name='Antecedentes de Embarazo:', blank=True)

    #Señale si durante los doce primeros meses de vida el niño o niña presentó
    desnutricion = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Desnutrición:')
    obesidad = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Obesidad:')
    fiebre_alta = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Fiebre Alta:')
    convulsiones = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Convulsiones:')
    traumatismos = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Traumatismos:')
    intoxicacion = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Intoxicación:')
    enfermedad_respiratoria = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Enfermedad Respiratoria:')
    asma = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Asma:')
    encefalitis = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Encefalitis:')
    meningitis = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Meningitis:')
    otra = models.CharField(max_length=300, verbose_name='Otra', blank=True)
    hospitalizaciones = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Hospitalizaciones:')
    hospitalizacion = models.CharField(max_length=300, verbose_name='Especifique motivos de la Hospitalización y duración:', blank=True)
    
    control_periodico_salud = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Se realizaron controles periódicos de salud:')
    vacunas = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Vacunas:')
    observaciones = models.TextField(verbose_name='Observaciones:', blank=True)

    #5.2. Desarrollo Sensorio Motriz
    #Edad en que el niño(a):
    fija_la_cabeza = models.PositiveSmallIntegerField(default=1, verbose_name='Fija la cabeza:')
    se_sienta_solo = models.PositiveSmallIntegerField(default=1, verbose_name='Se sienta solo/a:')
    camina_sin_apoyo = models.PositiveSmallIntegerField(default=1, verbose_name='Camina sin apoyo:')
    primeras_palabras = models.PositiveSmallIntegerField(default=1, verbose_name='Primeras palabras:')
    primeras_frases = models.PositiveSmallIntegerField(default=1, verbose_name='Primeras frases:')
    se_viste_solo = models.PositiveSmallIntegerField(default=1, verbose_name='Se viste solo/a:')
    controla_esfinter_vesical = models.CharField(max_length=10, choices=opcion_d_n, default='', verbose_name='Control de Esfinter Vesical:')
    controla_esfinter_anal = models.CharField(max_length=10, choices=opcion_d_n, default='', verbose_name='Control de Esfinter Anal:')
    observaciones_2 = models.TextField(verbose_name='Observaciones', blank=True)
    actividad_motora_general = models.CharField(max_length=15, choices=opcion_actividad_motora, default='', verbose_name='En su actividad motora general se aprecia:')
    tono_muscular_general = models.CharField(max_length=15, choices=opcion_tono_muscular, default='No', verbose_name='Su tono muscular general se aprecia:')
    
    #En relación con su motricidad gruesa se aprecia:
    estabilidad_caminar = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Estabilidad al caminar:')
    caida_frecuente = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Caídas frecuentes:')
    dominancia_lateral = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Dominancia lateral:')

    #En relación con su motricidad fina el niño (a) logra:
    garra = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Garra:')
    ensarta = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Ensarta:')
    presion = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Presión:')
    dibuja = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Dibuja:')
    pinza = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Pinza:')
    escribe = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Escribe:')

    #En relación con algunos signos cognitivos el niño (a)
    reaccion_voces_caras = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Reacciona a voces o caras familiares:')
    demanda_obj_comp = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Demanda objetos y compañía:')
    sonr_balb_gri_llo = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Sonríe, balbucea, grita, llora, indica o señala:')
    manipula_explora = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Manipula y Explora objetos:')
    comprende_prohibiciones = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Comprende prohibiciones:')
    disc_ojo_mano = models.CharField(max_length=10, choices=opciones_si_no, default='', verbose_name='Posee evidente descoordinación ojo-mano:')
    observaciones_3 = models.TextField(verbose_name='Observaciones:', blank=True)
    
    #5.3. Visión - Audición:
    estimulos_visuales = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Se interesa por los estímulos visuales (colores,\
    formas, movimientos, etc.)')
    dolores_cabeza = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta dolores frecuentes de cabeza')
    ojos_irrt_llor = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='En ocasiones tiene los ojos irritados o llorosos')
    acerca_aleja = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Se acerca o aleja demasiado los objetos a la\
    vista (frunce el ceño)')
    sigue_con_vista = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Sigue con la vista el desplazamiento de los\
    objetos o personas')
    presenta_movimientos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta movimientos oculares “anormales”')
    man_cond_erron = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Manifiesta conductas “erróneas” (tropiezos,\
    choques)')
    diag_medico = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta diagnóstico médico de miopía, \
    estrabismo, astigmatismo, u otro.')
    estimulo_auditivo = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Se interesa por los estímulos auditivos (ruidos, voces, música, etc.')
    voces_sonidos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Reacciona o reconoce voces o sonidos familiares')
    gira_cabeza = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Gira la cabeza cuando se le llama o ante un ruido fuerte')
    acerca_oidos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Acerca los oídos a la TV, radio o fuente de sonido')
    tapa_golpea_ojo = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='En ocasiones se tapa o golpea los oídos')
    dolor_oidos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta frecuentes dolores de oídos')
    pronunciacion_oral = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='La pronunciación oral es adecuada')
    otitis_hipo_otra =  models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta diagnóstico médico de otitis crónica, hipoacusia u otra.')
    observaciones_4 = models.TextField(verbose_name='Observaciones:', blank=True)


    #5.4. Desarrollo del Lenguaje
    nino_comunica = models.CharField(max_length=15, choices=opcion_comunica, default='', verbose_name='El niño (a) se comunica preferentemente en forma:')
    especifique = models.CharField(max_length=300, verbose_name='Otro, especifique:', blank=True)
    
    #Características del lenguaje expresivo
    balbucea = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Balbucea (oral o señas)/emite sonidos')
    vocaliza = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Vocaliza/realiza gestos o señas aisladas')
    emite_palabras = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Emite palabras/produce señas')
    emite_produce = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Emite/produce frases ')
    relata_expeciencias = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Relata experiencias')
    emision_pronunciacion = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='La emisión/pronunciación/producción es clara')

    #Características del lenguaje comprensivo
    identifica_objetos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Identifica objetos')
    identifica_personas = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Identifica personas')
    comprende_conceptos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Comprende conceptos abstractos')
    responde_coherente = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Responde en forma coherente preguntas de la vida diaria')
    instrucciones_simples = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Sigue instrucciones simples')
    instrucciones_complejas = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Sigue instrucciones complejas')
    instrucciones_grupales = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Sigue instrucciones grupales')
    comprende_relatos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Comprende relatos, noticias, cuentos cortos')
    perdida_lenguaje = models.CharField(max_length=300, verbose_name='Manifestó pérdida del lenguaje oral (especifique edad y motivos):', blank=True)
    observaciones_5 = models.TextField(verbose_name='Observaciones:', blank=True)

    #5.5. Desarrollo Social
    espontaneamente = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Se relaciona espontáneamente con las personas de su entorno natural.')
    comportamiento_actitudes = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Explica razones de sus comportamientos y actitudes')
    actividades_grupales = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Participa en actividades grupales ')
    trabajo_individual = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Opta por trabajo individual')
    lenguaje_ecolalico = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta lenguaje ecolálico')
    dificultad_adaptarse = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Exhibe dificultad para adaptarse a situaciones nuevas')
    forma_colaborativa = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Se relaciona en forma colaborativa')
    normas_sociales = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Respeta normas sociales')
    normas_escolares = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Respeta normas escolares')
    sentido_humor = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Muestra sentido del humor')
    movimientos_estereotipados = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Movimientos estereotipados ') 
    pataletas_frecuentes = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Presenta pataletas frecuentes')

    #Ante los siguientes estímulos su reacción es:
    luces = models.CharField(max_length=15, choices=opcion_estimulos, default='', verbose_name='Luces')
    sonidos = models.CharField(max_length=15, choices=opcion_estimulos, default='', verbose_name='Sonidos')
    personas_extranas = models.CharField(max_length=15, choices=opcion_estimulos, default='', verbose_name='Personas extrañas')
    observaciones_6 = models.TextField(verbose_name='Observaciones', blank=True)
    
    #5.6. Estado Actual de Salud del/la Estudiante
    vacunas_al_dia = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Vacunas al día')
    epilepsia = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Epilepsia')
    problemas_cardiacos = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Problemas cardiacos')
    paraplejia = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Paraplejia')
    perdida_auditiva = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Perdida auditiva')
    perdida_visual = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Perdida visual')
    trastorno_motor = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Trastorno motor')
    prob_bronco_resp = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Problema bronco-respiratorio')
    enf_infect_cont = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Enfermedad infecto-contagiosa')
    trastorno_emocional = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Trastorno emocional')
    trastorno_conductual = models.CharField(max_length=15, choices=opciones_si_no, default='', verbose_name='Trastorno conductual')
    otro_1 = models.CharField(max_length=300, verbose_name='Otro (especifique):', blank=True)
    problemas_salud = models.TextField(verbose_name='El o los problemas de salud reciben control/tratamiento (especifique):', blank=True)
    
    #Alimentación
    alimentacion = models.CharField(max_length=30, choices=opcion_alimentacion, default='', verbose_name='Alimentación')
    otro_2 = models.CharField(max_length=400, verbose_name='Otro (especifique):')
    
    #Peso
    peso_apreciacion = models.CharField(max_length=30, choices=opcion_peso, default='', verbose_name='Peso (apreciación del informante): ')
    
    #Sueño
    sueno = models.CharField(max_length=30, choices=opcion_sueno, default='', verbose_name='Sueño:')
    
    horas_sueno = models.PositiveSmallIntegerField(
    default=1,
    validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=12)
        ],
    verbose_name='Horas de sueño'
)

    insomnio = models.BooleanField(max_length=10, default='', verbose_name='Insomnio', blank=True)
    pesadillas = models.BooleanField(max_length=10, default='', verbose_name='Pesadillas', blank=True)
    terrores_nocturnos = models.BooleanField(max_length=10, default='', verbose_name='Terrores nocturnos', blank=True)
    sonambulismo = models.BooleanField(max_length=10, default='', verbose_name='Sonambulismo', blank=True)
    despierta_buen_humor = models.BooleanField(max_length=10, default='', verbose_name='Despierta de buen humor', blank=True)
    duerme = models.CharField(max_length=20, choices=opcion_como_duerme, default='', verbose_name='')
    especifique_2 = models.CharField(max_length=20, choices=opcion_relacion, default='Seleccione', verbose_name='Especifique:', blank=True)
    observaciones_7 = models.TextField(verbose_name='Observaciones', blank=True)


    def __str__(self):  
        return f'{self.nombre}, {self.fecha_nacimiento}, {self.domicilio}, {self.telefono}, {self.establecimiento}'
