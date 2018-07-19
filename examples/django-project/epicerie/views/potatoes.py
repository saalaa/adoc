from rest_framework import viewsets, serializers

from ..models import Potato


class PotatoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Potato
        fields = [
            'name',
            'weight'
        ]


class PotatoViewSet(viewsets.ModelViewSet):
    queryset = Potato.objects.all()
    serializer_class = PotatoSerializer
