from django.shortcuts import get_object_or_404
from django.urls import reverse
import requests
import json
import pandas as pd
import openpyxl


from contactos.models import Contacto, Seccion

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


def obtenerDescendientesPlano(api_url ,contacto):
    """
        A partir de los descendientes de un contactos, muestra la informacion
        en un excel.
    """

    try:
        # 1. Realizar la petición GET al endpoint
        response = requests.get(api_url)

        # 2. Verificar que la petición fue exitosa (código 200)
        response.raise_for_status() 
        # Esto lanzará una excepción para códigos 4xx o 5xx

        # 3. Cargar la respuesta JSON. 
        # Asumimos que la respuesta es una lista de diccionarios (datos planos)
        datos_planos = response.json()

        if not isinstance(datos_planos, list) or not datos_planos:
            print("🛑 Error: La respuesta del endpoint no es una lista o está vacía.")
            exit()

        return datos_planos

    except requests.exceptions.HTTPError as err_h:
        print(f"🛑 Error HTTP: {err_h}")
    except requests.exceptions.ConnectionError as err_c:
        print(f"🛑 Error de Conexión: {err_c}")
    except requests.exceptions.Timeout as err_t:
        print(f"🛑 Error de Tiempo de Espera (Timeout): {err_t}")
    except requests.exceptions.RequestException as err:
        print(f"🛑 Error Inesperado: {err}")
    except json.JSONDecodeError:
        print("🛑 Error: La respuesta no pudo decodificarse como JSON. Verifica el formato del endpoint.")
    except Exception as e:
        print(f"🛑 Ocurrió un error inesperado: {e}")


def insertarContactosExcel(df, contacto_asociado):
    """
        Recibe un dataframe del archivo leido. Para los datos que sean
        validos seran registrados con el contacto actual.
    """

    # almacenamos los contactos creados
    contactos_creados = []

    # convertimos las columnas a mayusculas
    df.columns = df.columns.str.upper()

    # iteramos para cada registro
    for index, row in df.iterrows():

        if 'NOMBRE' in df.columns:
            nombre = row['NOMBRE']

        if 'APELLIDO_PATERNO' in df.columns:
            apellido_paterno = row['APELLIDO_PATERNO']
        
        if 'APELLIDO_MATERNO' in df.columns:
            apellido_materno = row['APELLIDO_MATERNO']

        if 'CURP' in df.columns:
            curp = row['CURP']

        if 'CLAVE_ELECTOR' in df.columns:
            clave_elector = row['CLAVE_ELECTOR']
        
        if 'TELEFONO' in df.columns:
            telefono = row['TELEFONO']

        if 'EMAIL' in df.columns:
            email = row['EMAIL']

        if 'DOMICILIO' in df.columns:
            domicilio = row['DOMICILIO']

        # incializamos seccion
        seccion = None

        if 'SECCION' in df.columns:
            # obtenemos el numero de seccion
            numero_seccion = row['SECCION']
            
            try:
                # obtenemos seccion
                seccion = Seccion.objects.get(pk=numero_seccion)
            except Seccion.DoesNotExist:
                seccion = None

        # creamos nuevo contacto
        contacto_nuevo = Contacto.objects.create(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            curp=curp,
            clave_elector=clave_elector,
            telefono=telefono,
            email=email,
            domicilio=domicilio,
            seccion=seccion,
            parent=contacto_asociado
        )

        try:
            # almacenamos nuevo contacto
            contacto_nuevo.save()
            contactos_creados.append(contacto_nuevo)
        except Exception:
            continue

    return contactos_creados
