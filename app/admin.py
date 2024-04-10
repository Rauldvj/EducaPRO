from django.contrib import admin
from .models import *


# REGISTRAR BITACORA ESTUDIANTE

class BitacoraAdmin(admin.ModelAdmin): 
    list_display = ['fecha', 'hora_entrada', 'hora_salida', 'estudiante']
    search_fields = ['estudiante']
    fieldsets = (
        ('BITACORA ESTUDIANTE', {
            'fields': ('fecha', 'hora_entrada', 'hora_salida', 'estudiante'),
        }),
        ('PRIMER BLOQUE', {
            'fields': ('bloque1', 'objetivoClase1', 'objetivoPaci1', 'desarrolloActividad1', 'material1', 'personaMaterial1', 'reaccion1', 'estadoAprendizaje1', 'apoyoDocente1', 'obervacionesGenerales1'),
        }),
        ('SEGUNDO BLOQUE', {
            'fields': ('bloque2b', 'objetivoClase2b', 'objetivoPaci2b', 'desarrolloActividad2b', 'material2b', 'personaMaterial2b', 'reaccion2b', 'estadoAprendizaje2b', 'apoyoDocente2b', 'obervacionesGenerales2b'),
        }),
        ('TERCER BLOQUE', {
            'fields': ('bloque3c', 'objetivoClase3c', 'objetivoPaci3c', 'desarrolloActividad3c', 'material3c', 'personaMaterial3c', 'reaccion3c', 'estadoAprendizaje3c', 'apoyoDocente3c', 'obervacionesGenerales3c'),
        }),
        ('CUARTO BLOQUE', {
            'fields': ('bloque4d', 'objetivoClase4d', 'objetivoPaci4d', 'desarrolloActividad4d', 'material4d', 'personaMaterial4d', 'reaccion4d', 'estadoAprendizaje4d', 'apoyoDocente4d', 'obervacionesGenerales4d'),
        })
    )

admin.site.register(Bitacora, BitacoraAdmin)


#REGISTRAR ANAMNESIS

class AnamnesisAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sexo', 'fecha_nacimiento', 'años']
    search_fields = ['nombre']
    fieldsets = (
        ('1. IDENTIFICACION DEL ESTUDIANTE', {
            'fields': ('nombre', 'sexo', 'fecha_nacimiento', 'años', 'meses', 'pais', 'domicilio', 'telefono',\
                        'lengua_materna', 'comprende_materna', 'habla_materna',  'lee_materna', 'escribe_materna',\
                        'lengua_uso', 'comprende_uso', 'habla_uso', 'lee_uso', 'escribe_uso' , 'escolaridad_actual','establecimiento'),
        }),
        ('2. IDENTIFICACIÓN DEL O LOS INFORMANTES', {
            'fields': ( 'fecha_entrevista_1', 'nombres_entrevista_1', 'relacion_estudiante_1', 'en_presencia_de_1',\
                        'fecha_entrevista_2', 'nombres_entrevista_2', 'relacion_estudiante_2', 'en_presencia_de_2',\
                        'fecha_entrevista_3', 'nombres_entrevista_3', 'relacion_estudiante_3', 'en_presencia_de_3',\
                        'fecha_entrevista_4', 'nombres_entrevista_4', 'relacion_estudiante_4', 'en_presencia_de_4',),
        }),
        ('3. IDENTIFICACIÓN DEL ENTREVISTADOR', {
            'fields': ('fecha_entrevistador', 'nombreApellidos', 'rol', \
                       'fecha_entrevistador_2', 'nombreApellidos_2', 'rol_2',\
                       'fecha_entrevistador_3', 'nombreApellidos_3', 'rol_3', \
                        'fecha_entrevistador_4', 'nombreApellidos_4', 'rol_4'),
        }),
        ('4. DEFINICIÓN DEL PROBLEMA O SITUACIÓN QUE MOTIVA LA ENTREVISTA', {
            'fields': ('definicionProblema',),
        }),
        ('5. ANTECEDENTES RELATIVOS AL DESARROLLO Y A LA SALUD DEL/LA ESTUDIANTE', {
            'fields': ('pediatria', 'kinesiologia', 'genetico', 'fonoaudiologia', 'neurologia',\
                        'psicologia', 'psiquiatria', 'psicopedagogia', 'terapiaocupacional', 'otro'),
        }),
        ('6. PRIMER AÑO DE VIDA', {
            'fields': ('tipo_parto', 'cesarea', 'asistencia_medica_parto', 'peso', 'talla', 'antecedentes_embarazo_parto',),
         }),
        ('Señale si durante los doce primeros meses de vida el niño o niña presentó:', {
            'fields': ('desnutricion', 'obesidad', 'fiebre_alta', 'convulsiones', 'hospitalizaciones', 'hospitalizacion',\
            'traumatismos', 'intoxicacion', 'enfermedad_respiratoria', 'asma', 'encefalitis',\
            'meningitis', 'otra', 'control_periodico_salud', 'vacunas', 'observaciones'),
        }),
        ('5.2. Desarrollo Sensorio Motriz', {
            'fields': ('fija_la_cabeza', 'se_sienta_solo', 'camina_sin_apoyo', 'primeras_palabras', 'primeras_frases', \
            'se_viste_solo', 'controla_esfinter_vesical', 'controla_esfinter_anal', 'observaciones_2', \
            'actividad_motora_general', 'tono_muscular_general'),
        }),
        ('En relación con su motricidad gruesa se aprecia:', {
            'fields': ('estabilidad_caminar', 'caida_frecuente', 'dominancia_lateral'),
        }),
        ('5.3. Desarrollo Sensorio Emocional', {
            'fields': ('garra', 'ensarta', 'presion', 'dibuja', 'pinza', 'escribe')
        }),
        ('En relación con algunos signos cognitivos el niño(a)', {
            'fields': ('reaccion_voces_caras', 'demanda_obj_comp', 'sonr_balb_gri_llo', 'manipula_explora',\
                        'comprende_prohibiciones', 'disc_ojo_mano', 'observaciones_3')
        }),
        ('5.3. Visión - Audición:', {
            'fields': ('estimulos_visuales', 'ojos_irrt_llor', 'dolores_cabeza', 'acerca_aleja', 'sigue_con_vista', 'presenta_movimientos', \
            'man_cond_erron', 'diag_medico', 'estimulo_auditivo', 'voces_sonidos', 'gira_cabeza', 'acerca_oidos', \
            'tapa_golpea_ojo', 'dolor_oidos', 'pronunciacion_oral', 'otitis_hipo_otra', 'observaciones_4')
        }),
        ('5.4. Desarrollo Sensorio Espacial', {
            'fields': ('nino_comunica', 'especifique')
        }),
        ('Características del lenguaje expresivo', {
            'fields': ('balbucea', 'vocaliza', 'emite_palabras', 'emite_produce', 'relata_expeciencias', 'emision_pronunciacion')
        }),
        ('Características del lenguaje comprensivo', {
            'fields': ('identifica_objetos', 'identifica_personas', 'comprende_conceptos', 'responde_coherente', 'instrucciones_simples',\
            'instrucciones_complejas', 'instrucciones_grupales', 'comprende_relatos', 'perdida_lenguaje', 'observaciones_5')
        }),
        ('5.5. Desarrollo Social', {
            'fields': ('espontaneamente', 'comportamiento_actitudes', 'actividades_grupales', 'trabajo_individual', 'lenguaje_ecolalico', \
            'dificultad_adaptarse', 'forma_colaborativa', 'normas_sociales', 'normas_escolares', 'sentido_humor',\
            'movimientos_estereotipados', 'pataletas_frecuentes',)
        }),
        ('Ante los siguientes estímulos su reacción es:', {
            'fields': ('luces', 'sonidos', 'personas_extranas', 'observaciones_6',)
        }),
        ('5.6. Estado Actual de Salud del/la Estudiante', {
            'fields': ('vacunas_al_dia', 'epilepsia', 'problemas_cardiacos', 'paraplejia', 'perdida_auditiva', 'perdida_visual', \
            'trastorno_motor', 'prob_bronco_resp', 'enf_infect_cont', 'trastorno_emocional', 'trastorno_conductual', 'otro_1', \
            'problemas_salud', )
        }),
        ('Alimentacion', {
            'fields': ('alimentacion', 'otro_2')
        }),
        ('Peso (apreciación del informante): ', {
            'fields': ('peso_apreciacion',)
        }),
        ('Sueño', {
            'fields': ('sueno', 'horas_sueno', 'insomnio', 'pesadillas', 'terrores_nocturnos', 'sonambulismo', 'despierta_buen_humor',\
                        'duerme', 'especifique_2', 'observaciones_7')
        })    
    )

admin.site.register(Anamnesis, AnamnesisAdmin)
