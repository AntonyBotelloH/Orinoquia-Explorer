
from django.contrib import admin
from django.urls import path
from .views import listar_categoria, crear_categoria, listar_experiencia, crear_experiencia, listar_resena, editar_categoria, eliminar_categoria
urlpatterns = [
    path('categoria/', listar_categoria, name='categoria_listar'),
    path('categoria/crear/', crear_categoria, name='categoria_crear'),
    path('categoria/editar/<int:id>/', editar_categoria, name='categoria_editar'),
    path('categoria/eliminar/<int:id>/', eliminar_categoria, name='categoria_eliminar'),

    path('experiencia/', listar_experiencia, name='experiencia_listar'),
    path('experiencia/crear/', crear_experiencia, name='experiencia_crear'),

    path('resena/', listar_resena, name='resena_listar'),
]


