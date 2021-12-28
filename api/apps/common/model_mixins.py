from django.contrib import admin
from django.db import models
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class BaseModelMixin(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
	modified_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		abstract = True

	def __str__(self):
		if hasattr(self, 'ref') and getattr(self, 'ref', None):
			return self.ref
		if hasattr(self, 'name') and getattr(self, 'name', None):
			return self.name
		return super(BaseModelMixin, self).__str__()

	def generate_ref(self, prefix=None):
		"""
		Generate a (unique) property reference.
		Creates a reference of the form UG0000000001
		"""
		if hasattr(self, "ref") and not self.ref:
			if prefix is None:
				prefix = "PRX"
			self.ref = "{}{}{}".format(prefix, self.created_at.month, format(self.pk, '06d'))


class BaseModelAdminMixin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		if hasattr(obj, 'generate_ref'):
			obj.generate_ref()

		super(BaseModelAdminMixin, self).save_model(request, obj, form, change)


class RetrieveUpdateDestroyViewSet(
	mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
	"""
	A viewset that provides `retrieve()`, `update()`, `partial_update()`, `destroy()` actions.
	"""
	pass
