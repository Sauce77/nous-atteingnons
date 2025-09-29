# En tu archivo views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from contactos.models import Contacto
from django.shortcuts import get_object_or_404
from .serializers import ContactoSerializer, ContactWithChildrenSerializer, ContactSerializer

class ContactDetailWithChildrenView(APIView):
    def get(self, request, pk):
        contact = get_object_or_404(Contacto, pk=pk)
        
        # El serializador se encarga de incluir los hijos directos
        serializer = ContactWithChildrenSerializer(contact)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContactoSubtreeView(generics.RetrieveAPIView):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
    lookup_field = 'pk'

    def get_object(self):
        # Obtiene el nodo raíz del subárbol a partir del ID de la URL
        node = super().get_object()

        # Obtiene todos los descendientes del nodo, incluyéndolo a sí mismo
        descendants = node.get_descendants(include_self=True)

        return node

    def get_queryset(self):
        node_id = self.kwargs.get(self.lookup_field)
        if not node_id:
            return Contacto.objects.none()

        try:
            node = Contacto.objects.get(pk=node_id)
            return node.get_descendants(include_self=True)
        except Contacto.DoesNotExist:
            return Contacto.objects.none()

class ContactoPlanoView(APIView):

    def get(self, request, pk, format=None):
        # 1. Obtener el nodo base
        try:
            node = Contacto.objects.get(pk=pk)
        except Contacto.DoesNotExist:
            return Response(
                {"detail": "Nodo no encontrado."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 2. Obtener los descendientes E INCLUIR AL NODO RAÍZ
        # Al pasar include_self=True, el QuerySet devuelto contendrá el nodo base
        # junto con todos sus descendientes.
        descendants_queryset = node.get_descendants(include_self=True)

        # 3. Serializar el QuerySet
        serializer = ContactSerializer(descendants_queryset, many=True)
        
        # 4. Devolver la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)