from django.urls import path

import api.views as views

app_name = 'api'

urlpatterns = [
    path('arbol/<int:pk>/', views.ContactoSubtreeView.as_view(), name="mostrarSubArbol"),
    path('contactos/<int:pk>/', views.ContactDetailWithChildrenView.as_view(), name="mostrarRelaciones")
]