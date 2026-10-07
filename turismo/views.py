from django.shortcuts import render
from usuarios.decorators import rol_requerido
from usuarios.models import Usuario
from experiencias.models import Categoria, Experiencia
from reservas.models import Reserva, PolizaSeguro
from django.db.models import Count, Sum
from django.utils import timezone
import json

def index_usuario(request):
    return render(request, "turismo/usuarios/index.html", {})

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