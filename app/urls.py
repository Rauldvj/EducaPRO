from django.urls import path

#IMPORTAMOS LAS CLASES DE VISTAS (VIEWS)
from .views import IndexView, HomeView, RegisterView, ProfileView, ErrorView

#IMPORTAMOS UN HELPER (AYUDA), PARA PROTEGER LOS FORMULARIOS Y REGISTROS (ROLES Y PERMISOS DE ACCESO)
from django.contrib.auth.decorators import login_required
    
#--------------------------------------------------------------------------------------
urlpatterns = [

    #URL DE PAGINA DE ERRO
    path('error/', login_required(ErrorView.as_view()), name="error"),


    #--------------------------------------------------------------------------------------

    #URL INDEX (PAGINA PRINCIPAL)
    path('', IndexView.as_view(), name="index"), 

#--------------------------------------------------------------------------------------

    #URL DEL LOGIN
    path('login/', IndexView.as_view(), name="login"),

#--------------------------------------------------------------------------------------

    #URL DEL REGISTRO
    path('registro/', login_required(RegisterView.as_view()), name="registro"),
#--------------------------------------------------------------------------------------

    #URL HOME (PAGINA PRINCIPAL)
    path('home/', login_required(HomeView.as_view()), name="home"),

#--------------------------------------------------------------------------------------

    #URL DEL PERFIL
    path('perfil/', login_required(ProfileView.as_view()), name="perfil"),
]