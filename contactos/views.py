from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib import messages

from scripts.validacionesContactos import existenCoincidencias, filtrarContactosDuplicados

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

    # obtenemos el contacto
    contacto = get_object_or_404(Contacto, pk=id_contacto)

    # obtenemos secciones
    secciones = Seccion.objects.all()

    # obtenemos contactos
    contactos = Contacto.objects.all()
    
    # logica post form
    if request.method == "POST":
        # obtenemos boton submitGuardar
        submitGuardar = request.POST.get('submitGuardar')

        # si el valor de submitGuardar es 'Guardar'
        if submitGuardar == "Guardar":
            
            # obtenemos respuestas de la peticion POST
            form = ContactoForm(request.POST, instance=contacto)

            if form.is_valid():
                # si la informacion insertada es valida
                # alamacenamos las respuestas en una instancia temporal
                contacto = form.save(commit=False)

                if contacto.curp:
                    # convertimos CURP a mayusculas
                    contacto.curp = contacto.curp.upper()

                if contacto.clave_elector:
                    # convertimos clave de elector a mayusculas
                    contacto.clave_elector = contacto.clave_elector.upper()

                
                # serializamo
                contacto_cleaned_data = form.cleaned_data

                # obtenemos numero_seccion del contacto
                numero_seccion = request.POST.get('seccion')
                

                # --------- SECCION DEL CONTACTO -------------------

                # obtenemos numero_seccion del contacto
                numero_seccion = request.POST.get('seccion')

                # obtenemos el objeto seccion
                seccion = get_object_or_404(Seccion, pk=numero_seccion)

                # asignamos la seccion al contacto
                contacto.seccion = seccion

                # ----------------- CONTACTO ASOCIADO ---------------------

                # obtenemos id del contacto asociado
                numero_contacto_asociado = request.POST.get('padre')
                
                # obtenemos el objeto contacto
                contacto_asociado = get_object_or_404(Contacto, pk=numero_contacto_asociado)

                # asignamos la seccion al contacto
                contacto.parent = contacto_asociado


                # ------------------- CONTACTOS REPETIDOS -----------------------------
                
                if existenCoincidencias(contacto):
                    # si existe una coincidencia
                    messages.warning(request, "Se encontraron contactos con coincidencias en la informacion ingresada.")
                    # guardamos la informacion en la sesion
                    request.session['datos_contacto'] = contacto_cleaned_data
                    # si existen contactos repetidos redirigir a manejarDuplicados
                    return redirect("contactos:manejarDuplicados")
                
                else:
                    # guardamos los cambios realizados
                    form.save()
                    messages.info(request, f"La informacion de {contacto.apellido_paterno} {contacto.apellido_materno}, {contacto.nombre} ha sido modificada.")
                    return redirect("contactos:mostrarPerfilContacto", id_contacto=contacto.pk)
            else:
                messages.error(request, "Informacion ingresada fue invalidada. Intente de nuevo.")

    else:
        form = ContactoForm(instance=contacto)

    contexto = {
        "contacto": contacto,
        "opciones_secciones": secciones,
        "opciones_contactos": contactos,
        "form": form,
        "modoForm": "Editar",
    }

    return render(request, "contactos/editarContacto.html", contexto)

def mostrarPerfilContacto(request, id_contacto):
    """
        Muestra la informacion de contacto y sus relaciones.
    """

    # obtenemos el contacto
    contacto = get_object_or_404(Contacto, pk=id_contacto)

    # obtenemos secciones
    secciones = Seccion.objects.all()
    
    # obtenemos url para serializador del arbol
    api_url = reverse('api:mostrarRelaciones', args=[contacto.pk])


    # logica post form
    if request.method == "POST":
        # obtenemos el boton submitInsertarRelacion
        submitInsertarRelacion = request.POST.get('submitInsertarRelacion')
        # si el valor es "Insertar"
        if submitInsertarRelacion == "Insertar":

            # obtenemos los datos del form de la peticion POST
            form = ContactoForm(request.POST)

            if form.is_valid():
                # si los campos del form son correctos
                # alamacena la respuesta en una instancia provisional
                nuevo_contacto = form.save(commit=False)

                # asignamos la relacion
                nuevo_contacto.parent = contacto

                if nuevo_contacto.curp:
                    # convertimos CURP a mayusculas
                    nuevo_contacto.curp = nuevo_contacto.curp.upper()

                if nuevo_contacto.clave_elector:
                    # convertimos clave de elector a mayusculas
                    nuevo_contacto.clave_elector = nuevo_contacto.clave_elector.upper()


                # --------- SECCION DEL CONTACTO -------------------

                # obtenemos numero_seccion del contacto
                numero_seccion = request.POST.get('seccion')

                # obtenemos el objeto seccion
                seccion = get_object_or_404(Seccion, pk=numero_seccion)

                # asignamos la seccion al contacto
                contacto.seccion = seccion

                # ------------ CONTACTOS REPETIDOS --------------------

                coincidencias = filtrarContactosDuplicados(nuevo_contacto)
                
                if coincidencias.exists():
                    contexto = {
                        "titulo": "Contactos identicos",
                        "contactos": coincidencias,
                        "opciones_secciones": secciones,
                        "contacto": nuevo_contacto,
                        "form": form,
                        "modoForm": "Duplicado",
                    }

                    messages.warning(request, "Se encontraron contactos con coincidencias en la informacion ingresada.")
                    # si existen contactos repetidos redirigir
                    return render(request, "contactos/mostrarDuplicados.html", contexto)
                
                else:
                    try:
                        # guardamos la informacion del contacto
                        nuevo_contacto.save()
                        # enviamos un mensaje
                        messages.success(request, f"¡{nuevo_contacto.apellido_paterno} {nuevo_contacto.apellido_materno}, {nuevo_contacto.nombre} ingresado a la red!")
                        return redirect("contactos:mostrarPerfilContacto", id_contacto=contacto.pk)
                    except Exception as e:
                        messages.error(request, "Error al guardar contacto:", e)
            else:
                messages.error(request, "Informacion ingresada fue invalidada. Intente de nuevo.")

    else:
        # si no hay peticion POST
        form = ContactoForm()

    contexto = {
        "contacto": contacto,
        "alcance_contactos": contacto.get_descendant_count(),
        "opciones_secciones": secciones,
        "form": form,
        "modoForm": "Insertar",
        "api_url": api_url
    }

    return render(request, "contactos/mostrarPerfilContacto.html", contexto)


def manejarDuplicado(request):
    """
        Al encontrar un registro con coincidencias, esta vista permite corregir
        la informacion ingresada para evitar duplicados.
    """

    # obtenemos los datos del contacto
    datos_contacto = request.session.get('datos_contacto')

