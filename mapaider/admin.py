from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Organization, Map, Layer, MapLayer, MapFeature, MapLink


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


@admin.register(Layer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'contribution']
    list_editable = ['contribution']


@admin.register(MapFeature)
class MapFeatureAdmin(LeafletGeoAdmin):
    list_display = ['name', 'layer', 'geom_type', 'visibility']
    actions_on_bottom = True
    list_editable = ['visibility']
    search_fields = ['name']
    readonly_fields = ['uuid', 'geom_type']
    list_filter = ['layer', 'geom_type', 'visibility', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    settings_overrides = {
        'MIN_ZOOM': 3,
        'MAX_ZOOM': 19,
    }

    # def get_readonly_fields(self, request, obj=None):
    #     if obj: # editing an existing object
    #         return self.readonly_fields + ['latitude', 'longitude']
    #     return self.readonly_fields


@admin.register(MapLink)
class MapLinkAdmin(admin.ModelAdmin):
    list_display = ['label', 'map', 'sort']
    actions_on_bottom = True
    list_editable = ['sort']
    search_fields = ['label']
    # readonly_fields = ['uuid']
    list_filter = ['map']
    date_hierarchy = 'created_at'
    ordering = ['map', 'sort']


admin.site.register([Organization, Map])
