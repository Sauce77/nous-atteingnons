from django.shortcuts import render


from .models import Contacto, Seccion
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


def mostrarPerfilContacto(request, id_contacto):

    try:
        # obtenemos objeto del usuario seleccionado
        contacto = Contacto.objects.get(pk=id_contacto)
    except Contacto.DoesNotExist:
        return render(request, "core/error.html")

    # obtenemos todas las secciones
    secciones = Seccion.objects.all()
    
    contexto = {
        "contacto": contacto,
        "secciones": secciones,
    }

    return render(request, "contactos/mostrarPerfilContacto.html", contexto)