from django.urls import path, include

from .views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('auth/', include('users.urls')),
    path('doc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/', SpectacularSwaggerView.as_view(url_name='schema', template_name='api_docs/swagger_ui.html'), name='swagger-ui'),
    path('mapaider/', include('mapaider.urls_api')),
]
