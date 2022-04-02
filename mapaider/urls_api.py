from django.urls import path
from .views import MapAPIView, LayerAPIView, ContributionMapFeatureAPIView


urlpatterns = [
    # path('map/<str:uuid>', map_detail)
    path('map/<str:slug>', MapAPIView.as_view()),
    path('layer/<str:uuid>', LayerAPIView.as_view()),
    path('contribution/mapfeature', ContributionMapFeatureAPIView.as_view())
]
