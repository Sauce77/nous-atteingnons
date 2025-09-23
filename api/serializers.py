from rest_framework import serializers
from mptt.models import MPTTModel

from contactos.models import Contacto

class ContactoSerializer(serializers.ModelSerializer):
    """
        Serializa la informacion de cada nodo en el arbol para
        convertirla a json.
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = Contacto
        fields = ('id', 
                  'nombre', 
                  'apellido_paterno', 
                  'apellido_materno',
                  'children')

    def get_children(self, obj):
        # Filtra los hijos directos del nodo actual
        children_queryset = obj.children.all()
        # Si hay hijos, se serializan recursivamente
        if children_queryset:
            return ContactoSerializer(children_queryset, many=True).data
        return []