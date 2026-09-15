from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    ROL_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('GUIA', 'Guia'),
        ('TURISTA', 'Turista'),
    )
    rol = models.CharField(max_length=10,choices=ROL_CHOICES,default='TURISTA',verbose_name="Rol")
    TIPO_DOCUMENTO_CHOICES = (
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('PPT', 'Permiso de Permanecia Temporal'),
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('NU', 'Otro')
    )
    first_name = models.CharField(max_length=50,blank=False,verbose_name="Nombre")
    last_name = models.CharField(max_length=50,blank=False,verbose_name="Apellido")
    tipo_documento = models.CharField(max_length=3,choices=TIPO_DOCUMENTO_CHOICES ,verbose_name="Tipo de Documento")
    documento = models.CharField(max_length=20,unique=True,verbose_name="Documento")
    fecha_nacimiento = models.DateField(blank=True, verbose_name="Fecha de Nacimiento")
    REQUIRED_FIELDS = ["first_name", "last_name", "tipo_documento", "documento", "fecha_nacimiento"]
    