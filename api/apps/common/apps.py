from django.apps import AppConfig


class CommonConfig(AppConfig):
	name = 'api.apps.common'

	def ready(self):
		# noinspection PyUnresolvedReferences
		import api.apps.common.signals
