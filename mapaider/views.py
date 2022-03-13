from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.generics import RetrieveAPIView

from .models import MapProject, Layer, MapFeature
from .serializers import MapSerializer, LayerSerializer


class MapAPIView(RetrieveAPIView):
    serializer_class = MapSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return MapProject.objects.prefetch_related('layers').prefetch_related(
            'layers__features')


class LayerAPIView(RetrieveAPIView):
    serializer_class = LayerSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Layer.objects.all()


@xframe_options_exempt
def show_map(request, slug: str):
    return render(request, 'mapaider/map-viewer.html')
