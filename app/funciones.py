import re

#AQUÍ CREAREMOS DIFERENTES FUNCIONES QUE NOS VALIDEN CIERTOS ATRIBUTOS DE LOS MODELOS

#VALIDAR LONGITUD DEL RUT Y EL DÍGITO VERIFICADOR




def validar_rut(rut):
    # Función para validar el RUT chileno
    rut = rut.replace(".", "").replace("-", "")
    
    # Verifica que el formato del RUT sea correcto
    if not re.match(r'^\d{1,8}[-kK0-9]{1}$', rut):
        return False

    # Separa los dígitos del RUT y el dígito verificador
    rut_digits, check_digit = rut[:-1], rut[-1].lower()

    # Calcula el dígito verificador esperado
    calculated_check_digit = str((11 - sum(int(digit) * (i % 6 + 2) for i, digit in enumerate(reversed(rut_digits)))) % 11)
    
    # Si el cálculo resulta en 11, se considera como 0
    calculated_check_digit = '0' if calculated_check_digit == '11' else calculated_check_digit

    # Compara el dígito verificador calculado con el proporcionado y verifica si es válido
    return check_digit == calculated_check_digit if calculated_check_digit != '10' else check_digit == 'k'


#FUNCIÓN PARA PASAR DE PLURAL A SINGULAR LOS GRUPOS
def plural_singular(plural):
    plural_singular = {
        'Funcionarios': 'Funcionario',
        'Administradores': 'Administrador',
        'Coordinadores': 'Coordinador',
        'Psicopedagógos': 'Psicopedagógo',
        'Psicólogos': 'Psicólogo',
        'Terapeutas Ocupacionales': 'Terapeuta Ocupacional',
        'Fonoaudiologos': 'Fonoaudiologo',
        'Técnicos Diferenciales': 'Técnico Diferencial',
        'Técnicos Parvularios': 'Técnico Parvulario',
    }
    return plural_singular.get(plural, "error")





















