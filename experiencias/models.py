from django.db import models

def renombrar_imagen(instance, filename):
    return f"experiencias/{instance.nombre}.{filename.split('.')[-1]}"

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
    duracion = models.IntegerField(verbose_name="Duracion")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    estado= models.BooleanField(default=True, verbose_name="Estado")
    
    def __str__(self):
        return self.nombre

class Resena(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, verbose_name="Experiencia")
    calificacion = models.IntegerField(verbose_name="Calificación")
    comentario = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
     