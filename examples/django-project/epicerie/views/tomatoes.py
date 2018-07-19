from rest_framework import viewsets, serializers

from ..models import Tomato


class TomatoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tomato
        fields = [
            'name',
            'weight'
        ]


class TomatoViewSet(viewsets.ModelViewSet):
    queryset = Tomato.objects.all()
    serializer_class = TomatoSerializer
