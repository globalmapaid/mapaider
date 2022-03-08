from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Organization, Map, Layer, MapLayer, MapFeature


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['get_organization', 'map', 'layer', 'priority']
    list_filter = ['map']
    ordering = ['map', 'priority']

    @admin.display(ordering='author__organization')
    def get_organization(self, obj):
        return obj.map.organization


@admin.register(MapFeature)
class MapFeatureAdmin(LeafletGeoAdmin):
    list_display = ['name', 'layer', 'geom_type', 'visibility']


admin.site.register([Organization, Map, Layer])
