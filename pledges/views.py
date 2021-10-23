from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializers import *
from django.shortcuts import render
from .ShapeImporter import ShapeImporter
from .models import Pledge


class PledgeViewSet(viewsets.ModelViewSet):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


@api_view(["GET"])
def api_overview(request):
    api_urls = {
        "Make a Pledge": "/make-pledge/"
    }

    return Response(api_urls)


@ensure_csrf_cookie
def make_pledge(request):
    return render(request, "make-pledge.html", )


@api_view(["GET"])
def pledge_list(request):
    pledges = Pledge.objects.filter(visibility__gt=0).exclude(geom_type__isnull=True)
    serializer = PledgeSerializer(pledges, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def pledge_list_compact(request):
    pledges = Pledge.objects.filter(visibility__gt=0).exclude(geom_type__isnull=True)
    serializer = PledgeListCompactSerializer(pledges, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def pledge_detail(request, uuid):
    pledges = Pledge.objects.get(pk=uuid)
    serializer = PledgeSerializer(pledges, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def pledge_create(request):
    serializer = PledgeCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


def import_shapefile(request):
    Pledge.truncate()

    ShapeImporter.import_farm_pledges()
    ShapeImporter.import_garden_pledges()
    ShapeImporter.import_church_pledges()
    ShapeImporter.import_school_pledges()
    ShapeImporter.import_government_pledges()
    ShapeImporter.import_railway_stations_pledges()

    return HttpResponse('OK!')


def resave_all(request):
    pledges = Pledge.objects.all()

    for pledge in pledges:
        pledge.save()

    return HttpResponse('OK!')
