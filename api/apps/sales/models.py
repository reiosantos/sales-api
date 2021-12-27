from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class ItemSale(BaseModelMixin):
	item = models.ForeignKey('inventory.ItemType', on_delete=models.CASCADE)
	sold_by = models.ForeignKey(
		'venue.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="items_sold")
	unit_price = models.DecimalField(max_digits=13, null=False, decimal_places=3, default=0)
	quantity = models.IntegerField(null=False, default=1)
	customer = models.ForeignKey('customers.Customer', null=True, on_delete=models.SET_NULL)
	deleted = models.BooleanField(null=True)
	deletion_reason = models.TextField(null=True)
	sold_length = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3,
		help_text="Length of wire sold in metres"
	)
	price_per_meter = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3,
		help_text="Price per meter of wire sold"
	)
