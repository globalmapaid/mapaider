from django.urls import path, include

urlpatterns = [
    # path('auth/', include('knox.urls')),
    path('auth/', include('users.urls')),
    path('mapaider/', include('mapaider.urls_api')),
]
