from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    """
        Renderiza el form del modelo contacto.
    """
    class Meta:
        model = Contacto
        exclude = ['fecha_nacimiento', 'estatus', 'seccion', 'parent']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre(s)'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Apellido Materno'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Telefono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'E-mail'}),
            'domicilio': forms.Textarea(attrs={'class': 'form-control mb-2', 'placeholder': 'Domicilio'}),
            'curp': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'CURP'}),
            'clave_elector': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Clave Elector'}),
        }