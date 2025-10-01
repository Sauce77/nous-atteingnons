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
        # si el contacto ya esta registrado
        coincidencias = Contacto.objects.exclude(pk=c.pk)

    # CASO 1: Nombre y Apellidos
    if coincidencias.filter(apellido_paterno__iexact=c.apellido_paterno,
                               apellido_materno__iexact=c.apellido_materno,
                               nombre__iexact=c.nombre,
                               ).exists():
        return True
    
    # CASO 2: CURP
    if c.curp:

        if coincidencias.filter(curp=c.curp).exists():
            return True
        
    # CASO 3: Clave Elector
    if c.clave_elector:

        if coincidencias.filter(clave_elector=c.clave_elector).exists():
            return True

    # CASO 4: Telefono
    if c.telefono:

        if coincidencias.filter(telefono=c.telefono).exists():
            return True

    return False

def filtrarContactosDuplicados(c):
    """
        Identifica contactos ya registrados con coincidencias en la 
        informacion del contacto a insertar/modificar.
    """

    contactos = Contacto.objects.all()

    if c.pk:
        # si el contacto esta registrado
        contactos = Contacto.objects.exclude(pk=c.pk)

    coincidencias = contactos.filter(
        # caso 1: nombre y apellido
        ( Q(nombre__iexact=c.nombre) &
         Q(apellido_paterno__iexact=c.apellido_paterno) &
         Q(apellido_materno__iexact=c.apellido_materno)) |
        # caso 2: curp
        (Q(curp=c.curp) & Q(curp__isnull=False)) |
        # caso 3: clave_elector
        (Q(clave_elector=c.clave_elector) & Q(clave_elector__isnull=False)) |
        # caso 4: telefono
        (Q(telefono=c.telefono) & Q(telefono__isnull=False))
    )

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