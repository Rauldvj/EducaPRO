from django.utils.decorators import method_decorator # Importamos decoradores
from .funciones import plural_singular

def add_group_name_to_context(view_class):
    original_dispatch = view_class.dispatch # Obtenemos el dispatch original

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        group = user.groups.first() # Obtenemos el grupo al que pertenece el usuario
        group_name = None # Variable para saber el grupo al que pertenece el usuario
        group_name_singular = None # Variable para saber el singular del grupo
        color = None # Variable para saber el color del grupo


        if group: # Si el grupo existe

            #PREGUNTAMOS POR EL GRUPO Y COLOR
            if group.name == 'Funcionarios':
                color = 'bg-zinc-950'
            elif group.name == 'Administradores':
                color = 'bg-gradient-to-tr from-gray-600 to-gray-900'
            elif group.name == 'Coordinadores':
                color = 'bg-gradient-to-tr from-lime-600 to-lime-900'
            elif group.name == 'Psicopedagógos':
                color = 'bg-gradient-to-tr from-purple-600 to-purple-900'
            elif group.name == 'Psicólogo':
                color = 'bg-gradient-to-tr from-indigo-600 to-indigo-900'
            elif group.name == 'Terapeutas Ocupacionales':
                color = 'red-600'
            elif group.name == 'Fonoaudiologos':
                color = 'bg-gradient-to-tr from-amber-600 to-amber-900'
            elif group.name == 'Técnicos Diferenciales':
                color = 'bg-gradient-to-tr from-pink-600 to-pink-900'
            elif group.name == 'Técnicos Parvularios':
                color = 'bg-gradient-to-tr from-green-600 to-green-900'
            group_name = group.name # Asignamos el nombre del grupo
            group_name_singular = plural_singular(group.name) # Obtenemos el singular del grupo

        context = { # Creamos el contexto
            'group_name': group_name, # Asignamos el nombre del grupo
            'group_name_singular': group_name_singular, # Asignamos el singular del grupo
            'color': color # Asignamos el color
        }
        self.extra_context = context # Asignamos el contexto
        return original_dispatch(self, request, *args, **kwargs) # Retornamos el dispatch

    view_class.dispatch = dispatch #
    return view_class # Retornamos la vista