from django.db.models import Q
from contactos.models import Contacto, Seccion


def existenCoincidencias(c):
    """
        Si encuentra una coincidencia, retorna true
        de lo contrario false.
        c: contacto.
    """

    coincidencias = Contacto.objects.all()

    if c.pk:
        # si el usuario ya esta registrado
        coincidencias = Contacto.objects.exclude(pk=c.pk)

    if coincidencias.filter(apellido_paterno__iexact=c.apellido_paterno,
                               apellido_materno__iexact=c.apellido_materno,
                               nombre__iexact=c.nombre,
                               ).exists():
        return True
    
    # CASO 2: CURP
    if c.curp:
        caso = coincidencias.filter(curp__iexact=c.curp)

        if caso.exists():
            return True
        
    # CASO 3: Clave Elector
    if c.clave_elector:
        caso = coincidencias.filter(clave_elector__iexact=c.clave_elector)

        if caso.exists():
            return True

    # CASO 4: Telefono
    if c.telefono:
        caso = coincidencias.filter(telefono=c.telefono)

        if caso.exists():
            return True

    return False

def filtrarContactosDuplicados(c):
    """
        Identifica contactos ya registrados con coincidencias en la 
        informacion del contacto a insertar/modificar.
    """

    coincidencias = Contacto.objects.none()

    # CASO 1: Nombre y apellidos
    caso = coincidencias.filter(nombre__iexact=c.nombre).filter(apellido_paterno=c.apellido_paterno).filter(apellido_materno=c.apellido_materno)

    if caso.exists():
        coincidencias = coincidencias.union(caso)
    
    # CASO 2: CURP
    if c.curp:
        caso = coincidencias.filter(curp__iexact=c.curp)

        if caso.exists():
            coincidencias = coincidencias.union(caso)
        
    # CASO 3: Clave Elector
    if c.clave_elector:
        caso = coincidencias.filter(clave_elector__iexact=c.clave_elector)

        if caso.exists():
            coincidencias = coincidencias.union(caso)

    # CASO 4: Telefono
    if c.telefono:
        caso = coincidencias.filter(telefono=c.telefono)

        if caso.exists():
            coincidencias = coincidencias.union(caso)

    if c.pk:
        coincidencias = coincidencias.exclude(pk=c.pk)

    return coincidencias
    

def normalizarDatosContacto(form):
    """
        Recibe un form ya validado y normaliza los campos de nombre,
        apellidos, curp y clave de elector.

        Retorna una instancia temporal validada de Contacto.
    """
    # normalizamos el nombre 
    form.cleaned_data["nombre"] = form.cleaned_data["nombre"].upper()

    # normalizamos el apellido_paterno
    form.cleaned_data["apellido_paterno"] = form.cleaned_data["apellido_paterno"].upper()

    # normalizamos el apellido_materno
    form.cleaned_data["apellido_materno"] = form.cleaned_data["apellido_materno"].upper()
    
    if form.cleaned_data["curp"]:
        # colocamos la curp en mayusculas
        form.cleaned_data["curp"] = form.cleaned_data["curp"].upper()

    if form.cleaned_data["clave_elector"]:
        # colocamos la clave_elector en mayusculas
        form.cleaned_data["clave_elector"] = form.cleaned_data["clave_elector"].upper()

    contacto = form.save(commit=False)

    return contacto