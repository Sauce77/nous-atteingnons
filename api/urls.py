from django.urls import path

import api.views as views

app_name = 'api'

urlpatterns = [
    path('contacto/<int:pk>/', views.ContactoSubtreeView.as_view(), name="mostrarSubArbol")
]