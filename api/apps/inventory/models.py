from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class ItemVendor(BaseModelMixin):
	name = models.CharField(max_length=220, unique=True, null=False, blank=False)

	def __str__(self):
		return self.name


class ItemCategory(BaseModelMixin):
	name = models.CharField(max_length=220, unique=True, null=False, blank=False)
	venue = models.ForeignKey(
		'venue.Venue', related_name='item_categories', blank=True, null=True,
		on_delete=models.SET_NULL
	)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name', 'venue'),)


class ItemSubCategory(BaseModelMixin):
	category = models.ForeignKey(
		ItemCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories'
	)
	name = models.CharField(max_length=220)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('category', 'name'),)


class ItemType(BaseModelMixin):
	vendor = models.ForeignKey(
		ItemVendor, on_delete=models.SET_NULL, related_name='items', null=True
	)
	subcategory = models.ForeignKey(
		ItemSubCategory, on_delete=models.CASCADE, related_name="items", null=False
	)
	venue = models.ForeignKey(
		'venue.Venue', related_name='items', blank=False, null=False, on_delete=models.CASCADE
	)
	name = models.CharField(max_length=220, null=False, blank=False)
	description = models.TextField(null=True, blank=True)
	unit_buying_price = models.DecimalField(max_digits=13, blank=False, decimal_places=3, default=0)
	unit_selling_price = models.DecimalField(
		max_digits=13, blank=False, decimal_places=3, default=0
	)
	barcode = models.CharField(max_length=50, null=True, blank=True)
	total_qty = models.IntegerField(null=False, blank=False, default=0)
	available_qty = models.IntegerField(null=False, blank=False, default=0)
	latest_qty = models.IntegerField(null=False, blank=False, default=0)
	image_url = models.CharField(max_length=200, null=True, blank=True)

	is_wire_type = models.BooleanField(default=False, null=True)
	is_available = models.BooleanField(default=True, null=True)
	color = models.CharField(max_length=200, null=True, blank=True)
	total_length = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3, help_text="Length of wire in metres"
	)
	latest_length = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3,
		help_text="New Length of wire in metres"
	)
	available_length = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3,
		help_text="New Length of wire in metres"
	)
	unit_buying_price_per_meter = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3, default=0
	)
	unit_selling_price_per_meter = models.DecimalField(
		max_digits=13, null=True, blank=True, decimal_places=3, default=0
	)

	def __str__(self):
		return '%s - %s' % (self.subcategory, self.name)

	class Meta:
		unique_together = (('name', 'subcategory', 'vendor', 'venue'),)
