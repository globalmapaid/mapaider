from django.urls import path
from .views import MapAPIView, LayerAPIView


urlpatterns = [
    # path('map/<str:uuid>', map_detail)
    path('map/<str:slug>', MapAPIView.as_view()),
    path('layer/<str:uuid>', LayerAPIView.as_view())
]
