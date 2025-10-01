from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import F

import openpyxl

from scripts.validacionesContactos import filtrarContactosDuplicados, existenCoincidencias
from scripts.operacionesContactos import borrarContacto, obtenerDescendientesPlano, insertarContactosExcel

import pandas as pd

from .models import Contacto, Seccion
from .forms import ContactoForm, ExcelForm
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
                    # guardamos el id de contacto como nulo
                    request.session['id_contacto'] = None
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

    if request.method == "POST":
        # obtenemos btnBorrarContacto
        btnBorrarContacto = request.POST.get('btnBorrarContacto')
        # obtenemos btnAfiliacion
        btnAfiliacion = request.POST.get('btnAfiliacion')
        # obtenemos btnAfiliacion
        btnDescargarExcel = request.POST.get('btnDescargarExcel')

        if btnBorrarContacto == "Borrar":
            # obtenemos id del contacto
            id_contacto = request.POST.get("idContacto")

            if borrarContacto(id_contacto):
                # si el contacto se pudo eliminar
                messages.error(request, "Contacto eliminado.")
                return redirect("contactos:mostrarContactos")

            else:
                messages.warning(request, "Este contacto mantiene relaciones registradas. Considere marcar el contacto como 'Desafiliado' o modifique los contactos relacionados.")

        elif btnAfiliacion == "Afiliado":
            # cambiamos el estado a desafiliado
            contacto.estatus = "D"
            contacto.save()
            messages.info(request, f"El estatus del contacto cambio a 'Desafiliado'")

        elif btnAfiliacion == "Desafiliado":
            # cambiamos el estado a desafiliado
            contacto.estatus = "A"
            contacto.save()
            messages.info(request, f"El estatus del contacto cambio a 'Afiliado'")

        elif btnDescargarExcel == "Descargar":

            # obtenemos url para descencdientes
            api_url = reverse("api:mostrarContactoPlano", kwargs={'pk': contacto.pk})

            url_absoluta = request.build_absolute_uri(api_url)

            datos = obtenerDescendientesPlano(url_absoluta, contacto)

            if datos:

                # archivo de salida
                nombre_archivo_salida = f'Contactos_{contacto.apellido_paterno}_{contacto.apellido_materno}_{contacto.nombre}.xlsx'
                
                df = pd.DataFrame(datos)
        
                # 3. Crear el objeto HttpResponse de Django
                # Especificamos el Content-Type para un archivo Excel (.xlsx)
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
                
                # 4. Configurar la cabecera Content-Disposition
                # 'attachment' indica al navegador que descargue el archivo.
                # 'filename' especifica el nombre del archivo que se descargará.
                response['Content-Disposition'] = f'attachment; filename="{nombre_archivo_salida}"'
                
                # 5. Guardar el DataFrame directamente en el objeto HttpResponse
                # Usamos BytesIO (proceso interno de to_excel) para no escribir el archivo en disco.
                df.to_excel(response, index=False, sheet_name='Datos Aplanados')
                
                # 6. Devolver la respuesta al navegador
                messages.success(request, f"Se ha completado la descarga {nombre_archivo_salida}")
                return response
            
            else:
                messages.error(request, "Hubo un problema al descargar el archivo.")


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

    return HttpResponse("Coincidencias")

    # obtenemos los datos del contacto
    datos_contacto = request.session.get('datos_contacto')

    # obtenemos id del contacto
    id_contacto = request.session.get('id_contacto')

    if datos_contacto:

        # incializamos seccion y contacto_asociado
        seccion = None
        contacto_asociado = None

        if datos_contacto["seccion"]:
            # obtenemos numero seccion
            numero_seccion = datos_contacto["seccion"]
            # obtenemos seccion
            seccion = get_object_or_404(Seccion, pk=numero_seccion)
            # retiramos seccion de los datos
            datos_contacto["seccion"] = None

        if datos_contacto["parent"]:
            # obtenemos con id de contacto asociado
            id_contacto_asociado = datos_contacto["parent"]
            # obtenemos objeto contacto asociado
            contacto_asociado = get_object_or_404(Contacto, pk=id_contacto_asociado)
            # retiramos contacto asociado de los datos
            datos_contacto["parent"] = None
        
        # creamos una instancia de contacto
        contacto = Contacto(**datos_contacto)

        if seccion:
            # actualizamos la seccion del contacto
            contacto.seccion = seccion
        
        if contacto_asociado:
            # actualizamos el contacto asociado del contacto
            contacto.parent = contacto_asociado
    else:
        contexto = {
            "titulo": "No se pudo encontrar informacion.",
            "descripcion": "La informacion ingresada no pudo ser insertada.",
        }

        return render(request, "core/error.html", contexto)

    if request.method == "POST":
        
        form = ContactoForm(request.POST, instance=contacto)

        if request.session.get('id_contacto'):
            # borramos el id de contacto de la sesion
            del request.session["id_contacto"]

        if request.session.get('datos_contacto'):
            # borramos los datos de contacto de la sesion
            del request.session["datos_contacto"]

        if form.is_valid():
            # si la informacion insertada es valida
            # alamacenamos las respuestas en una instancia temporal

            # obtenemos una instancia temporal
            form.save()

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
        "id_contacto": id_contacto,
        "contactos": coincidencias,
    }

    return render(request, "contactos/mostrarDuplicados.html", contexto)

def subirContactos(request, id_contacto):
    """
        A partir de un archivo de Excel, asigna los nuevos registros como
        contactos asociados del contacto elegido.
    """

    # obtenemos contacto
    contacto = get_object_or_404(Contacto, pk=id_contacto)

    # inicializamos contactos creados
    contactos_creados = None

    if request.method == "POST":
        # obtenemos boton btnSubirContactos
        btnSubirContactos = request.POST.get("btnSubirContactos")

        if btnSubirContactos == "Subir":

            form = ExcelForm(request.POST, request.FILES)

            if form.is_valid():
                # obtenemos el archivo subido
                archivo_excel = request.FILES["archivo"]

                try:
                    archivo = openpyxl.load_workbook(archivo_excel)
                except Exception:
                    messages.error(request, "El archivo subido no es compatible con Excel. Revise que la extension del archivo sea .xlsx o .xls")
                
                # leemos el archivo en un dataframe
                df_archivo = pd.read_excel(archivo_excel, engine='openpyxl')

                # creamos contactos
                contactos_creados = insertarContactosExcel(df_archivo, contacto)
                messages.info(request, f"Se han insertado {len(contactos_creados)} contacto(s).")

            else:
                messages.error(request, "El archivo ingresado no pudo ser validado.")
            
    else:
        form = ExcelForm()

    contexto = {
        "form": form,
        "contacto": contacto,
        "contactos": contactos_creados, 
    }
    return render(request, "contactos/subirContactos.html", contexto)


def home(request):
    """
        Renderiza el inicio de la aplicacion.
    """

    return render(request, "core/home.html")