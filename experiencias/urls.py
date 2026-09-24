
from django.contrib import admin
from django.urls import path
from .views import listar_categoria, crear_categoria, listar_experiencia, crear_experiencia, listar_resena, crear_resena, editar_resena, eliminar_resena, editar_categoria, eliminar_categoria, editar_experiencia, eliminar_experiencia
urlpatterns = [
    path('categoria/', listar_categoria, name='categoria_listar'),
    path('categoria/crear/', crear_categoria, name='categoria_crear'),
    path('categoria/editar/<int:id>/', editar_categoria, name='categoria_editar'),
    path('categoria/eliminar/<int:id>/', eliminar_categoria, name='categoria_eliminar'),

    path('experiencia/', listar_experiencia, name='experiencia_listar'),
    path('experiencia/crear/', crear_experiencia, name='experiencia_crear'),
    path('experiencia/editar/<int:id>/', editar_experiencia, name='experiencia_editar'),
    path('experiencia/eliminar/<int:id>/', eliminar_experiencia, name='experiencia_eliminar'),

    path('resena/', listar_resena, name='resena_listar'),
    path('resena/crear/', crear_resena, name='resena_crear'),
    path('resena/editar/<int:id>/', editar_resena, name='resena_editar'),
    path('resena/eliminar/<int:id>/', eliminar_resena, name='resena_eliminar'),
]


