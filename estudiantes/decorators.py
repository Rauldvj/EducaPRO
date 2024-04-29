from django.utils.decorators import method_decorator
from .models import Estudiante, ApoderadoTitular, ApoderadoSuplente1, ApoderadoSuplente2


def get_color_for_model(instance):
    if isinstance(instance, Estudiante):
        return 'bg-gradient-to-tr from-blue-600 to-blue-900'
    elif isinstance(instance, ApoderadoTitular):
        return 'bg-gradient-to-tr from-green-600 to-green-900'
    elif isinstance(instance, ApoderadoSuplente1):
        return 'bg-gradient-to-tr from-yellow-600 to-yellow-900'
    elif isinstance(instance, ApoderadoSuplente2):
        return 'bg-gradient-to-tr from-red-600 to-red-900'
    else:
        return None

def add_color_to_context(view_class):
    original_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        # Obtener la instancia del modelo si está presente en los argumentos de la vista
        model_instance = None
        for arg in args:
            if isinstance(arg, (Estudiante, ApoderadoTitular, ApoderadoSuplente1, ApoderadoSuplente2)):
                model_instance = arg
                break

        # Si se encontró una instancia del modelo, obtener su color
        color = get_color_for_model(model_instance)

        # Agregar el color al contexto
        self.extra_context = {'color': color}

        # Llamar a la vista original
        return original_dispatch(self, request, *args, **kwargs)

    view_class.dispatch = dispatch
    return view_class

