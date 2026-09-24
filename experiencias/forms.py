from django.forms import ModelForm
from .models import Categoria, Resena, Experiencia

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields= '__all__'
        exclude = ['estado']
class ExperienciaForm(ModelForm):
    class Meta:
        model = Experiencia
        fields= '__all__'
        exclude = ['estado']

class ResenaForm(ModelForm):
    class Meta:
        model = Resena
        fields= '__all__'
        exclude = ['fecha_creacion']