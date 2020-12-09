from django.db import models
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class BaseModelMixin(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
	modified_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		abstract = True


class RetrieveUpdateDestroyViewSet(
	mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
	"""
	A viewset that provides `retrieve()`, `update()`, `partial_update()`, `destroy()` actions.
	"""
	pass
