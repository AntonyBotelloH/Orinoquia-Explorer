from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuario, name='listar_usuarios'),
    path('crear/', views.usuario, {'accion': 'C'}, name='crear_usuario'),
    path('<str:accion>/', views.usuario, name='usuario_sin_pk'),
    path('<int:pk>/<str:accion>/', views.usuario, name='usuario_accion'),
]


