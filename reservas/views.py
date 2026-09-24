from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva, PolizaSeguro
from .forms import ReservaForm, PolizaSeguroForm
from django.contrib import messages
from usuarios.decorators import rol_requerido

@rol_requerido('ADMIN', 'GUIA')
def listar_reserva(request):
    reservas = Reserva.objects.all()
    titulo = 'Reservas'
    context = {
        'reservas': reservas,
        'titulo': titulo
    }
    return render(request, 'reservas/listar_reservas.html', context)

@rol_requerido('ADMIN')
def crear_reserva(request):
    accion = 'Crear'
    titulo = 'Reserva'
    form = ReservaForm()
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva creada correctamente.')
            return redirect('reserva_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")
    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }
    return render(request, 'partials/base-creacion.html', context)

@rol_requerido('ADMIN')
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    accion = 'Editar'
    titulo = 'Reserva'
    form = ReservaForm(instance=reserva)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('reserva_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")

    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }
    return render(request, 'partials/base-creacion.html', context)

@rol_requerido('ADMIN')
def eliminar_reserva(request, id):
    objeto = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        objeto.estado = 'CANCELADA'
        objeto.save()
        messages.success(request, 'Reserva cancelada correctamente.')
    return redirect('reserva_listar')

@rol_requerido('ADMIN', 'GUIA')
def listar_poliza(request):
    polizas = PolizaSeguro.objects.all().order_by('fecha_expiracion')
    titulo = 'Pólizas de Seguro'
    context = {
        'polizas': polizas,
        'titulo': titulo
    }
    return render(request, 'reservas/listar_polizas.html', context)

@rol_requerido('ADMIN')
def crear_poliza(request):
    accion = 'Crear'
    titulo = 'Póliza de Seguro'
    form = PolizaSeguroForm()
    if request.method == 'POST':
        form = PolizaSeguroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Póliza creada correctamente.')
            return redirect('poliza_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")
    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }
    return render(request, 'partials/base-creacion.html', context)

@rol_requerido('ADMIN')
def editar_poliza(request, id):
    poliza = get_object_or_404(PolizaSeguro, id=id)
    accion = 'Editar'
    titulo = 'Póliza de Seguro'
    form = PolizaSeguroForm(instance=poliza)
    if request.method == 'POST':
        form = PolizaSeguroForm(request.POST, instance=poliza)
        if form.is_valid():
            form.save()
            messages.success(request, 'Póliza actualizada correctamente.')
            return redirect('poliza_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")

    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }
    return render(request, 'partials/base-creacion.html', context)

@rol_requerido('ADMIN')
def eliminar_poliza(request, id):
    objeto = get_object_or_404(PolizaSeguro, id=id)
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, 'Póliza eliminada correctamente.')
    return redirect('poliza_listar')
