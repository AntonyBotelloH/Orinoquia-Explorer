import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from usuarios.models import Usuario

def renombrar_imagen(instance, filename):
    nombre_limpio = "".join(c for c in instance.nombre if c.isalnum() or c in (' ', '_', '-')).strip()
    nombre_limpio = nombre_limpio.replace(' ', '_')
    if not nombre_limpio:
        nombre_limpio = "experiencia"
    return f"experiencias/{nombre_limpio}.webp"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripcion")
    estado= models.BooleanField(default=True, verbose_name="Estado")
    def __str__(self):
        return self.nombre
    
# Create your models here.
class Experiencia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripcion")
    imagen = models.ImageField(upload_to=renombrar_imagen, verbose_name="Imagen")
    precio = models.FloatField(verbose_name="Precio")
    duracion = models.IntegerField(verbose_name="Duración")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    estado= models.BooleanField(default=True, verbose_name="Estado")

    def save(self, *args, **kwargs):
        if self.imagen:
            try:
                self.imagen.seek(0)
                with Image.open(self.imagen) as img:
                    necesita_conversion = (img.format != 'WEBP' or not self.imagen.name.lower().endswith('.webp'))
                    if necesita_conversion:
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            img_converted = img.convert('RGBA')
                        else:
                            img_converted = img.convert('RGB')
                        
                        buffer = BytesIO()
                        img_converted.save(buffer, format='WEBP', quality=85, optimize=True)
                        buffer.seek(0)

                        base_name = os.path.splitext(os.path.basename(self.imagen.name))[0]
                        nombre_webp = f"{base_name}.webp"
                        self.imagen.save(nombre_webp, ContentFile(buffer.read()), save=False)
            except Exception:
                pass

        super().save(*args, **kwargs)

    @property
    def promedio_calificacion(self):
        res = list(self.resena_set.all())
        if not res:
            return None
        return round(sum(r.calificacion for r in res) / len(res), 1)

    @property
    def total_resenas(self):
        return self.resena_set.count()

    def __str__(self):
        return self.nombre

class Resena(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, verbose_name="Experiencia")
    calificacion = models.IntegerField(verbose_name="Calificación")
    comentario = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
     