from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from django.shortcuts import render


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
    pledges = Pledge.objects.all()
    serializer = PledgeSerializer(pledges, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def pledge_detail(request, uuid):
    pledges = Pledge.objects.get(pk=uuid)
    serializer = PledgeSerializer(pledges, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def pledge_create(request):
    serializer = PledgeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
