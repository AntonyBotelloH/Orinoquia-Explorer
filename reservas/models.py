from django.db import models
from django.conf import settings
from experiencias.models import Experiencia

class PolizaSeguro(models.Model):
    proveedor = models.CharField(max_length=100, verbose_name="Proveedor")
    numero_poliza = models.CharField(max_length=50, verbose_name="Número de Póliza")
    fecha_expiracion = models.DateField(verbose_name="Fecha de Expiración")

    def __str__(self):
        return f"{self.proveedor} - {self.numero_poliza}"
        
class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas', verbose_name="Usuario")
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name='reservas', verbose_name="Experiencia")
    fecha = models.DateField(verbose_name="Fecha de Reserva")
    numero_personas = models.PositiveIntegerField(verbose_name="Número de Personas")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Total")
    estado = models.CharField(max_length=20, choices=ESTADOS_RESERVA, default='PENDIENTE', verbose_name="Estado")
    peticiones_especiales = models.TextField(blank=True, null=True, verbose_name="Peticiones Especiales")
    poliza = models.ForeignKey(PolizaSeguro, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas', verbose_name="Póliza de Seguro")

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.username if self.usuario else ''} - {self.experiencia.nombre}"