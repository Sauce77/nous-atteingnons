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
        contexto = {
            "titulo": "Contacto no encontrado.",
            "descripcion": "El contacto seleccionado no pudo ser encontrado en los registros."
        }
        return render(request, "core/error.html", contexto)

    # obtenemos todas las secciones
    secciones = Seccion.objects.all()

    # logica post form
    if request.method == "POST":
        # obtenemos el boton submitInsertarRelacion
        submitInsertarRelacion = request.POST.get('submitInsertarRelacion')
        # si el valor es "Insertar"
        if submitInsertarRelacion == "Insertar":
            # obtenemos nombre del contacto
            nombre = request.POST.get('nombre')
            # obtenemos apellido paterno del contacto
            apellido_paterno = request.POST.get('apellido_paterno')
            # obtenemos apellido materno del contacto
            apellido_materno = request.POST.get('apellido_materno')
            # obtenemos email del contacto
            email = request.POST.get('email')
            # obtenemos telefono del contacto
            telefono = request.POST.get('telefono')
            # obtenemos domicilio del contacto
            domicilio = request.POST.get('domicilio')

            # obtenemos numero_seccion del contacto
            numero_seccion = request.POST.get('seccion')
            # obtenemos seccion del contacto
            try:
                seccion = Seccion.objects.get(numero=numero_seccion)
            except Seccion.DoesNotExist:
                contexto = {
                    "titulo": "La seccion elegida no fue encontrada.",
                    "descripcion": "No hay registro de la seccion elegida al insertar el contacto."
                }
                return render(request, "core/error.html", contexto)

            # filtramos contactos por seccion y apellido paterno (sin considerar mayusculas)
            contactos_repetidos = Contacto.objects.filter(seccion=seccion).filter(apellido_paterno__iexact=apellido_paterno)
            # filtramos contactos por nombre (sin considerar mayusculas) y apellido materno (sin considerar mayusculas)
            contactos_repetidos = contactos_repetidos.filter(nombre__iexact=nombre).filter(apellido_materno__iexact=apellido_materno)

            if contactos_repetidos:
                contexto = {
                    "titulo": "El contacto a insertar, ya existe.",
                    "descripcion": "Se ha encontrado un contacto que coincide en seccion, nombre y apellidos."
                }
                # si existen contactos repetidos redirigir
                return render(request, "core/error.html", contexto)
            
            else:
                # si no creamos un nuevo contacto
                nuevo_contacto = Contacto.objects.create(
                    nombre=nombre,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    email=email,
                    telefono=telefono,
                    domicilio=domicilio,
                    seccion=seccion
                )
                nuevo_contacto.save()

                # anadimos el nuevo contacto a las relaciones
                contacto.seguidores.add(nuevo_contacto)
            
    contexto = {
        "contacto": contacto,
        "secciones": secciones,
    }

    return render(request, "contactos/mostrarPerfilContacto.html", contexto)