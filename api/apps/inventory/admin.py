from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from api.apps.inventory.models import ItemVendor, ItemCategory, ItemSubCategory, ItemType


class ItemTypeAdmin(admin.ModelAdmin):
	list_display = list_display_links = ('name',)
	list_filter = ('subcategory', 'vendor', 'name', 'barcode')


class ItemSubcategoryInline(admin.TabularInline):
	model = ItemSubCategory


class ItemCategoryAdmin(ImportExportModelAdmin):
	search_fields = ('name', 'venue')
	list_display = ('name', 'venue')
	inlines = [ItemSubcategoryInline]


admin.site.register(ItemVendor)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(ItemSubCategory)
admin.site.register(ItemType, ItemTypeAdmin)
