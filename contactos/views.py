from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import Contacto, Seccion
from .forms import ContactoForm
# Create your views here.

def mostrarContactos(request):
    """
        Despliega los contactos disponibles para un contacto en especifico.
    """
    
    # obtenemos contactos
    contactos = Contacto.objects.all()

    contexto = {
        "titulo": "Contactos",
        "contactos": contactos,
    }

    return render(request, "contactos/mostrarContactos.html", contexto)

def editarContacto(request, id_contacto):
    """
        Permite modificar la informacion y la relacion de un contacto seleccionado.
    """
    try:
        # obtenemos contacto
        contacto = Contacto.objects.get(pk=id_contacto)
    except Contacto.DoesNotExist:
        contexto = {
            "titulo": "Contacto no pudo ser encontrado.",
            "descripcion": "El contacto no se encuentra registrado."
        }
        return render(request, "core/error.html", contacto)
    
    # logica post form
    if request.method == "POST":
        # obtenemos boton submitGuardar
        submitGuardar = request.POST.get('submitGuardar')

        # si el valor de submitGuardar es 'Guardar'
        if submitGuardar == "Guardar":
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
            # obtenemos telefono del contacto
            curp = request.POST.get('curp')
            # obtenemos telefono del contacto
            clave_elector = request.POST.get('clave_elector')
            # obtenemos domicilio del contacto
            domicilio = request.POST.get('domicilio')

            # obtenemos numero_seccion del contacto
            numero_seccion = request.POST.get('seccion')
            # obtenemos id del contacto asociado
            numero_contacto_asociado = request.POST.get('padre')

            # revisamos que numero de seccion sea un numero
            try:
                numero_seccion = int(numero_seccion)
            except ValueError:
                numero_seccion = -1

            # convertimos CURP a mayusculas
            curp = curp.upper()

            # convertimos clave de elector a mayusculas
            clave_elector = clave_elector.upper()

            # obtenemos seccion del contacto
            try:
                seccion = Seccion.objects.get(numero=numero_seccion)
            except Seccion.DoesNotExist:
                contexto = {
                    "titulo": "La seccion elegida no fue encontrada.",
                    "descripcion": "No hay registro de la seccion elegida al modificar el contacto."
                }
                return render(request, "core/error.html", contexto)
            
            # al principio no hay un contacto asociado
            contacto_asociado = None
            
            # si el hay numero de contacto asociado
            if numero_contacto_asociado:

                # obtenemos contacto asociado del contacto
                try:
                    contacto_asociado = Contacto.objects.get(pk=numero_contacto_asociado)
                except Contacto.DoesNotExist:
                    contexto = {
                        "titulo": "Contacto asociado no encontrado.",
                        "descripcion": "No hay registro del contacto asociado elegido al editar la relacion del contacto."
                    }
                    return render(request, "core/error.html", contexto)

            # filtramos contactos por seccion y apellido paterno (sin considerar mayusculas)
            contactos_repetidos = Contacto.objects.filter(seccion=seccion).filter(apellido_paterno__iexact=apellido_paterno)
            # filtramos contactos por nombre (sin considerar mayusculas) y apellido materno (sin considerar mayusculas)
            contactos_repetidos = contactos_repetidos.filter(nombre__iexact=nombre).filter(apellido_materno__iexact=apellido_materno)
            # excluimos el contacto a editar
            contactos_repetidos = contactos_repetidos.exclude(pk=contacto.id)

            if contactos_repetidos:
                contexto = {
                    "titulo": "El contacto a insertar, ya existe.",
                    "descripcion": "Se ha encontrado un contacto que coincide en seccion, nombre y apellidos."
                }
                # si existen contactos repetidos redirigir
                return render(request, "core/error.html", contexto)
            
            else:
                # si no actualizamos los valores actuales
                contacto.nombre=nombre
                contacto.apellido_paterno=apellido_paterno
                contacto.apellido_materno=apellido_materno
                contacto.email=email
                contacto.telefono=telefono
                contacto.curp = curp
                contacto.clave_elector = clave_elector
                contacto.domicilio=domicilio
                contacto.seccion=seccion
                contacto.parent=contacto_asociado

                contacto.save()

                return redirect('contactos:mostrarPerfilContacto', id_contacto=contacto.id)
    
    else:
        form = ContactoForm()

    # obtenemos secciones
    secciones = Seccion.objects.all()

    # obtenemos contactos
    contactos = Contacto.objects.all()

    contexto = {
        "contacto": contacto,
        "secciones": secciones,
        "contactos": contactos,
        "form": form,
    }

    return render(request, "contactos/editarContacto.html", contexto)

