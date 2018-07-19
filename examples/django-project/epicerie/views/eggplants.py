from rest_framework import viewsets, serializers

from ..models import Eggplant


class EggplantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Eggplant
        fields = [
            'name',
            'weight'
        ]


class EggplantViewSet(viewsets.ModelViewSet):
    queryset = Eggplant.objects.all()
    serializer_class = EggplantSerializer
