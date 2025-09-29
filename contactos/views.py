from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib import messages

from scripts.validacionesContactos import filtrarContactosDuplicados, existenCoincidencias, normalizarDatosContacto

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

def insertarContacto(request):
    """
        Inserta un contacto en la red.
    """

    if request.method == "POST":

        # obtenemos boton btnSubmitContacto
        btnSubmitContacto = request.POST.get("btnSubmitContacto")

        if btnSubmitContacto == "Aceptar":
            # instanciamos el form con las respuestas
            form = ContactoForm(request.POST)

            if form.is_valid():
                # si la informacion es correcta
                # alamacenamos las respuestas en una instancia temporal

                # obtenemos una instancia temporal normalizada de contacto
                contacto = form.save(commit=False)

                # --------------- CONTACTOS REPETIDOS -------------------
                if existenCoincidencias(contacto):
                    # si existe una coincidencia
                    messages.warning(request, "Se encontraron contactos con coincidencias en la informacion ingresada.")
                    # serializamos informacion del form
                    contacto_cleaned_data = form.cleaned_data
                    
                    if contacto.seccion:
                        # insertamos solo llave foranea de la seccion
                        contacto_cleaned_data['seccion'] = contacto.seccion.pk

                    if contacto.parent:
                        # insertamos solo llave foranea del contacto asociado
                        contacto_cleaned_data['parent'] = contacto.parent.pk

                    # guardamos la informacion en la sesion
                    request.session['datos_contacto'] = contacto_cleaned_data
                    # si existen contactos repetidos redirigir a manejarDuplicados
                    return redirect("contactos:manejarDuplicados")
                
                else:
                    # guardamos los cambios realizados
                    contacto.save()
                    messages.success(request, f"Nuevo contacto ingresado con exito!")
                    return redirect("contactos:mostrarPerfilContacto", id_contacto=contacto.pk)

            else:
                messages.error(request, "La informacion ingresada no pudo ser validada. Intente de nuevo.")
    else:
        # crear un form vacio
        form = ContactoForm()

    contexto = {
        "form": form
    }

    return render(request, "contactos/editarContacto.html", contexto)

def editarContacto(request, id_contacto):
    """
        Permite modificar la informacion y la relacion de un contacto seleccionado.
    """

    # obtenemos el contacto
    contacto = get_object_or_404(Contacto, pk=id_contacto)
    
    # logica post form
    if request.method == "POST":
        # obtenemos boton submitGuardar
        btnSubmitContacto = request.POST.get('btnSubmitContacto')

        if btnSubmitContacto == "Aceptar":
            # obtenemos respuestas de la peticion POST
            form = ContactoForm(request.POST, instance=contacto)

            if form.is_valid():
                # si la informacion insertada es valida
                # alamacenamos las respuestas en una instancia temporal

                # obtenemos una instancia temporal normalizada de contacto
                contacto = form.save(commit=False)
                # ------------------- CONTACTOS REPETIDOS -----------------------------
                
                if existenCoincidencias(contacto):
                    # si existe una coincidencia
                    messages.warning(request, "Se encontraron contactos con coincidencias en la informacion ingresada.")
                    # serializamos informacion del form
                    contacto_cleaned_data = form.cleaned_data

                    if contacto.seccion:
                        # insertamos solo llave foranea de la seccion
                        contacto_cleaned_data['seccion'] = contacto.seccion.pk

                    if contacto.parent:
                        # insertamos solo llave foranea del contacto asociado
                        contacto_cleaned_data['parent'] = contacto.parent.pk

                    # guardamos la informacion en la sesion
                    request.session['datos_contacto'] = contacto_cleaned_data
                    # guardamos el id de contacto
                    request.session['id_contacto'] = contacto.id
                    # si existen contactos repetidos redirigir a manejarDuplicados
                    return redirect("contactos:manejarDuplicados")
                
                else:
                    # guardamos los cambios realizados
                    contacto = form.save()
                    messages.info(request, f"La informacion de {contacto.apellido_paterno} {contacto.apellido_materno}, {contacto.nombre} ha sido modificada.")
                    return redirect("contactos:mostrarPerfilContacto", id_contacto=contacto.pk)
            else:
                messages.error(request, "Informacion ingresada fue invalidada. Intente de nuevo.")

    else:
        form = ContactoForm(instance=contacto)

    contexto = {
        "contacto": contacto,
        "form": form,
    }

    return render(request, "contactos/editarContacto.html", contexto)

def mostrarPerfilContacto(request, id_contacto):
    """
        Muestra la informacion de contacto y sus relaciones.
    """

    # obtenemos el contacto
    contacto = get_object_or_404(Contacto, pk=id_contacto)
    
    # obtenemos url para serializador del arbol
    api_url = reverse('api:mostrarRelaciones', args=[contacto.pk])

    contexto = {
        "contacto": contacto,
        "alcance_contactos": contacto.get_descendant_count(),
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

    # obtenemos id del contacto
    id_contacto = request.session.get('id_contacto')

    if id_contacto:
        # obtenemos objeto del contacto
        contacto = get_object_or_404(Contacto, pk=id_contacto)
    else:
        # creamos una instancia de contacto
        contacto = Contacto(**datos_contacto)


    if request.method == "POST":
        
        form = ContactoForm(request.POST, instance=contacto)

        if form.is_valid():
            # si la informacion insertada es valida
            # alamacenamos las respuestas en una instancia temporal

            # obtenemos una instancia temporal
            form.save()

            if request.session.get("id_contacto"):
                # borramos el id de contacto de la sesion
                del request.session["id_contacto"]

            if request.session.get("datos_contacto"):
                # borramos los datos de contacto de la sesion
                del request.session["datos_contacto"]

            messages.info(request, f"Informacion de contacto ingresada con exito!.")
            return redirect("contactos:mostrarPerfilContacto", id_contacto=contacto.pk)
        
        else:
            # el fomulario presenta errores
            messages.error(request, "La informacion ingresada no fue validada.")

    
    else:
        form = ContactoForm(initial=datos_contacto, instance=contacto)

    # obtenemos las coincidencias encontradas
    coincidencias = filtrarContactosDuplicados(contacto)
    
    contexto = {
        "form": form,
        "contactos": coincidencias,
    }

    return render(request, "contactos/mostrarDuplicados.html", contexto)

