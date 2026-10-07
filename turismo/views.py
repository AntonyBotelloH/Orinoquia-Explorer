from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from usuarios.decorators import rol_requerido
from usuarios.models import Usuario
from experiencias.models import Categoria, Experiencia
from reservas.models import Reserva, PolizaSeguro
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .clima import consultar_pronostico_fecha
import json

def index_usuario(request):
    categoria_id = request.GET.get('categoria')
    q = request.GET.get('q', '').strip()

    # Experiencias activas subidas en la plataforma
    experiencias_qs = Experiencia.objects.filter(estado=True).select_related('categoria')

    if categoria_id and categoria_id.isdigit():
        experiencias_qs = experiencias_qs.filter(categoria_id=int(categoria_id))

    if q:
        experiencias_qs = experiencias_qs.filter(
            Q(nombre__icontains=q) | 
            Q(descripcion__icontains=q) | 
            Q(categoria__nombre__icontains=q)
        )

    experiencias = list(experiencias_qs.order_by('-id'))

    # Categorías activas con conteo real de experiencias
    categorias = (
        Categoria.objects.filter(estado=True)
        .annotate(num_exp=Count('experiencia', filter=Q(experiencia__estado=True)))
        .filter(num_exp__gt=0)
        .order_by('-num_exp')
    )

    total_activas = Experiencia.objects.filter(estado=True).count()
    destacada = Experiencia.objects.filter(estado=True).order_by('-precio').first()

    context = {
        'titulo': 'Inicio | Descubre la Orinoquia',
        'experiencias': experiencias,
        'total_activas': total_activas,
        'total_encontradas': len(experiencias),
        'categorias': categorias,
        'categoria_actual': int(categoria_id) if (categoria_id and categoria_id.isdigit()) else None,
        'busqueda': q,
        'destacada': destacada,
    }
    return render(request, "turismo/usuarios/index.html", context)

@rol_requerido('ADMIN', 'GUIA')
def dashboard_admin(request):
    # Conteo de usuarios por rol
    total_usuarios = Usuario.objects.count()
    turistas_count = Usuario.objects.filter(rol='TURISTA').count()
    guias_count = Usuario.objects.filter(rol='GUIA').count()
    admins_count = Usuario.objects.filter(rol='ADMIN').count()

    # Experiencias y categorías
    total_experiencias = Experiencia.objects.count()
    experiencias_activas = Experiencia.objects.filter(estado=True).count()
    total_categorias = Categoria.objects.count()

    # Reservas y estados
    total_reservas = Reserva.objects.count()
    reservas_confirmadas = Reserva.objects.filter(estado='CONFIRMADA').count()
    reservas_pendientes = Reserva.objects.filter(estado='PENDIENTE').count()
    reservas_canceladas = Reserva.objects.filter(estado='CANCELADA').count()

    # Ingresos y pólizas
    total_ingresos = Reserva.objects.filter(estado='CONFIRMADA').aggregate(total=Sum('precio_total'))['total'] or 0
    polizas_vigentes = PolizaSeguro.objects.filter(fecha_expiracion__gte=timezone.now().date()).count()

    # Experiencias por categoría
    categorias_qs = Categoria.objects.annotate(num_exp=Count('experiencia')).order_by('-num_exp')[:8]
    cat_nombres = [c.nombre for c in categorias_qs]
    cat_cantidades = [c.num_exp for c in categorias_qs]

    # Reservas por mes del año actual
    current_year = timezone.now().year
    meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    reservas_por_mes = [0] * 12
    ingresos_por_mes = [0] * 12

    for r in Reserva.objects.filter(fecha__year=current_year):
        if r.fecha:
            m_idx = r.fecha.month - 1
            reservas_por_mes[m_idx] += 1
            if r.estado == 'CONFIRMADA' and r.precio_total:
                ingresos_por_mes[m_idx] += float(r.precio_total)

    # Últimas reservas registradas
    ultimas_reservas = Reserva.objects.select_related('usuario', 'experiencia').order_by('-id')[:6]

    context = {
        'titulo': 'Dashboard Administrativo',
        'total_usuarios': total_usuarios,
        'turistas_count': turistas_count,
        'guias_count': guias_count,
        'admins_count': admins_count,
        'total_experiencias': total_experiencias,
        'experiencias_activas': experiencias_activas,
        'total_categorias': total_categorias,
        'total_reservas': total_reservas,
        'reservas_confirmadas': reservas_confirmadas,
        'reservas_pendientes': reservas_pendientes,
        'reservas_canceladas': reservas_canceladas,
        'total_ingresos': total_ingresos,
        'polizas_vigentes': polizas_vigentes,
        'ultimas_reservas': ultimas_reservas,
        # Datos formateados en JSON para Chart.js
        'chart_reservas_estado': json.dumps({
            'labels': ['Confirmadas', 'Pendientes', 'Canceladas'],
            'data': [reservas_confirmadas, reservas_pendientes, reservas_canceladas]
        }),
        'chart_usuarios_rol': json.dumps({
            'labels': ['Turistas', 'Guías', 'Administradores'],
            'data': [turistas_count, guias_count, admins_count]
        }),
        'chart_categorias': json.dumps({
            'labels': cat_nombres,
            'data': cat_cantidades
        }),
        'chart_meses': json.dumps({
            'labels': meses_nombres,
            'reservas': reservas_por_mes,
            'ingresos': ingresos_por_mes
        }),
    }
    return render(request, "turismo/administracion/index.html", context)


def api_clima_fecha(request):
    """
    Endpoint JSON que retorna el pronóstico o clima estacional
    para una fecha seleccionada en los formularios de reserva.
    """
    fecha = request.GET.get('fecha')
    if not fecha:
        return JsonResponse({'valido': False, 'error': 'No se proporcionó ninguna fecha'}, status=400)
    data = consultar_pronostico_fecha(fecha)
    return JsonResponse(data)


@login_required
def solicitar_reserva(request, exp_id):
    """
    Permite a los turistas autenticados solicitar y registrar una reserva
    directamente desde el catálogo de experiencias.
    """
    if request.method != 'POST':
        return redirect('index_usuario')

    experiencia = get_object_or_404(Experiencia, id=exp_id, estado=True)
    fecha = request.POST.get('fecha')
    numero_personas = request.POST.get('numero_personas', 1)
    peticiones = request.POST.get('peticiones_especiales', '').strip()

    if not fecha:
        messages.error(request, 'Debes seleccionar una fecha para tu reserva.')
        return redirect(f"{reverse('index_usuario')}#catalogo")

    try:
        num_p = max(1, int(numero_personas))
    except (ValueError, TypeError):
        num_p = 1

    precio_total = Decimal(str(experiencia.precio)) * Decimal(num_p)

    Reserva.objects.create(
        usuario=request.user,
        experiencia=experiencia,
        fecha=fecha,
        numero_personas=num_p,
        precio_total=precio_total,
        estado='PENDIENTE',
        peticiones_especiales=peticiones
    )

    messages.success(
        request,
        f'¡Excelente! Tu reserva para "{experiencia.nombre}" ha sido solicitada con éxito para el {fecha}. '
        f'Revisa los detalles en tu perfil.'
    )
    return redirect(f"{reverse('perfil')}?layout=user#tab-reservas")