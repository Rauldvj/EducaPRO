from django.urls import path

#IMPORTAMOS LAS CLASES DE VISTAS (VIEWS)
from .views import IndexView, HomeView, RegisterView, ProfileView
    
#--------------------------------------------------------------------------------------
urlpatterns = [
    #URL INDEX (PAGINA PRINCIPAL)
    path('', IndexView.as_view(), name="index"), 

#--------------------------------------------------------------------------------------

    #URL DEL LOGIN
    path('login/', IndexView.as_view(), name="login"),

#--------------------------------------------------------------------------------------

    #URL DEL REGISTRO
    path('registro/', RegisterView.as_view(), name="registro"),
#--------------------------------------------------------------------------------------

    #URL HOME (PAGINA PRINCIPAL)
    path('home/', HomeView.as_view(), name="home"),

#--------------------------------------------------------------------------------------

    #URL DEL PERFIL
    path('perfil/', ProfileView.as_view(), name="perfil"),
]