from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_usuario, name='index_usuario'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('api/clima-fecha/', views.api_clima_fecha, name='api_clima_fecha'),
    path('solicitar-reserva/<int:exp_id>/', views.solicitar_reserva, name='solicitar_reserva'),
    path('usuarios/', include('usuarios.urls')),
]
