from django.contrib import admin

from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'is_active']
    readonly_fields = ['id']
    list_display_links = ['id', 'name']
    ordering = ['id']
    sortable_by = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
