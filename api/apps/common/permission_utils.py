from django.conf import settings
from django.utils.module_loading import import_string

message = 'You do not have required permission to perform this action'


def with_default_permission_classes():
	"""
	Decorator for classes to keep the default permissions classes while still appending new permissions
	using the permission_classes attribute
	"""

	def _decorator(cls):
		permission_classes = list(cls.permission_classes)

		perms = settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']
		perms = list(map(lambda x: import_string(x), perms))

		# insert at the beginning
		permission_classes[0:0] = perms

		cls.permission_classes = permission_classes

		return cls

	return _decorator
