from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Map, Layer, MapFeature
from .serializers import MapViewerMapSerializer, MapViewerLayerSerializer, ContributionMapFeatureSerializer, \
    MapViewerMapFeatureSerializer


class MapAPIView(RetrieveAPIView):
    serializer_class = MapViewerMapSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Map.objects.prefetch_related('layers').prefetch_related(
            'layers__features')


class LayerAPIView(RetrieveAPIView):
    serializer_class = MapViewerLayerSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Layer.objects.all()


class ContributionMapFeatureAPIView(APIView):
    """
        Contribution Map Feature - Create API View
    """

    def post(self, request):
        serializer = ContributionMapFeatureSerializer(data=request.data)
        if serializer.is_valid():
            feature = serializer.save()
            return Response(MapViewerMapFeatureSerializer(feature).data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@xframe_options_exempt
def show_map(request, slug: str):
    return render(request, 'mapaider/map-viewer.html', {'slug': slug})
