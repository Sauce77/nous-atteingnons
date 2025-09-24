# En tu archivo views.py
from rest_framework import generics
from contactos.models import Contacto
from .serializers import ContactoSerializer

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