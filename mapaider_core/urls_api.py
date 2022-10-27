from django.urls import path, include

from .views import schema_view

urlpatterns = [
    path('auth/', include('users.urls')),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('mapaider/', include('mapaider.urls_api')),
]
