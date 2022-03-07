from django.contrib import admin
from .models import Organization, Map, Layer, MapLayer


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    list_display = ['get_organization', 'map', 'layer', 'priority']
    list_filter = ['map']
    ordering = ['map', 'priority']

    @admin.display(ordering='author__organization')
    def get_organization(self, obj):
        return obj.map.organization


admin.site.register([Organization, Map, Layer])
