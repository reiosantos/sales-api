from django.contrib import admin

from api.apps.common.model_mixins import BaseModelAdminMixin
from api.apps.sales.models import ItemSale


@admin.register(ItemSale)
class ItemSaleAdmin(BaseModelAdminMixin):
	readonly_fields = ["ref"]
