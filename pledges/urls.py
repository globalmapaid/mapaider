from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(prefix='v1/pledges', viewset=PledgeViewSet, basename='pledge')

urlpatterns = router.urls
urlpatterns += [
    path("pledge", api_overview, name="api-overview"),
    path("pledge/list", pledge_list, name="pledge-list"),
    path("pledge/list-compact", pledge_list_compact, name="pledge-list-compact"),
    # path('pledge/list', PledgeList.as_view(), name="pledge-filtered"),
    path("pledge/create", pledge_create, name="pledge-create"),
    # path("pledge/<str:uuid>", pledge_detail, name="pledge-detail"),
]
