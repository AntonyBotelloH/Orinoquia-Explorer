from django.forms import ModelForm
from .models import Categoria, Resena, Experiencia

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields= '__all__'
        exclude = ['estado']
class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields= '__all__'
        exclude = ['estado']

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields= '__all__'
        exclude = ['fecha_creacion']