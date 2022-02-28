from django.urls import path

from .views import *

urlpatterns = [
    path('make', make_pledge, name='pledge-make'),
    path('map', pledge_map, name='pledge-map'),
]
