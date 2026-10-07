from django import forms
from .models import Destino, CulturaGastronomia, MensajeContacto

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Cañón del Río Güejar'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del destino, paisajes y geografía...'}),
            'clima_promedio': forms.TextInput(attrs={'placeholder': 'Ej: 27°C - Clima tropical húmedo'}),
            'atractivos': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Cascadas, formaciones rocosas, navegación...'}),
            'como_llegar': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Rutas terrestres, vías de acceso o transportes recomendados...'}),
        }

class CulturaGastronomiaForm(forms.ModelForm):
    class Meta:
        model = CulturaGastronomia
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ej: Ternera a la Llanera (Mamona)'}),
            'subtitulo': forms.TextInput(attrs={'placeholder': 'Ej: Plato insignia asado a fuego lento en chuzos de madera'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Historia, preparación tradicional o valor cultural...'}),
            'origen_region': forms.TextInput(attrs={'placeholder': 'Ej: Meta, Casanare y sabanas del Llano'}),
        }

class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'telefono', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre y apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+57 310 123 4567'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Consulta sobre expedición o safaris'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntanos qué experiencia buscas o qué dudas tienes...'}),
        }
