from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Pledge, PledgeType


class PledgeTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    readonly_fields = ['id']
    list_display_links = ['id', 'name']


class PledgeAdmin(LeafletGeoAdmin):
    list_display = ['uuid', 'name', 'type', 'geom_type', 'area', 'measurement_unit', 'get_acres', 'created_at']
    list_display_links = ['uuid', 'name']
    actions_on_bottom = True
    # list_editable = ['type']
    search_fields = ['first_name', 'last_name']
    list_filter = ['type', 'geom_type']

    ordering = ['-created_at']

    sortable_by = ['uuid', 'name', 'type', 'geom_type', 'area', 'measurement_unit', 'get_acres', 'created_at']

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
            return float(rec.area) / 2.47105381
        elif rec.measurement_unit == 'm2':
            return float(rec.area) / 24710.5381
        else:
            return rec.area

    get_acres.short_description = 'Area (Acres)'


admin.site.register(PledgeType, PledgeTypeAdmin)
admin.site.register(Pledge, PledgeAdmin)

admin.site.site_header = 'Global MapAid'
admin.site.site_title = 'Main'
admin.site.index_title = 'Administration'
