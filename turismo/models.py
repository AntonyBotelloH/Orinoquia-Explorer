import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models

def renombrar_destino(instance, filename):
    nombre_limpio = "".join(c for c in instance.nombre if c.isalnum() or c in (' ', '_', '-')).strip()
    nombre_limpio = nombre_limpio.replace(' ', '_') or "destino"
    return f"destinos/{nombre_limpio}.webp"

def renombrar_cultura(instance, filename):
    nombre_limpio = "".join(c for c in instance.titulo if c.isalnum() or c in (' ', '_', '-')).strip()
    nombre_limpio = nombre_limpio.replace(' ', '_') or "cultura"
    return f"cultura/{nombre_limpio}.webp"

class Destino(models.Model):
    DEPARTAMENTOS = (
        ('META', 'Meta'),
        ('CASANARE', 'Casanare'),
        ('ARAUCA', 'Arauca'),
        ('VICHADA', 'Vichada'),
        ('GUAVIARE', 'Guaviare'),
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Destino")
    departamento = models.CharField(max_length=20, choices=DEPARTAMENTOS, default='META', verbose_name="Departamento")
    descripcion = models.TextField(verbose_name="Descripción")
    imagen = models.ImageField(upload_to=renombrar_destino, verbose_name="Fotografía Principal")
    clima_promedio = models.CharField(max_length=100, default="28°C - Tropical Cálido", verbose_name="Clima Promedio")
    atractivos = models.TextField(verbose_name="Atractivos Principales", help_text="Separados por comas o viñetas")
    como_llegar = models.TextField(blank=True, null=True, verbose_name="Cómo Llegar")
    destacado = models.BooleanField(default=False, verbose_name="Destacado en Portada")
    estado = models.BooleanField(default=True, verbose_name="Estado Activo")

    def save(self, *args, **kwargs):
        if self.imagen:
            try:
                self.imagen.seek(0)
                with Image.open(self.imagen) as img:
                    if img.format != 'WEBP' or not self.imagen.name.lower().endswith('.webp'):
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            img_conv = img.convert('RGBA')
                        else:
                            img_conv = img.convert('RGB')
                        buf = BytesIO()
                        img_conv.save(buf, format='WEBP', quality=85, optimize=True)
                        buf.seek(0)
                        base = os.path.splitext(os.path.basename(self.imagen.name))[0]
                        self.imagen.save(f"{base}.webp", ContentFile(buf.read()), save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.get_departamento_display()})"


class CulturaGastronomia(models.Model):
    TIPO_CHOICES = (
        ('CULTURA', 'Cultura y Tradición Llanera'),
        ('GASTRONOMIA', 'Gastronomía Típica'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='CULTURA', verbose_name="Tipo de Publicación")
    titulo = models.CharField(max_length=150, verbose_name="Título")
    subtitulo = models.CharField(max_length=250, blank=True, null=True, verbose_name="Subtítulo o Resumen Corto")
    descripcion = models.TextField(verbose_name="Descripción Detallada")
    imagen = models.ImageField(upload_to=renombrar_cultura, verbose_name="Fotografía")
    origen_region = models.CharField(max_length=100, default="Llanos Orientales", verbose_name="Región u Origen")
    destacado = models.BooleanField(default=False, verbose_name="Destacado")
    estado = models.BooleanField(default=True, verbose_name="Estado Activo")

    def save(self, *args, **kwargs):
        if self.imagen:
            try:
                self.imagen.seek(0)
                with Image.open(self.imagen) as img:
                    if img.format != 'WEBP' or not self.imagen.name.lower().endswith('.webp'):
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            img_conv = img.convert('RGBA')
                        else:
                            img_conv = img.convert('RGB')
                        buf = BytesIO()
                        img_conv.save(buf, format='WEBP', quality=85, optimize=True)
                        buf.seek(0)
                        base = os.path.splitext(os.path.basename(self.imagen.name))[0]
                        self.imagen.save(f"{base}.webp", ContentFile(buf.read()), save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=120, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=25, blank=True, null=True, verbose_name="Teléfono o WhatsApp")
    asunto = models.CharField(max_length=200, verbose_name="Asunto")
    mensaje = models.TextField(verbose_name="Mensaje o Consulta")
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Envío")
    leido = models.BooleanField(default=False, verbose_name="Marcado como Leído")

    def __str__(self):
        return f"{self.nombre} - {self.asunto} ({self.fecha_envio.strftime('%d/%m/%Y')})"
