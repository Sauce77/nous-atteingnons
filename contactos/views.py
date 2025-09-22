from django.shortcuts import render


from .models import Contacto
# Create your views here.

def mostrarContactos(request):
    """
        Despliega los contactos disponibles para un contacto en especifico.
    """
    
    # obtenemos contactos
    contactos = Contacto.objects.all()

    contexto = {
        "contactos": contactos,
    }

    return render(request, "contactos/mostrarContactos.html", contexto)