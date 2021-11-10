from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class Permission(BaseModelMixin):
	PERMISSION_READ = 'read'
	PERMISSION_REPORT = 'report'
	PERMISSION_DELETE = 'delete'
	PERMISSION_EDIT = 'edit'
	PERMISSION_SMS = 'sms'
	PERMISSION_PAYMENT = 'payment'
	PERMISSION_DEPOSIT = 'deposit'
	PERMISSION_REFUND = 'refund'

	permission_name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.permission_name


class Role(BaseModelMixin):
	ADMIN = "Admin"
	MANAGER = "Manager"
	STAFF = "Staff"
	DEFAULT = "Default"

	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class UserRole(BaseModelMixin):
	name = models.ForeignKey(Role, on_delete=models.CASCADE)
	user = models.ForeignKey('venue.User', on_delete=models.CASCADE, related_name='roles')
	venue = models.ForeignKey('venue.Venue', on_delete=models.CASCADE, related_name='roles')

	def __str__(self):
		return "{}-{}-{}".format(self.venue.name, self.user.email, self.name)

	class Meta:
		unique_together = (('user', 'venue'),)
