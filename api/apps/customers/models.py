from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class Customer(BaseModelMixin):
	ref = models.CharField(max_length=20, db_index=True, null=True, blank=True)
	name = models.CharField(max_length=120, null=False)
	email = models.EmailField(null=True, blank=True)
	contact = models.CharField(max_length=20, null=True, blank=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	venue = models.ForeignKey('venue.Venue', on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.name

	def generate_ref(self, prefix=None):
		super(Customer, self).generate_ref('CUS')
