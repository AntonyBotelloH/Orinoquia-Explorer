from django.db import models

def renombrar_imagen(instance, filename):
    return f"experiencias/{instance.nombre}.{filename.split('.')[-1]}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripcion")
    def __str__(self):
        return self.nombre
    
# Create your models here.
class Experiencia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripcion")
    imagen = models.ImageField(upload_to=renombrar_imagen, verbose_name="Imagen")
    precio = models.FloatField(verbose_name="Precio")
    duracion = models.IntegerField(verbose_name="Duracion")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    def __str__(self):
        return self.nombre
    
    