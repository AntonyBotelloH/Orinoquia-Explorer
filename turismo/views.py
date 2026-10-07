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
from .models import Destino, CulturaGastronomia, MensajeContacto
from .forms import DestinoForm, CulturaGastronomiaForm, MensajeContactoForm
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .clima import consultar_pronostico_fecha
import json

def index_usuario(request):
    categoria_id = request.GET.get('categoria')
    q = request.GET.get('q', '').strip()

    # Experiencias activas subidas en la plataforma
    experiencias_qs = Experiencia.objects.filter(estado=True).select_related('categoria').prefetch_related('resena_set__usuario')

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


# ==================== VISTAS PÚBLICAS DE CARA AL USUARIO ====================

def destinos_usuario(request):
    """
    Vista pública para explorar todos los destinos turísticos de la Orinoquía,
    con filtro interactivo por departamento (Meta, Casanare, Arauca, Vichada, Guaviare)
    y buscador predictivo.
    """
    depto = request.GET.get('depto', '').strip().upper()
    q = request.GET.get('q', '').strip()

    destinos_qs = Destino.objects.filter(estado=True)

    if depto and depto in dict(Destino.DEPARTAMENTOS):
        destinos_qs = destinos_qs.filter(departamento=depto)

    if q:
        destinos_qs = destinos_qs.filter(
            Q(nombre__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(atractivos__icontains=q) |
            Q(como_llegar__icontains=q)
        )

    destinos = list(destinos_qs.order_by('-destacado', 'nombre'))

    # Conteo por departamento
    deptos_counts = {
        code: Destino.objects.filter(estado=True, departamento=code).count()
        for code, label in Destino.DEPARTAMENTOS
    }
    total_destinos = Destino.objects.filter(estado=True).count()

    context = {
        'titulo': 'Destinos | Explora la Orinoquía',
        'destinos': destinos,
        'departamentos': Destino.DEPARTAMENTOS,
        'deptos_counts': deptos_counts,
        'departamento_actual': depto,
        'total_destinos': total_destinos,
        'total_encontrados': len(destinos),
        'busqueda': q,
    }
    return render(request, "turismo/usuarios/destinos.html", context)


def cultura_usuario(request):
    """
    Vista pública para descubrir la Cultura y Tradición Llanera
    y la Gastronomía Típica, con filtros por categoría temática y buscador.
    """
    tipo = request.GET.get('tipo', '').strip().upper()
    q = request.GET.get('q', '').strip()

    cultura_qs = CulturaGastronomia.objects.filter(estado=True)

    if tipo in ('CULTURA', 'GASTRONOMIA'):
        cultura_qs = cultura_qs.filter(tipo=tipo)

    if q:
        cultura_qs = cultura_qs.filter(
            Q(titulo__icontains=q) |
            Q(subtitulo__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(origen_region__icontains=q)
        )

    articulos = list(cultura_qs.order_by('-destacado', '-id'))

    total_todos = CulturaGastronomia.objects.filter(estado=True).count()
    total_cultura = CulturaGastronomia.objects.filter(estado=True, tipo='CULTURA').count()
    total_gastronomia = CulturaGastronomia.objects.filter(estado=True, tipo='GASTRONOMIA').count()

    context = {
        'titulo': 'Cultura y Gastronomía | Orinoquía',
        'articulos': articulos,
        'tipo_actual': tipo,
        'total_todos': total_todos,
        'total_cultura': total_cultura,
        'total_gastronomia': total_gastronomia,
        'total_encontrados': len(articulos),
        'busqueda': q,
    }
    return render(request, "turismo/usuarios/cultura_gastronomia.html", context)


def contacto_usuario(request):
    """
    Vista pública para formulario de contacto directo e información de canales
    oficiales de atención, teléfonos y ubicaciones de Orinoquia Explorer.
    """
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            mensaje_obj = form.save()
            messages.success(
                request,
                f'¡Muchas gracias {mensaje_obj.nombre}! Tu mensaje ha sido recibido con éxito. '
                f'Nos pondremos en contacto contigo a la mayor brevedad.'
            )
            return redirect('contacto_usuario')
        else:
            messages.error(request, 'Por favor revisa la información ingresada en el formulario.')
    else:
        form = MensajeContactoForm()

    context = {
        'titulo': 'Contacto | Orinoquia Explorer',
        'form': form,
    }
    return render(request, "turismo/usuarios/contacto.html", context)


# ==================== DASHBOARD & CLIMA ====================

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

    # Destinos y cultura
    total_destinos = Destino.objects.count()
    destinos_activos = Destino.objects.filter(estado=True).count()
    total_cultura = CulturaGastronomia.objects.count()
    mensajes_pendientes = MensajeContacto.objects.filter(leido=False).count()

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
        'total_destinos': total_destinos,
        'destinos_activos': destinos_activos,
        'total_cultura': total_cultura,
        'mensajes_pendientes': mensajes_pendientes,
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


# ==================== ADMIN CRUD: DESTINOS ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_destino(request):
    destinos = Destino.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_destinos.html', {
        'destinos': destinos,
        'titulo': 'Destinos',
    })

