from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.location.models import Village, Area, Region


class VillageInline(admin.StackedInline):
    model = Village
    extra = 1


class AreaInline(admin.StackedInline):
    model = Area
    extra = 1


class AreaModelAdmin(ImportExportModelAdmin):
    list_display = ['name', 'region', "is_active", 'id']
    list_filter = ["name", "is_active", 'region']
    list_editable = ['is_active']
    search_fields = ['name', "id"]

    inlines = [VillageInline]


class RegionModelAdmin(ImportExportModelAdmin):
    list_display = ['name', "is_active", 'id']
    list_filter = ["name", "is_active"]
    list_editable = ['is_active']
    search_fields = ['name', "id"]

    inlines = [AreaInline]


class VillageModelAdmin(ImportExportModelAdmin):
    list_display = ['name', "area", "is_active", 'id']
    list_filter = ["name", "area", "is_active"]
    list_editable = ['is_active']
    search_fields = ['name', "id"]


admin.site.register(Region, RegionModelAdmin)
admin.site.register(Area, AreaModelAdmin)
admin.site.register(Village, VillageModelAdmin)
