from django.shortcuts import render

def index_usuario(request):
    
    context = {
        
    }

    return render(request, "turismo/usuarios/index.html", context)