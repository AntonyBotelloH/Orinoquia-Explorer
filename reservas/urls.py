from django.urls import path
from .views import listar_reserva, crear_reserva, editar_reserva, eliminar_reserva

urlpatterns = [
    path('reserva/', listar_reserva, name='reserva_listar'),
    path('reserva/crear/', crear_reserva, name='reserva_crear'),
    path('reserva/editar/<int:id>/', editar_reserva, name='reserva_editar'),
    path('reserva/eliminar/<int:id>/', eliminar_reserva, name='reserva_eliminar'),
]
