import re

#AQUÍ CREAREMOS DIFERENTES FUNCIONES QUE NOS VALIDEN CIERTOS ATRIBUTOS DE LOS MODELOS

#FUNCIÓN PARA PASAR DE PLURAL A SINGULAR LOS GRUPOS
def plural_singular(plural):
    plural_singular = {
        'Funcionarios': 'Funcionario',
        'Administradores': 'Administrador',
        'Coordinadores': 'Coordinador',
        'Coordinadores Suplentes': 'Coordinador Suplente',
        'Psicopedagógos': 'Psicopedagógo',
        'Psicólogos': 'Psicólogo',
        'Terapeutas Ocupacionales': 'Terapeuta Ocupacional',
        'Fonoaudiologos': 'Fonoaudiologo',
        'Técnicos Diferenciales': 'Técnico Diferencial',
        'Técnicos Parvularios': 'Técnico Parvulario',
    }
    return plural_singular.get(plural, "error")





















