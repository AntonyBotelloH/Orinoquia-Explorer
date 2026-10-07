
from django.urls import path
from .views import (
    listar_categoria, crear_categoria, editar_categoria, eliminar_categoria, ver_categoria,
    listar_experiencia, crear_experiencia, editar_experiencia, eliminar_experiencia, ver_experiencia,
    listar_resena
)

urlpatterns = [
    path('categoria/', listar_categoria, name='categoria_listar'),
    path('categoria/crear/', crear_categoria, name='categoria_crear'),
    path('categoria/ver/<int:id>/', ver_categoria, name='categoria_ver'),
    path('categoria/editar/<int:id>/', editar_categoria, name='categoria_editar'),
    path('categoria/eliminar/<int:id>/', eliminar_categoria, name='categoria_eliminar'),

    path('experiencia/', listar_experiencia, name='experiencia_listar'),
    path('experiencia/crear/', crear_experiencia, name='experiencia_crear'),
    path('experiencia/ver/<int:id>/', ver_experiencia, name='experiencia_ver'),
    path('experiencia/editar/<int:id>/', editar_experiencia, name='experiencia_editar'),
    path('experiencia/eliminar/<int:id>/', eliminar_experiencia, name='experiencia_eliminar'),

    path('resena/', listar_resena, name='resena_listar'),
]


