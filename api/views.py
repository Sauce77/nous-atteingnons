# En tu archivo views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from contactos.models import Contacto
from django.shortcuts import get_object_or_404
from .serializers import ContactoSerializer, ContactWithChildrenSerializer

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