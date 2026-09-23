from django.shortcuts import render,redirect
from .models import Categoria, Experiencia, Resena
from .forms import CategoriaForm, ExperienciaForm
# Create your views here.
def listar_categoria(request):
    categorias= Categoria.objects.all()
    titulo='Categorias'
    context={'categorias':categorias}
    return render(request, 'categorias/listar_categorias.html', context)
def crear_categoria(request):
    titulo='Categoria'
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_listar')
    context={
        'titulo':titulo,
        'form':form
    }   
    return render(request, 'partials/base-creacion.html', context)
def listar_experiencia(request):
    experiencias = Experiencia.objects.all()
    context={'experiencias':experiencias}
    return render(request, 'experiencias/listar_experiencias.html', context)
def crear_experiencia(request):
    titulo='Experiencia'
    form = ExperienciaForm()
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('experiencia_listar')
    context={
        'titulo':titulo,
        'form':form
    }   
    return render(request, 'partials/base-creacion.html', context)

def listar_resena(request):
    return render(request, 'experiencias/listar_resena.html')