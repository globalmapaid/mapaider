"""wemod_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pledges.views import *
from wemod_api import settings

admin.site.site_url = "/pledge/map"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pledge/', include('pledges.urls')),
    path('api/pledge/', include('pledges.urls_api')),

    path('mapaider/', include('mapaider.urls')),
    path('api/mapaider/', include('mapaider.urls_api')),
    # path('import', import_shapefile)
    # path('import', import_excel)
    # path('resave', resave_all)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
