from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_usuario, name='index_usuario'),
    path('usuarios/', include('usuarios.urls')),
]
