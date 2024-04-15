# ____________________________________________________________________________________________________________________________
#AQUÍ CREAREMOS UNA VISTA CUSTOMIZADA, A CUAL SE REUTILIZARA LAS VISTAS BASADAS EN CLASES

# class CustomTemplateView(TemplateView):
#     group_name = None # Variable para saber el grupo al que pertenece el usuario
#     group_name_singular = None # Variable para saber el singular del grupo
#     color = None # Variable para saber el color del grupo

#     # FUNCION PARA SABER EL GRUPO AL QUE PERTENECE EL USUARIO Y DARLE EL COLOR ASIGNADO A ESE GRUPO
#     def get_context_data(self, **kwargs): # Función para obtener la data
#         context = super().get_context_data(**kwargs) # Obtenemos la data de la superclase
#         user = self.request.user # Obtenemos el usuario que esta logeado
#         if user.is_authenticated:
#             group = Group.objects.filter(user=user).first() # Obtenemos el grupo al que pertenece el usuario
#             if group: # Si el grupo existe

#                 #PREGUNTAMOS POR EL GRUPO Y COLOR
#                 if group.name == 'Funcionarios':
#                     self.color = 'bg-zinc-950'
#                 elif group.name == 'Administradores':
#                     self.color = 'bg-gradient-to-tr from-gray-600 to-gray-900'
#                 elif group.name == 'Coordinadores':
#                     self.color = 'bg-gradient-to-tr from-lime-600 to-lime-900'
#                 elif group.name == 'Psicopedagógos':
#                     self.color = 'bg-gradient-to-tr from-purple-600 to-purple-900'
#                 elif group.name == 'Psicólogo':
#                     self.color = 'bg-gradient-to-tr from-indigo-600 to-indigo-900'
#                 elif group.name == 'Terapeutas Ocupacionales':
#                     self.color = 'red-600'
#                 elif group.name == 'Fonoaudiologos':
#                     self.color = 'bg-gradient-to-tr from-amber-600 to-amber-900'
#                 elif group.name == 'Técnicos Diferenciales':
#                     self.color = 'bg-gradient-to-tr from-pink-600 to-pink-900'
#                 elif group.name == 'Técnicos Parvularios':
#                     self.color = 'bg-gradient-to-tr from-green-600 to-green-900'


#                 self.group_name = group.name # Asignamos el nombre del grupo
#                 self.group_name_singular = plural_singular(group.name) # Obtenemos el singular del grupo
#         context['group_name'] = self.group_name # Asignamos el nombre del grupo
#         context['group_name_singular'] = self.group_name_singular # Asignamos el singular del grupo
#         context['color'] = self.color # Asignamos el color

#         return context # Retornamos el context