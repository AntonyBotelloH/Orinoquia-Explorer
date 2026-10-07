from django import forms
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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'categoria' in self.fields:
            self.fields['categoria'].empty_label = "Seleccione una categoría..."

class ResenaForm(ModelForm):
    class Meta:
        model = Resena
        fields= '__all__'
        exclude = ['fecha_creacion']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Calificación de 1 a 5'}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe aquí la reseña o comentario...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'usuario' in self.fields:
            self.fields['usuario'].empty_label = "Seleccione un usuario..."
        if 'experiencia' in self.fields:
            self.fields['experiencia'].empty_label = "Seleccione una experiencia..."