from django.shortcuts import render
from .decorators import rol_requerido
# Create your views here.

@rol_requerido('ADMIN', 'GUIA')
def listar_usuarios(request):
    context = {
        "titulo": "Listar Usuarios"
    }
    return render(request, "listar_usuarios.html", context)