from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Experiencia, Resena
from .forms import CategoriaForm, ExperienciaForm
from django.contrib import messages
from usuarios.decorators import rol_requerido
# Create your views here.

@rol_requerido('ADMIN', 'GUIA')
def listar_categoria(request):
    categorias = Categoria.objects.all()
    titulo = 'Categorías'
    context = {
        'categorias': categorias,
        'titulo': titulo
    }
    return render(request, 'categorias/listar_categorias.html', context)

@rol_requerido('ADMIN')
def crear_categoria(request):
    accion = 'Crear'
    titulo = 'Categoría'
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría {request.POST.get("nombre")} creada correctamente.')
            return redirect('categoria_listar')
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
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    accion = 'Editar'
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

    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }   
    return render(request, 'partials/base-creacion.html', context)

@rol_requerido('ADMIN')
def eliminar_categoria(request, id):
    objeto = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        objeto.estado = False
        objeto.save()
        messages.success(request, 'Categoría eliminada correctamente.')
        
    return redirect('categoria_listar')


@rol_requerido('ADMIN', 'GUIA')
def listar_experiencia(request):
    experiencias = Experiencia.objects.all()
    context = {'experiencias': experiencias}
    return render(request, 'experiencias/listar_experiencias.html', context)

@rol_requerido('ADMIN')
def crear_experiencia(request):
    accion = 'Crear'
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
    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }   
    return render(request, 'partials/base-creacion.html', context)


@rol_requerido('ADMIN', 'GUIA')
def listar_resena(request):
    return render(request, 'experiencias/listar_resena.html')