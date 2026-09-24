from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),
]
