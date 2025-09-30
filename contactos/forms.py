from django import forms
from django_select2 import forms as s2forms

from .models import Contacto


class ContactoAsociadoWidget(s2forms.ModelSelect2Widget):
    """
        Anade un buscador y select para el modelo Contacto.
    """
    search_fields = [
        "nombre__icontains",
        "apellido_paterno__icontains",
        "apellido_materno__icontains",
        "curp__icontains",
        "clave_elector__icontains",
        "telefono__icontains",
    ]

class SeccionWidget(s2forms.ModelSelect2Widget):
    """
        Anade un buscador y select para el modelo Seccion.
    """
    search_fields = [
        "numero__icontains",
        "nombre__icontains",
    ]


class ContactoForm(forms.ModelForm):
    """
        Renderiza el form del modelo contacto.
    """
    class Meta:
        model = Contacto
        exclude = ['estatus']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre(s)'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Apellido Materno'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Telefono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'E-mail'}),
            'domicilio': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'Domicilio'}),
            'curp': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'CURP'}),
            'clave_elector': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Clave Elector'}),
            'seccion': SeccionWidget(attrs={"class": "form-select", "data-placeholder": "Buscar seccion..."}),
            'parent': ContactoAsociadoWidget(attrs={"class": "form-select", 'data-allow-clear': 'false', "data-placeholder": "Buscar un contacto..."}),
        }


class ExcelForm(forms.Form):
    """
        Utilizado para mostrar un espacio e insertar
        un archivo Excel.
    """
    archivo = forms.FileField(
        label='Seleccione un archivo Excel...',
        help_text='Solo se permiten archivos con extension .xlsx, .xls'
    )