@rol_requerido('ADMIN', 'GUIA')
def ver_destino(request, id):
    destino = get_object_or_404(Destino, id=id)
    destinos = Destino.objects.all().order_by('-id')
    detalles = [
        ('Nombre', destino.nombre),
        ('Departamento', destino.get_departamento_display()),
        ('Clima Promedio', destino.clima_promedio),
        ('Atractivos', destino.atractivos),
        ('Cómo Llegar', destino.como_llegar or 'No especificado'),
        ('Destacado en Portada', 'Sí' if destino.destacado else 'No'),
        ('Estado', 'Activo' if destino.estado else 'Inactivo'),
    ]
    return render(request, 'turismo/administracion/listar_destinos.html', {
        'destinos': destinos,
        'titulo': 'Destino',
        'objeto': destino,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('destino_listar'),
    })

@rol_requerido('ADMIN')
def crear_destino(request):
    form = DestinoForm()
    if request.method == 'POST':
        form = DestinoForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo = form.save()
            messages.success(request, f'Destino "{nuevo.nombre}" creado exitosamente.')
            return redirect('destino_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en '{campo}': {error}")

    destinos = Destino.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_destinos.html', {
        'destinos': destinos,
        'titulo': 'Destino',
        'form': form,
        'accion': 'C',
        'url_listar': reverse('destino_listar'),
    })

@rol_requerido('ADMIN')
def editar_destino(request, id):
    destino = get_object_or_404(Destino, id=id)
    form = DestinoForm(instance=destino)
    if request.method == 'POST':
        form = DestinoForm(request.POST, request.FILES, instance=destino)
        if form.is_valid():
            form.save()
            messages.success(request, f'Destino "{destino.nombre}" actualizado correctamente.')
            return redirect('destino_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en '{campo}': {error}")

    destinos = Destino.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_destinos.html', {
        'destinos': destinos,
        'titulo': 'Destino',
        'form': form,
        'objeto': destino,
        'accion': 'U',
        'url_listar': reverse('destino_listar'),
    })

@rol_requerido('ADMIN')
def eliminar_destino(request, id):
    objeto = get_object_or_404(Destino, id=id)
    if request.method == 'POST':
        objeto.estado = False
        objeto.save()
        messages.success(request, f'Destino "{objeto.nombre}" desactivado correctamente.')
        return redirect('destino_listar')

    destinos = Destino.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_destinos.html', {
        'destinos': destinos,
        'titulo': 'Destino',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('destino_listar'),
        'descripcion_eliminar': 'El destino pasará a estar inactivo y no se mostrará a los turistas en la plataforma.'
    })


# ==================== ADMIN CRUD: CULTURA Y GASTRONOMÍA ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_cultura(request):
    articulos = CulturaGastronomia.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_cultura.html', {
        'articulos': articulos,
        'titulo': 'Cultura y Gastronomía',
    })

