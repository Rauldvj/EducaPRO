from django.urls import path

#IMPORTAMOS LAS CLASES DE VISTAS (VIEWS)
from .views import IndexView, HomeView, RegisterView, ProfileView, superuser_edit, ErrorView, CustomLoginView, ProfilePasswordChangeView\
,AddUserView, UserDetailView, AnamnesisView

from estudiantes.views import EstudianteView

from pie.views import ListPieView
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
    path('profile/', login_required(ProfileView.as_view()), name="profile"),

#--------------------------------------------------------------------------------------

    #URL DE DETALLE DEL USUARIO
    path('profile_detail/<int:pk>/', login_required(UserDetailView.as_view()), name="profile_detail"),

    #EDITAR DATOS DE UN USUARIO
    path('superuser_edit/<int:user_id>', login_required(superuser_edit), name='superuser_edit'),


    #URL DE CAMBIO DE CONTRASEÑA
    path('password_change/', login_required(ProfilePasswordChangeView.as_view()), name="profile_password_change"),

    #AGREGAR NUEVO USUARIO POR EL COORDINADOR O ADMINISTRADOR   
    path('add_user/', login_required(AddUserView.as_view()), name="add_user"),

    #LOGIN PERSONALIZADO
    path('custom_login/', CustomLoginView.as_view(), name="custom_login"),

    #URL DE ESTUDIANTES
    path('estudiante/', login_required(EstudianteView.as_view()), name="estudiante"),

    #URL DE REGISTRO DE PIE
    path('pie/', login_required(ListPieView.as_view()), name="pie"),

    #URL PARA REGISTRO DE INFORME ANAMNESIS
    path('anamnesis/', login_required(AnamnesisView.as_view()), name="anamnesis"),
]