import re

#AQUÍ CREAREMOS DIFERENTES FUNCIONES QUE NOS VALIDEN CIERTOS ATRIBUTOS DE LOS MODELOS

#VALIDAR LONGITUD DEL RUT Y EL DÍGITO VERIFICADOR


def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").lower()
    rut = rut[:-1] + "-" + rut[-1]

    rut = rut.split("-")
    cuerpo_rut = rut[0]
    digito_verificador = rut[1]

    suma = 0
    multiplo = 2
    for i in reversed(cuerpo_rut):
        suma += int(i) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2

    digito_calculado = 11 - (suma % 11)
    if digito_calculado == 11:
        digito_calculado = 0
    elif digito_calculado == 10:
        digito_calculado = "k"

    return str(digito_calculado) == digito_verificador


# Ejemplo de uso:
if __name__ == "__main__":
    rut = "11111111-1"  # Aquí coloca el RUT que quieres validar
    if validar_rut(rut):
        print("El RUT es válido.")
    else:
        print("El RUT no es válido.")





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





















