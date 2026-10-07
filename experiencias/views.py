from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Categoria, Experiencia, Resena
from .forms import CategoriaForm, ExperienciaForm, ResenaForm
from django.contrib import messages
from usuarios.decorators import rol_requerido

# Create your views here.

# ==================== CATEGORÍAS ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_categoria(request):
    categorias = Categoria.objects.all()
    titulo = 'Categorías'
    context = {
        'categorias': categorias,
        'titulo': titulo,
    }
    return render(request, 'categorias/listar_categorias.html', context)

@rol_requerido('ADMIN', 'GUIA')
def ver_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categorias = Categoria.objects.all()
    detalles = [
        ('Nombre', categoria.nombre),
        ('Descripción', categoria.descripcion),
        ('Estado', 'Activo' if categoria.estado else 'Inactivo'),
    ]
    context = {
        'categorias': categorias,
        'titulo': 'Categoría',
        'objeto': categoria,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('categoria_listar'),
    }
    return render(request, 'categorias/listar_categorias.html', context)

@rol_requerido('ADMIN')
def crear_categoria(request):
    titulo = 'Categoría'
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría "{request.POST.get("nombre")}" creada correctamente.')
            return redirect('categoria_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")
    
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias,
        'titulo': titulo,
        'form': form,
        'accion': 'C',
        'url_listar': reverse('categoria_listar'),
    }   
    return render(request, 'categorias/listar_categorias.html', context)

@rol_requerido('ADMIN')
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    titulo = 'Categoría'
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('categoria_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")

    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias,
        'titulo': titulo,
        'form': form,
        'objeto': categoria,
        'accion': 'U',
        'url_listar': reverse('categoria_listar'),
    }   
    return render(request, 'categorias/listar_categorias.html', context)

@rol_requerido('ADMIN')
def eliminar_categoria(request, id):
    objeto = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        objeto.estado = False
        objeto.save()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('categoria_listar')
        
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias,
        'titulo': 'Categoría',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('categoria_listar'),
    }
    return render(request, 'categorias/listar_categorias.html', context)


# ==================== EXPERIENCIAS ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_experiencia(request):
    experiencias = Experiencia.objects.all()
    titulo = 'Experiencias'
    context = {
        'experiencias': experiencias,
        'titulo': titulo,
    }
    return render(request, 'experiencias/listar_experiencias.html', context)

@rol_requerido('ADMIN', 'GUIA')
def ver_experiencia(request, id):
    experiencia = get_object_or_404(Experiencia, id=id)
    experiencias = Experiencia.objects.all()
    detalles = [
        ('Nombre', experiencia.nombre),
        ('Descripción', experiencia.descripcion),
        ('Precio', f"${experiencia.precio:,}"),
        ('Duración', experiencia.duracion),
        ('Categoría', experiencia.categoria.nombre if experiencia.categoria else 'Sin Categoría'),
        ('Estado', 'Activo' if experiencia.estado else 'Inactivo'),
    ]
    context = {
        'experiencias': experiencias,
        'titulo': 'Experiencia',
        'objeto': experiencia,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('experiencia_listar'),
    }
    return render(request, 'experiencias/listar_experiencias.html', context)

