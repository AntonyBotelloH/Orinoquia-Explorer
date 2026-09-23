from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Experiencia, Resena
from .forms import CategoriaForm, ExperienciaForm

# Create your views here.
def listar_categoria(request):
    categorias = Categoria.objects.all()
    titulo = 'Categorías'
    context = {
        'categorias': categorias,
        'titulo': titulo
    }
    return render(request, 'categorias/listar_categorias.html', context)

def crear_categoria(request):
    accion = 'Crear'
    titulo = 'Categoría'
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_listar')
        else:
            print(form.errors)
    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }   
    return render(request, 'partials/base-creacion.html', context)

def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    accion = 'Editar'
    titulo = 'Categoría'
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categoria_listar')
        else:
            print(form.errors)
    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }   
    return render(request, 'partials/base-creacion.html', context)

def eliminar_categoria(request, id):
    objeto = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        objeto.estado = False
        objeto.save()
        
    return redirect('categoria_listar')


def listar_experiencia(request):
    experiencias = Experiencia.objects.all()
    context = {'experiencias': experiencias}
    return render(request, 'experiencias/listar_experiencias.html', context)

def crear_experiencia(request):
    accion = 'Crear'
    titulo = 'Experiencia'
    form = ExperienciaForm()
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('experiencia_listar')
    context = {
        'titulo': titulo,
        'form': form,
        'accion': accion,
    }   
    return render(request, 'partials/base-creacion.html', context)


def listar_resena(request):
    return render(request, 'experiencias/listar_resena.html')