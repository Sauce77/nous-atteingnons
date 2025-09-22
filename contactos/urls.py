from django.urls import path

import contactos.views as views

urlpatterns = [
    path("", views.mostrarContactos, name="mostrarContactos"),
]