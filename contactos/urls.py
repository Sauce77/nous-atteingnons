from django.urls import path

import contactos.views as views

app_name = 'contactos'

urlpatterns = [
    path("", views.mostrarContactos, name="mostrarContactos"),
    path("perfil/<int:id_contacto>/", views.mostrarPerfilContacto, name="mostrarPerfilContacto"),
    path("insertar/", views.insertarContacto, name="insertarContacto"),
    path("editar/<int:id_contacto>/", views.editarContacto, name="editarContacto"),
    path("duplicados/", views.manejarDuplicado, name="manejarDuplicados"),
    path("subir/<int:id_contacto>", views.subirContactos, name="subirContactos"),
]