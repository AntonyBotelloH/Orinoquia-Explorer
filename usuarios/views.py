from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import rol_requerido
from .models import Usuario
from .forms import UsuarioForm, UsuarioEditarForm, PerfilUsuarioForm
from reservas.models import Reserva

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


@login_required
def mi_perfil(request):
    user = request.user
    layout = request.GET.get('layout')
    if layout == 'admin':
        base_template = 'partials/base-admin.html'
    elif layout == 'user':
        base_template = 'partials/base-user.html'
    else:
        base_template = 'partials/base-admin.html' if (user.rol in ['ADMIN', 'GUIA'] or user.is_superuser) else 'partials/base-user.html'

    form_perfil = PerfilUsuarioForm(instance=user)
    form_password = PasswordChangeForm(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        redirect_url = reverse('perfil')
        if layout:
            redirect_url += f'?layout={layout}'

        if action == 'update_profile':
            form_perfil = PerfilUsuarioForm(request.POST, instance=user)
            if form_perfil.is_valid():
                form_perfil.save()
                messages.success(request, '¡Tu información de perfil ha sido actualizada!')
                return redirect(redirect_url)
            else:
                for campo, errores in form_perfil.errors.items():
                    for err in errores:
                        messages.error(request, f"Error en '{campo.capitalize()}': {err}")

        elif action == 'change_password':
            form_password = PasswordChangeForm(user=user, data=request.POST)
            if form_password.is_valid():
                user_updated = form_password.save()
                update_session_auth_hash(request, user_updated)
                messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente!')
                return redirect(redirect_url)
            else:
                for campo, errores in form_password.errors.items():
                    for err in errores:
                        messages.error(request, f"Error en contraseña: {err}")

    mis_reservas = Reserva.objects.filter(usuario=user).select_related('experiencia').order_by('-fecha')
    context = {
        'titulo': 'Mi Perfil',
        'base_template': base_template,
        'form_perfil': form_perfil,
        'form_password': form_password,
        'mis_reservas': mis_reservas,
        'total_reservas': mis_reservas.count(),
        'layout': layout,
    }
    return render(request, "perfil.html", context)
