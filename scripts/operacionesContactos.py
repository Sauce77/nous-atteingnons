from django.shortcuts import get_object_or_404


from contactos.models import Contacto

def borrarContacto(id_contacto):
    """
        El usuario seleccionado es retirado de la base de datos,
        solo es posible para contactos sin relaciones.

        Retorna true al borrar el contacto.
    """

    contacto = get_object_or_404(Contacto, pk=id_contacto)

    numero_relaciones = contacto.get_descendant_count()

    if numero_relaciones <= 0:
        # si el contacto no tiene relaciones
        # eliminamos el contacto
        contacto.delete()
        return True
    
    return False