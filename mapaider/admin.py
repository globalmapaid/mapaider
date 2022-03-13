from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Organization, Map, Layer, MapLayer, MapFeature


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['layer', 'map', 'priority', 'organization', 'contribution']
    list_filter = ['map', 'layer']
    list_editable = ['priority', 'contribution']
    ordering = ['map', 'priority']
    readonly_fields = ['uuid']

    @admin.display(ordering='map__organization', description='Organisation')
    def organization(self, obj):
        return obj.map.organization


@admin.register(MapFeature)
class MapFeatureAdmin(LeafletGeoAdmin):
    list_display = ['name', 'layer', 'geom_type', 'visibility']
    actions_on_bottom = True
    list_editable = ['visibility']
    search_fields = ['name']
    readonly_fields = ['uuid', 'geom_type', 'latitude', 'longitude']
    list_filter = ['layer', 'geom_type', 'visibility', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    settings_overrides = {
        'MIN_ZOOM': 3,
        'MAX_ZOOM': 19,
    }


admin.site.register([Organization, Map, Layer])