def mostrarPerfilContacto(request, id_contacto):
    """
        Muestra la informacion de contacto y sus relaciones.
    """

    try:
        # obtenemos objeto del usuario seleccionado
        contacto = Contacto.objects.get(pk=id_contacto)
    except Contacto.DoesNotExist:
        contexto = {
            "titulo": "Contacto no encontrado.",
            "descripcion": "El contacto seleccionado no pudo ser encontrado en los registros."
        }
        return render(request, "core/error.html", contexto)
    
    # obtenemos url para serializador del arbol
    api_url = reverse('api:mostrarRelaciones', args=[contacto.pk])

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
            # obtenemos telefono del contacto
            curp = request.POST.get('curp')
            # obtenemos telefono del contacto
            clave_elector = request.POST.get('clave_elector')
            # obtenemos domicilio del contacto
            domicilio = request.POST.get('domicilio')

            # obtenemos numero_seccion del contacto
            numero_seccion = request.POST.get('seccion')

            # revisamos que numero de seccion sea un numero
            try:
                numero_seccion = int(numero_seccion)
            except ValueError:
                numero_seccion = -1

            # convertimos CURP a mayusculas
            curp = curp.upper()

            # convertimos clave de elector a mayusculas
            clave_elector = clave_elector.upper()
            
            # obtenemos seccion del contacto
            try:
                seccion = Seccion.objects.get(numero=numero_seccion)
            except Seccion.DoesNotExist:
                contexto = {
                    "titulo": "La seccion elegida no fue encontrada.",
                    "descripcion": "No hay registro de la seccion elegida al insertar el contacto."
                }
                return render(request, "core/error.html", contexto)

            # filtramos contactos apellido paterno (sin considerar mayusculas)
            contactos_repetidos = Contacto.objects.filter(apellido_paterno__iexact=apellido_paterno)
            # filtramos contactos por nombre (sin considerar mayusculas) y apellido materno (sin considerar mayusculas)
            contactos_repetidos = contactos_repetidos.filter(nombre__iexact=nombre).filter(apellido_materno__iexact=apellido_materno)
            # filtramos por telefono
            if telefono:
                # si el form incluye telefono
                contactos_repetidos = contactos_repetidos.filter(telefono__iexact=telefono)

            # filtramos por curp y clave de elector
            if curp:
                # si el form incluye curp
                contactos_repetidos = contactos_repetidos.filter(curp__iexact=curp)

            if curp:
                # si el form incluye clave de elector
                contactos_repetidos = contactos_repetidos.filter(clave_elector__iexact=clave_elector)
            
            if contactos_repetidos.exists():
                contexto = {
                    "titulo": "Contactos identicos",
                    "contactos": contactos_repetidos
                }

                messages.warning(request, "Se encontraron contactos con concidencias en la informacion ingresada.")
                # si existen contactos repetidos redirigir
                return render(request, "contactos/mostrarContactos.html", contexto)
            
            else:

                try:
                    # si no creamos un nuevo contacto
                    nuevo_contacto = Contacto.objects.create(
                        nombre=nombre,
                        apellido_paterno=apellido_paterno,
                        apellido_materno=apellido_materno,
                        email=email,
                        telefono=telefono,
                        curp=curp,
                        clave_elector=clave_elector,
                        domicilio=domicilio,
                        seccion=seccion,
                        parent=contacto
                    )
                    nuevo_contacto.save()
                except Exception as e:
                    contexto = {
                        "titulo": "Error al insertar nuevo contacto.",
                        "descripcion": e
                    }
                    # si existe error al crear un contacto
                    return render(request, "core/error.html", contexto)
    else:
        form = ContactoForm()

    contexto = {
        "contacto": contacto,
        "secciones": secciones,
        "form": form,
        "api_url": api_url
    }

    return render(request, "contactos/mostrarPerfilContacto.html", contexto)

