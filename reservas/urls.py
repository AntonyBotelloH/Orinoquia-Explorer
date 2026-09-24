from django.urls import path
from .views import listar_reserva, crear_reserva, editar_reserva, eliminar_reserva, listar_poliza, crear_poliza, editar_poliza, eliminar_poliza

urlpatterns = [
    path('reserva/', listar_reserva, name='reserva_listar'),
    path('reserva/crear/', crear_reserva, name='reserva_crear'),
    path('reserva/editar/<int:id>/', editar_reserva, name='reserva_editar'),
    path('reserva/eliminar/<int:id>/', eliminar_reserva, name='reserva_eliminar'),

    path('poliza/', listar_poliza, name='poliza_listar'),
    path('poliza/crear/', crear_poliza, name='poliza_crear'),
    path('poliza/editar/<int:id>/', editar_poliza, name='poliza_editar'),
    path('poliza/eliminar/<int:id>/', eliminar_poliza, name='poliza_eliminar'),
]
