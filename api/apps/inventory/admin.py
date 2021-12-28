from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from api.apps.common.model_mixins import BaseModelAdminMixin
from api.apps.inventory.models import ItemVendor, ItemCategory, ItemSubCategory, ItemType


class ItemTypeAdmin(BaseModelAdminMixin):
	list_display = list_display_links = ('ref', 'name',)
	list_filter = ('ref', 'subcategory', 'vendor', 'name', 'barcode')
	readonly_fields = ["ref"]


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
