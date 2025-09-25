from django.db import models
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Zonal(models.Model):
    """
        Identifica a un zonal en el distrito.
    """
    nombre = models.CharField(max_length=150, null=False, blank=False)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    """
        Identifica una seccion del distrito.
    """
    numero = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    rentabilidad = models.FloatField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    zonales = models.ManyToManyField(Zonal, null=True, blank=True)

    def __str__(self):
        return str(self.numero)
    

class Contacto(MPTTModel):
    """
        Identifica a una persona dentro de la red de contactos del sistema.
    """
    ESTATUS_CHOICES = {
        'A': 'Afiliado',
        'D': 'Desafiliado'
    }

    nombre = models.CharField(max_length=150, null=False, blank=False)
    apellido_paterno = models.CharField(max_length=150, null=False, blank=False)
    apellido_materno = models.CharField(max_length=150, null=False, blank=False)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    domicilio = models.TextField(null=True, blank=True)
    curp = models.CharField(max_length=18, blank=True, unique=True)
    clave_elector = models.CharField(max_length=13, blank=True, unique=True)
    estatus = models.CharField(max_length=1, choices=ESTATUS_CHOICES, default='A')
    
    seccion = models.ForeignKey(Seccion, on_delete=models.SET_NULL, null=True, blank=True)

    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['apellido_paterno']

    def save(self, *args, **kwargs):
        # en caso de no contar con seccion se asigna una por defecto
        
        # busca la categoria 'Sin Seccion' si la encuentra la retorna, sino la crea
        seccion_por_defecto, creada = Seccion.objects.get_or_create(
            numero=-1, defaults={"nombre": "Sin Seccion"})
        
        if not self.seccion:
            self.seccion = seccion_por_defecto

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombre}"
    
