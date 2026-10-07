from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_usuario, name='index_usuario'),
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('usuarios/', include('usuarios.urls')),
]