@rol_requerido('ADMIN')
def crear_experiencia(request):
    titulo = 'Experiencia'
    form = ExperienciaForm()
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia creada correctamente.')
            return redirect('experiencia_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")
    
    experiencias = Experiencia.objects.all()
    context = {
        'experiencias': experiencias,
        'titulo': titulo,
        'form': form,
        'accion': 'C',
        'url_listar': reverse('experiencia_listar'),
    }   
    return render(request, 'experiencias/listar_experiencias.html', context)

@rol_requerido('ADMIN')
def editar_experiencia(request, id):
    experiencia = get_object_or_404(Experiencia, id=id)
    titulo = 'Experiencia'
    form = ExperienciaForm(instance=experiencia)
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia actualizada correctamente.')
            return redirect('experiencia_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")

    experiencias = Experiencia.objects.all()
    context = {
        'experiencias': experiencias,
        'titulo': titulo,
        'form': form,
        'objeto': experiencia,
        'accion': 'U',
        'url_listar': reverse('experiencia_listar'),
    }   
    return render(request, 'experiencias/listar_experiencias.html', context)

@rol_requerido('ADMIN')
def eliminar_experiencia(request, id):
    objeto = get_object_or_404(Experiencia, id=id)
    if request.method == 'POST':
        objeto.estado = False
        objeto.save()
        messages.success(request, 'Experiencia eliminada correctamente.')
        return redirect('experiencia_listar')

    experiencias = Experiencia.objects.all()
    context = {
        'experiencias': experiencias,
        'titulo': 'Experiencia',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('experiencia_listar'),
    }
    return render(request, 'experiencias/listar_experiencias.html', context)


# ==================== RESEÑAS ====================

@rol_requerido('ADMIN', 'GUIA')
def listar_resena(request):
    resenas = Resena.objects.select_related('usuario', 'experiencia').all()
    context = {
        'titulo': 'Gestión de Reseñas',
        'resenas': resenas,
    }
    return render(request, 'experiencias/listar_resena.html', context)

@rol_requerido('ADMIN', 'GUIA')
def ver_resena(request, id):
    resena = get_object_or_404(Resena.objects.select_related('usuario', 'experiencia'), id=id)
    resenas = Resena.objects.select_related('usuario', 'experiencia').all()
    detalles = [
        ('Usuario', f"{resena.usuario.get_full_name() or resena.usuario.username} ({resena.usuario.email})"),
        ('Experiencia', resena.experiencia.nombre if resena.experiencia else 'Sin experiencia'),
        ('Calificación', f"{resena.calificacion} / 5 ⭐"),
        ('Comentario', resena.comentario),
        ('Fecha de Creación', resena.fecha_creacion.strftime('%d/%m/%Y %H:%M')),
    ]
    context = {
        'resenas': resenas,
        'titulo': 'Reseña',
        'objeto': resena,
        'detalles': detalles,
        'accion': 'R',
        'url_listar': reverse('resena_listar'),
    }
    return render(request, 'experiencias/listar_resena.html', context)

@rol_requerido('ADMIN')
def crear_resena(request):
    titulo = 'Reseña'
    form = ResenaForm()
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña creada correctamente.')
            return redirect('resena_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")

    resenas = Resena.objects.select_related('usuario', 'experiencia').all()
    context = {
        'resenas': resenas,
        'titulo': titulo,
        'form': form,
        'accion': 'C',
        'url_listar': reverse('resena_listar'),
    }
    return render(request, 'experiencias/listar_resena.html', context)

@rol_requerido('ADMIN')
def editar_resena(request, id):
    resena = get_object_or_404(Resena, id=id)
    titulo = 'Reseña'
    form = ResenaForm(instance=resena)
    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña actualizada correctamente.')
            return redirect('resena_listar')
        else:
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f"Error en el campo '{campo.capitalize()}': {error}")

    resenas = Resena.objects.select_related('usuario', 'experiencia').all()
    context = {
        'resenas': resenas,
        'titulo': titulo,
        'form': form,
        'objeto': resena,
        'accion': 'U',
        'url_listar': reverse('resena_listar'),
    }
    return render(request, 'experiencias/listar_resena.html', context)

@rol_requerido('ADMIN')
def eliminar_resena(request, id):
    objeto = get_object_or_404(Resena, id=id)
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, 'Reseña eliminada correctamente.')
        return redirect('resena_listar')

    resenas = Resena.objects.select_related('usuario', 'experiencia').all()
    context = {
        'resenas': resenas,
        'titulo': 'Reseña',
        'objeto': objeto,
        'accion': 'D',
        'url_listar': reverse('resena_listar'),
    }
    return render(request, 'experiencias/listar_resena.html', context)