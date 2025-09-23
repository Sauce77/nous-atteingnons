from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Zonal, Seccion, Contacto
# Register your models here.
admin.site.register(Zonal)
admin.site.register(Seccion)
admin.site.register(Contacto, MPTTModelAdmin)