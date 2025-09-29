from django.db.models import Q
from contactos.models import Contacto, Seccion


def existenCoincidencias(c):
    """
        Si encuentra una coincidencia, retorna true
        de lo contrario false
    """

    # si el contacto ya tiene un id
    if c.id:
        # 1. Excluir el contacto actual.
        base_filtro = Contacto.objects.exclude(pk=c.id)
    else:
        # el contacto no esta registrado aun
        base_filtro = Contacto.objects.all()


    # CASO 1: Coincidencias de Nombre Completo
    coincidencias = base_filtro.filter(
        Q(apellido_paterno__iexact=c.apellido_paterno) & 
        Q(apellido_materno__iexact=c.apellido_materno) & 
        Q(nombre__iexact=c.nombre))
    
    if coincidencias.exists():
        return True
    
    # CASO 2: Coincidencias de CURP
    if c.curp:
        coincidencias = base_filtro.filter(Q(curp__iexact=c.curp))

        if coincidencias.exists():
            return True

    # CASO 3: Coincidencias de Clave de Elector
    if c.clave_elector:
        coincidencias = base_filtro.filter(Q(clave_elector__iexact=c.clave_elector))

        if coincidencias.exists():
            return True

    # CASO 4: Coincidencias de Telefono
    if c.telefono:
        coincidencias = base_filtro.filter(Q(telefono__iexact=c.telefono))

        if coincidencias.exists():
            return True

    return False

def filtrarContactosDuplicados(c):
    """
        Identifica contactos ya registrados con coincidencias en la 
        informacion del contacto a insertar/modificar.
    """

    # si el contacto ya tiene un id
    if c.id:
        # 1. Excluir el contacto actual.
        base_filtro = Contacto.objects.exclude(pk=c.id)
    else:
        # el contacto no esta registrado aun
        base_filtro = Contacto.objects.all()

    # 2. Definir las condiciones de coincidencia (OR lógica)
    coincidencia_q_object = Q()

    # CASO 1: Coincidencias de Nombre Completo
    coincidencia_q_object |= (
        Q(apellido_paterno__iexact=c.apellido_paterno) & 
        Q(apellido_materno__iexact=c.apellido_materno) & 
        Q(nombre__iexact=c.nombre)
    )

    # CASO 2: Coincidencias de CURP
    if c.curp:
        coincidencia_q_object |= Q(curp__iexact=c.curp)

    # CASO 3: Coincidencias de Clave de Elector
    if c.clave_elector:
        coincidencia_q_object |= Q(clave_elector__iexact=c.clave_elector)

    # CASO 4: Coincidencias de Telefono
    if c.telefono:
        # Nota: No es necesario excluir los None/vacíos aquí,
        # ya que el filtro solo se aplica si c.telefono tiene valor.
        coincidencia_q_object |= Q(telefono=c.telefono)

    # 3. Aplicar el filtro OR a la base con exclusión
    coincidencias = base_filtro.filter(coincidencia_q_object)

    # El QuerySet 'coincidencias' ahora contiene todos los registros
    # que coinciden con AL MENOS una de las condiciones y
    # NO son el contacto actual.

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