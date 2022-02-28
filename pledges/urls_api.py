from django.urls import path

from .views import *

urlpatterns = [
    path("", api_overview, name="api-overview"),
    path("list", pledge_list, name="pledge-list"),
    path("list-compact", pledge_list_compact, name="pledge-list-compact"),
    path('pledge-types', pledge_type_list, name="pledge-types"),
    path("create", pledge_create, name="pledge-create"),
    # path("pledge/<str:uuid>", pledge_detail, name="pledge-detail"),
]
