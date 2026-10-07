from django import forms
from django.forms import ModelForm
from .models import Reserva, PolizaSeguro

class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'id': 'id_fecha_reserva'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].empty_label = "Seleccione un usuario..."
        self.fields['experiencia'].empty_label = "Seleccione una experiencia..."
        self.fields['poliza'].empty_label = "Sin póliza (Opcional)"

class PolizaSeguroForm(ModelForm):
    class Meta:
        model = PolizaSeguro
        fields = '__all__'
