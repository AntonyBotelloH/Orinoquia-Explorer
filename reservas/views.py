from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Reserva, PolizaSeguro
from .forms import ReservaForm, PolizaSeguroForm
from django.contrib import messages
from usuarios.decorators import rol_requerido

# ==================== RESERVAS ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_reserva(request):
    reservas = Reserva.objects.all()
    titulo = 'Reservas'
    context = {
        'reservas': reservas,
        'titulo': titulo,
    }
    return render(request, 'reservas/listar_reservas.html', context)

@rol_requerido('ADMIN', 'GUIA')
def ver_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reservas = Reserva.objects.all()
    detalles = [
        ('Turista / Usuario', f"{reserva.usuario.first_name} {reserva.usuario.last_name} ({reserva.usuario.documento})"),
        ('Experiencia', reserva.experiencia.nombre),
        ('Fecha', reserva.fecha.strftime('%d/%m/%Y') if reserva.fecha else 'N/A'),
        ('Número de Personas', reserva.numero_personas),
        ('Precio Total', f"${int(round(reserva.precio_total)):,}".replace(',', '.')),
        ('Estado', reserva.get_estado_display()),
    ]
    context = {
        'reservas': reservas,
        'titulo': 'Reserva',
        'objeto': reserva,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('reserva_listar'),
    }
    return render(request, 'reservas/listar_reservas.html', context)

@rol_requerido('ADMIN')
def crear_reserva(request):
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
    
    reservas = Reserva.objects.all()
    context = {
        'reservas': reservas,
        'titulo': titulo,
        'form': form,
        'accion': 'C',
        'url_listar': reverse('reserva_listar'),
    }
    return render(request, 'reservas/listar_reservas.html', context)

@rol_requerido('ADMIN')
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
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

    reservas = Reserva.objects.all()
    context = {
        'reservas': reservas,
        'titulo': titulo,
        'form': form,
        'objeto': reserva,
        'accion': 'U',
        'url_listar': reverse('reserva_listar'),
    }
    return render(request, 'reservas/listar_reservas.html', context)

@rol_requerido('ADMIN')
def eliminar_reserva(request, id):
    objeto = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        objeto.estado = 'CANCELADA'
        objeto.save()
        messages.success(request, 'Reserva cancelada correctamente.')
        return redirect('reserva_listar')

    reservas = Reserva.objects.all()
    context = {
        'reservas': reservas,
        'titulo': 'Reserva',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('reserva_listar'),
    }
    return render(request, 'reservas/listar_reservas.html', context)


# ==================== PÓLIZAS ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_poliza(request):
    polizas = PolizaSeguro.objects.all().order_by('fecha_expiracion')
    titulo = 'Pólizas de Seguro'
    context = {
        'polizas': polizas,
        'titulo': titulo,
    }
    return render(request, 'reservas/listar_polizas.html', context)

@rol_requerido('ADMIN', 'GUIA')
def ver_poliza(request, id):
    poliza = get_object_or_404(PolizaSeguro, id=id)
    polizas = PolizaSeguro.objects.all().order_by('fecha_expiracion')
    detalles = [
        ('Proveedor', poliza.proveedor),
        ('Número de Póliza', poliza.numero_poliza),
        ('Fecha de Expiración', poliza.fecha_expiracion.strftime('%d/%m/%Y') if poliza.fecha_expiracion else 'N/A'),
    ]
    context = {
        'polizas': polizas,
        'titulo': 'Póliza de Seguro',
        'objeto': poliza,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('poliza_listar'),
    }
    return render(request, 'reservas/listar_polizas.html', context)

@rol_requerido('ADMIN')
def crear_poliza(request):
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
    
    polizas = PolizaSeguro.objects.all().order_by('fecha_expiracion')
    context = {
        'polizas': polizas,
        'titulo': titulo,
        'form': form,
        'accion': 'C',
        'url_listar': reverse('poliza_listar'),
    }
    return render(request, 'reservas/listar_polizas.html', context)

@rol_requerido('ADMIN')
def editar_poliza(request, id):
    poliza = get_object_or_404(PolizaSeguro, id=id)
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

    polizas = PolizaSeguro.objects.all().order_by('fecha_expiracion')
    context = {
        'polizas': polizas,
        'titulo': titulo,
        'form': form,
        'objeto': poliza,
        'accion': 'U',
        'url_listar': reverse('poliza_listar'),
    }
    return render(request, 'reservas/listar_polizas.html', context)

@rol_requerido('ADMIN')
def eliminar_poliza(request, id):
    objeto = get_object_or_404(PolizaSeguro, id=id)
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, 'Póliza eliminada correctamente.')
        return redirect('poliza_listar')

    polizas = PolizaSeguro.objects.all().order_by('fecha_expiracion')
    context = {
        'polizas': polizas,
        'titulo': 'Póliza de Seguro',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('poliza_listar'),
    }
    return render(request, 'reservas/listar_polizas.html', context)

