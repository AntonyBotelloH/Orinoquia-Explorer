from django.shortcuts import render
from .decorators import rol_requerido
from .models import Usuario
# Create your views here.


@rol_requerido('ADMIN', 'GUIA')
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    context = {
        "titulo": "Listar Usuarios",
        "usuarios": usuarios
    }
    return render(request, "listar_usuarios.html", context)