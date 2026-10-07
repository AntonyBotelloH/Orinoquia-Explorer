from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class UsuarioManager(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        documento = extra_fields.get('documento') or username
        if not username:
            username = documento
        if not extra_fields.get('documento'):
            extra_fields['documento'] = username
        return super().create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        documento = extra_fields.get('documento') or username
        if not username:
            username = documento
        if not extra_fields.get('documento'):
            extra_fields['documento'] = username
        extra_fields.setdefault('rol', 'ADMIN')
        return super().create_superuser(username=username, email=email, password=password, **extra_fields)

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
        ('PPT', 'Permiso de Permanencia Temporal'),
        ('NU', 'Otro')
    )
    first_name = models.CharField(max_length=50,blank=False,verbose_name="Nombre")
    last_name = models.CharField(max_length=50,blank=False,verbose_name="Apellido")
    tipo_documento = models.CharField(max_length=3,choices=TIPO_DOCUMENTO_CHOICES ,verbose_name="Tipo de Documento")
    documento = models.CharField(max_length=20,unique=True,verbose_name="Documento")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")

    objects = UsuarioManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "tipo_documento", "documento", "fecha_nacimiento"]

    def save(self, *args, **kwargs):
        if self.documento:
            self.username = str(self.documento)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.documento})"