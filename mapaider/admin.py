from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Organization, MapProject, Layer, MapLayer, MapFeature, MapLink


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['layer', 'map_project', 'priority', 'organization', 'contribution']
    list_filter = ['map_project', 'layer']
    list_editable = ['priority', 'contribution']
    ordering = ['map_project', 'priority']
    readonly_fields = ['uuid']

    @admin.display(ordering='map_project__organization', description='Organisation')
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


@admin.register(MapLink)
class MapLinkAdmin(admin.ModelAdmin):
    list_display = ['label', 'map_project', 'sort']
    actions_on_bottom = True
    list_editable = ['sort']
    search_fields = ['label']
    # readonly_fields = ['uuid']
    list_filter = ['map_project']
    date_hierarchy = 'created_at'
    ordering = ['map_project', 'sort']


admin.site.register([Organization, MapProject, Layer])
