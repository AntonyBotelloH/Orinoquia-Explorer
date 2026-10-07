from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .decorators import rol_requerido
from .models import Usuario
from .forms import UsuarioForm, UsuarioEditarForm

# Create your views here.

@rol_requerido('ADMIN', 'GUIA')
def usuario(request, pk='', accion=''):
    usuarios = Usuario.objects.all()
    user = None
    form = UsuarioForm() # Formulario por defecto (para crear)

    # 1. READ: Consultar usuario para ver detalles en modal
    if accion == 'R' and pk:
        user = get_object_or_404(Usuario, id=pk)

    # 2. CREATE: Crear un nuevo usuario
    elif accion == 'C':
        if request.user.rol != 'ADMIN' and not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para crear usuarios.')
            return redirect('listar_usuarios')
            
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario creado correctamente.')
                return redirect('listar_usuarios')
            else:
                for campo, errores in form.errors.items():
                    for error in errores:
                        messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")
        else:
            form = UsuarioForm()

    # 3. UPDATE: Actualizar datos de un usuario existente
    elif accion == 'U' and pk:
        if request.user.rol != 'ADMIN' and not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para editar usuarios.')
            return redirect('listar_usuarios')
            
        user = get_object_or_404(Usuario, id=pk)
        if request.method == 'POST':
            form = UsuarioEditarForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario actualizado correctamente.')
                return redirect('listar_usuarios')
            else:
                for campo, errores in form.errors.items():
                    for error in errores:
                        messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")
        else:
            form = UsuarioEditarForm(instance=user)

    # 4. DELETE: Eliminar usuario
    elif accion == 'D' and pk:
        if request.user.rol != 'ADMIN' and not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para eliminar usuarios.')
            return redirect('listar_usuarios')
            
        user = get_object_or_404(Usuario, id=pk)
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'Usuario eliminado correctamente.')
            return redirect('listar_usuarios')

    context = {
        'titulo': 'Gestión de Usuarios',
        'usuarios': usuarios,
        'user': user,
        'form': form,
        'accion': accion,
        'pk': pk,
    }
    return render(request, "listar_usuarios.html", context)
