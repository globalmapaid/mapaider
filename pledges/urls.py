from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(prefix='v1/pledges', viewset=PledgeViewSet, basename='pledge')

urlpatterns = router.urls
urlpatterns += [
    path("api/pledge", api_overview, name="api-overview"),
    path("api/pledge/list", pledge_list, name="pledge-list"),
    path("api/pledge/create", pledge_create, name="pledge-create"),
    path("api/pledge/<str:uuid>", pledge_detail, name="pledge-detail"),

]