@rol_requerido('ADMIN', 'GUIA')
def ver_cultura(request, id):
    item = get_object_or_404(CulturaGastronomia, id=id)
    articulos = CulturaGastronomia.objects.all().order_by('-id')
    detalles = [
        ('Título', item.titulo),
        ('Tipo', item.get_tipo_display()),
        ('Subtítulo', item.subtitulo or 'N/A'),
        ('Región / Origen', item.origen_region),
        ('Descripción', item.descripcion),
        ('Destacado', 'Sí' if item.destacado else 'No'),
        ('Estado', 'Activo' if item.estado else 'Inactivo'),
    ]
    return render(request, 'turismo/administracion/listar_cultura.html', {
        'articulos': articulos,
        'titulo': 'Cultura y Gastronomía',
        'objeto': item,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('cultura_listar'),
    })

@rol_requerido('ADMIN')
def crear_cultura(request):
    form = CulturaGastronomiaForm()
    if request.method == 'POST':
        form = CulturaGastronomiaForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo = form.save()
            messages.success(request, f'Publicación "{nuevo.titulo}" creada exitosamente.')
            return redirect('cultura_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en '{campo}': {error}")

    articulos = CulturaGastronomia.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_cultura.html', {
        'articulos': articulos,
        'titulo': 'Cultura y Gastronomía',
        'form': form,
        'accion': 'C',
        'url_listar': reverse('cultura_listar'),
    })

@rol_requerido('ADMIN')
def editar_cultura(request, id):
    item = get_object_or_404(CulturaGastronomia, id=id)
    form = CulturaGastronomiaForm(instance=item)
    if request.method == 'POST':
        form = CulturaGastronomiaForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Publicación "{item.titulo}" actualizada correctamente.')
            return redirect('cultura_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en '{campo}': {error}")

    articulos = CulturaGastronomia.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_cultura.html', {
        'articulos': articulos,
        'titulo': 'Cultura y Gastronomía',
        'form': form,
        'objeto': item,
        'accion': 'U',
        'url_listar': reverse('cultura_listar'),
    })

@rol_requerido('ADMIN')
def eliminar_cultura(request, id):
    objeto = get_object_or_404(CulturaGastronomia, id=id)
    if request.method == 'POST':
        objeto.estado = False
        objeto.save()
        messages.success(request, f'Publicación "{objeto.titulo}" desactivada correctamente.')
        return redirect('cultura_listar')

    articulos = CulturaGastronomia.objects.all().order_by('-id')
    return render(request, 'turismo/administracion/listar_cultura.html', {
        'articulos': articulos,
        'titulo': 'Cultura y Gastronomía',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('cultura_listar'),
        'descripcion_eliminar': 'La publicación pasará a estado inactivo y no se mostrará a los usuarios en la web.'
    })


# ==================== ADMIN CRUD: MENSAJES DE CONTACTO ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_contacto(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    return render(request, 'turismo/administracion/listar_contacto.html', {
        'mensajes': mensajes,
        'titulo': 'Mensajes de Contacto',
    })

@rol_requerido('ADMIN', 'GUIA')
def ver_contacto(request, id):
    msg = get_object_or_404(MensajeContacto, id=id)
    if not msg.leido:
        msg.leido = True
        msg.save()

    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    detalles = [
        ('Nombre', msg.nombre),
        ('Correo Electrónico', msg.email),
        ('Teléfono / WhatsApp', msg.telefono or 'No registrado'),
        ('Asunto', msg.asunto),
        ('Fecha de Envío', msg.fecha_envio.strftime('%d/%m/%Y %H:%M')),
        ('Mensaje', msg.mensaje),
    ]
    return render(request, 'turismo/administracion/listar_contacto.html', {
        'mensajes': mensajes,
        'titulo': 'Mensaje de Contacto',
        'objeto': msg,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('contacto_listar'),
    })

@rol_requerido('ADMIN')
def eliminar_contacto(request, id):
    objeto = get_object_or_404(MensajeContacto, id=id)
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, 'Mensaje de contacto eliminado permanentemente.')
        return redirect('contacto_listar')

    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    return render(request, 'turismo/administracion/listar_contacto.html', {
        'mensajes': mensajes,
        'titulo': 'Mensaje de Contacto',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('contacto_listar'),
        'descripcion_eliminar': f'Se eliminará el mensaje enviado por {objeto.nombre} ({objeto.email}).'
    })