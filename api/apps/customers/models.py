from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class Customer(BaseModelMixin):
	name = models.CharField(max_length=120, null=False)
	email = models.EmailField(null=True)
	contact = models.CharField(max_length=20, null=True)
	address = models.CharField(max_length=200, null=True)
	venue = models.ForeignKey('venue.Venue', on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.name
