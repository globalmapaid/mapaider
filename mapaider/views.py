from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView

from .models import Map, Layer, MapFeature
from .serializers import MapSerializer, LayerSerializer


class MapAPIView(RetrieveAPIView):
    serializer_class = MapSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Map.objects.prefetch_related('layers').prefetch_related(
            'layers__features')


class LayerAPIView(RetrieveAPIView):
    serializer_class = LayerSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Layer.objects.all()
