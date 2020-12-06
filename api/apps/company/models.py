from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class Company(BaseModelMixin):
	name = models.CharField(max_length=45, blank=False, null=False)
	active = models.IntegerField(blank=False, null=False, default=True)
	address1 = models.CharField(max_length=100, blank=True, null=True)
	address2 = models.CharField(max_length=100, blank=True, null=True)
	postcode = models.CharField(max_length=45, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	country = models.CharField(max_length=100, blank=False, null=False, default='Uganda')
	deleted = models.BooleanField(default=False)

	@property
	def venues_count(self):
		return self.venues.count()

	def __str__(self):
		return str(self.name)
