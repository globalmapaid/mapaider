import os

from django.conf import settings
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

import numpy as np
import pandas as pd
from dateutil import parser

from .serializers import *
from django.shortcuts import render
from .ShapeImporter import ShapeImporter
from .models import Pledge, PledgeType


class PledgeViewSet(viewsets.ModelViewSet):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


@api_view(["GET"])
def api_overview(request):
    api_urls = {
        "Make a Pledge": "/make-pledge/"
    }

    return Response(api_urls)


# @ensure_csrf_cookie
def make_pledge(request):
    return render(request, "pledge-make.html", )


def pledge_map(request):
    return render(request, "pledge-map.html", )


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
def pledge_type_list(request):
    pledge_types = PledgeType.objects.order_by('id').all()
    serializer = PledgeTypeSerializer(pledge_types, many=True)
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

    return Response(serializer.data, status=status.HTTP_201_CREATED)


def import_shapefile(request):
    Pledge.truncate()

    ShapeImporter.import_farm_pledges()
    ShapeImporter.import_garden_pledges()
    ShapeImporter.import_church_pledges()
    ShapeImporter.import_school_pledges()
    ShapeImporter.import_government_pledges()
    ShapeImporter.import_railway_stations_pledges()

    return HttpResponse('OK!')


def import_excel(request):
    filename = 'update-20220205.xlsx'
    file_path = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'data', 'excel', filename))

    columns = ['submission_date', 'pledge_type', 'first_name', 'last_name', 'email', 'phone', 'street', 'city',
               'postcode', 'area', 'measurement_unit', 'reason', 'latitude', 'longitude']

    df = pd.read_excel(file_path)
    df.columns = columns
    df = df.replace({np.nan: None})

    def format_data(item):
        item['submission_date'] = parser.parse(item['submission_date'])
        item['postcode'] = None if item['postcode'] is None else str(item['postcode']).upper()
        return item

    data_dict = list(map(format_data, df.to_dict(orient='records')))

    for item in data_dict:
        pledge_type = PledgeType.objects.get(name=item['pledge_type'])
        if item.get('latitude') is not None and item.get('latitude') is not None:
            geom = Point(item.get('longitude'), item.get('latitude'))
            geom_type = geom.geom_type
        else:
            geom = None
            geom_type = None
        notes = 'Excel 2022-02-06'

        new_pledge = Pledge(
            type=pledge_type,
            area=item.get('area'),
            geom=geom,
            geom_type=geom_type,
            measurement_unit=item.get('measurement_unit'),
            first_name=item.get('first_name'),
            last_name=item.get('last_name'),
            street=item.get('street'),
            city=item.get('city'),
            postcode=item.get('postcode'),
            email=item.get('email'),
            phone=item.get('phone'),
            notes=notes,
            reason=item.get('reason'),
            submitted_at=item.get('submission_date'),
            visibility=4
        )

        try:
            new_pledge.save()
        except DataError:
            pass
        except ValueError:
            pass

    return HttpResponse('Allright!')
    pass


def resave_all(request):
    pledges = Pledge.objects.all()

    for pledge in pledges:
        pledge.save()

    return HttpResponse('OK!')
