from django.urls import path, include
from . import views

urlpatterns = [
    # Páginas de cara al usuario
    path('', views.index_usuario, name='index_usuario'),
    path('destinos/', views.destinos_usuario, name='destinos_usuario'),
    path('cultura-y-gastronomia/', views.cultura_usuario, name='cultura_usuario'),
    path('contacto/', views.contacto_usuario, name='contacto_usuario'),
    path('reservar/', views.reservar_usuario, name='reservar_usuario'),

    # Utilidades y reservas
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('api/clima-fecha/', views.api_clima_fecha, name='api_clima_fecha'),
    path('solicitar-reserva/<int:exp_id>/', views.solicitar_reserva, name='solicitar_reserva'),

    # Admin: Gestión de Destinos
    path('administracion/destinos/', views.listar_destino, name='destino_listar'),
    path('administracion/destinos/ver/<int:id>/', views.ver_destino, name='destino_ver'),
    path('administracion/destinos/crear/', views.crear_destino, name='destino_crear'),
    path('administracion/destinos/editar/<int:id>/', views.editar_destino, name='destino_editar'),
    path('administracion/destinos/eliminar/<int:id>/', views.eliminar_destino, name='destino_eliminar'),

    # Admin: Gestión de Cultura y Gastronomía
    path('administracion/cultura/', views.listar_cultura, name='cultura_listar'),
    path('administracion/cultura/ver/<int:id>/', views.ver_cultura, name='cultura_ver'),
    path('administracion/cultura/crear/', views.crear_cultura, name='cultura_crear'),
    path('administracion/cultura/editar/<int:id>/', views.editar_cultura, name='cultura_editar'),
    path('administracion/cultura/eliminar/<int:id>/', views.eliminar_cultura, name='cultura_eliminar'),

    # Admin: Gestión de Mensajes de Contacto
    path('administracion/contacto/', views.listar_contacto, name='contacto_listar'),
    path('administracion/contacto/ver/<int:id>/', views.ver_contacto, name='contacto_ver'),
    path('administracion/contacto/eliminar/<int:id>/', views.eliminar_contacto, name='contacto_eliminar'),

    # Módulo Usuarios
    path('usuarios/', include('usuarios.urls')),
]

