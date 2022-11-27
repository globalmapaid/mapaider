from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Organization, Map, Layer, MapLayer, MapFeature, MapLink, Membership


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'is_active']
    list_filter = ['organization', 'is_active']


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
class LayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'extra_fields', 'contribution']
    list_editable = ['contribution']

    @admin.display(description='Data Fields')
    def extra_fields(self, obj):
        return len(obj.field_set)


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

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['organization', 'user', 'role']
    list_filter = ['organization']
    search_fields = ['user']

admin.site.register([Organization])
