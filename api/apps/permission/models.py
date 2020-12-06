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
