from django.urls import path

from .views import *

urlpatterns = [
    path('map/<str:slug>', show_map, name='mapaider-map'),
]
