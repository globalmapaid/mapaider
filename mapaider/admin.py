from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Organization, Map, Layer, MapLayer, MapFeature


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['organization', 'map', 'layer', 'priority']
    list_filter = ['map', 'layer']
    ordering = ['map', 'priority']

    @admin.display(ordering='map__organization', description='Organisation')
    def organization(self, obj):
        return obj.map.organization


@admin.register(MapFeature)
class MapFeatureAdmin(LeafletGeoAdmin):
    list_display = ['name', 'layer', 'geom_type', 'visibility']
    actions_on_bottom = True
    list_editable = ['visibility']
    search_fields = ['uuid', 'name', 'layer']
    readonly_fields = ['latitude', 'longitude']
    list_filter = ['layer', 'geom_type', 'visibility', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


admin.site.register([Organization, Map, Layer])
