from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Zonal(models.Model):
    """
        Identifica a un zonal en el distrito.
    """
    nombre = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    """
        Identifica una seccion del distrito.
    """
    numero = models.IntegerField(null=False, blank=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    rentabilidad = models.FloatField(null=False, blank=False)

    zonales = models.ManyToManyField(Zonal)

    def __str__(self):
        return str(self.numero)
    

class Contacto(models.Model):
    """
        Identifica a una persona dentro de la red de contactos del sistema.
    """
    nombre = models.CharField(max_length=150, null=False, blank=False)
    apellido_paterno = models.CharField(max_length=150, null=False, blank=False)
    apellido_materno = models.CharField(max_length=150, null=False, blank=False)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    domicilio = models.TextField(null=True, blank=True)
    
    seccion = models.ForeignKey(Seccion, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_matero} {self.nombre}"
    
class Relacion(models.Model):
    """
        Muestra una relacion en la red de contactos.
        Verifica que las relaciones sean unicas y unidireccionales.
    """

    TIPOS_RELACION = {
        ("follow", "FOLLOW"),
        ("block", "BLOCK")
    }

    contacto_master = models.ForeignKey(Contacto, related_name='inicio_relacion',on_delete=models.SET_NULL, null=True)
    contacto_detail = models.ForeignKey(Contacto, related_name='recibio_relacion',on_delete=models.SET_NULL, null=True)

    ultima_modificacion = models.DateField(auto_now=True)
    tipo_relacion = models.CharField(max_length=15, choices=TIPOS_RELACION)
    descripcion = models.TextField(null=True, blank=True)

    def clean(self):
        # valida si se ingresaron dos usuarios al crear o modificar una relacion
        if self.contacto_master == None or self.contacto_detail == None:
            raise ValidationError("Relation must be created with two contacts.")

    def __str__(self):
        return str(self.ultima_modificacion)