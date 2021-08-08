from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Pledge, PledgeType


class PledgeTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    readonly_fields = ['id']
    list_display_links = ['id', 'name']


class PledgeAdmin(LeafletGeoAdmin):
    list_display = ['name', 'type', 'geom_type', 'get_acres', 'get_hectares', 'visibility', 'submitted_at']
    list_display_links = ['name']
    actions_on_bottom = True
    list_editable = ['visibility']
    search_fields = ['first_name', 'last_name']
    list_filter = ['type', 'geom_type', 'submitted_at']

    ordering = ['-submitted_at']

    sortable_by = ['name', 'type', 'geom_type', 'get_acres', 'get_hectares', 'submitted_at']

    # def get_list_display(self, request):
    #     # Define column list to show
    #     ld = ['uuid', 'name', 'type', 'geom_type', 'area', 'measurement_unit', 'get_acres']
    #
    #     if request.user.is_superuser:
    #         ld += ['created_at']
    #
    #     return ld

    def get_acres(self, rec):
        if rec.measurement_unit == 'ha':
            area = float(rec.area) * 2.47105381
        elif rec.measurement_unit == 'm2':
            area = float(rec.area) * 24710.5381
        else:
            area = rec.area

        return round(area, 4)

    get_acres.short_description = 'Acres'

    def get_hectares(self, rec):
        if rec.measurement_unit == 'acres':
            area = float(rec.area) / 2.47105381
        elif rec.measurement_unit == 'm2':
            area = float(rec.area) / 24710.5381
        else:
            area = rec.area

        return round(area, 5)

    get_hectares.short_description = 'Hectares'


admin.site.register(PledgeType, PledgeTypeAdmin)
admin.site.register(Pledge, PledgeAdmin)

admin.site.site_header = 'Global MapAid'
admin.site.site_title = 'GMA'
admin.site.index_title = 'Administration'
