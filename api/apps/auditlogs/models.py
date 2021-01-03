from django.db import models

from api.apps.common.model_mixins import BaseModelMixin


class AuditLog(BaseModelMixin):
	table_name = models.CharField(max_length=100, blank=False, null=False)
	table_pk = models.CharField(max_length=100, blank=True, null=True)
	action = models.CharField(max_length=100, blank=False, null=False)
	description = models.TextField(blank=True, null=True)
	prev_entity = models.JSONField(blank=True, null=True)
	new_entity = models.JSONField(blank=True, null=True)
	user = models.ForeignKey(
		'venue.User', blank=True, null=True, on_delete=models.SET_NULL, related_name='auditlogs'
	)
	venue = models.ForeignKey(
		'venue.Venue', blank=True, null=True, on_delete=models.SET_NULL, related_name='auditlogs'
	)
