import json
import logging
import threading
import time
from functools import partial

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete
from django.forms import model_to_dict
from django.utils.deprecation import MiddlewareMixin

from api.apps.auditlogs.models import AuditLog
from api.apps.common.cc_json_encoder import CCJSONEncoder

thread_local = threading.local()
log = logging.getLogger('api')


class AuditlogMiddleware(MiddlewareMixin):
	"""
	Middleware to couple the request's user to log items. This is accomplished by currying the signal
	receiver with the user from the request (or None if the user is not authenticated).
	"""

	def process_request(self, request):
		"""
		Gets the current user from the request and prepares and connects a signal receiver with the
		user already attached to it.
		"""
		# Initialize thread local storage
		thread_local.auditlog = {
			'signal_uid': (self.__class__, time.time()),
			'remote_addr': request.META.get('REMOTE_ADDR'),
		}

		# In case of proxy, set 'original' address
		if request.META.get('HTTP_X_FORWARDED_FOR'):
			thread_local.auditlog['remote_addr'] = \
				request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]

		# Connect signal for automatic logging
		set_save_actor = partial(
			self.set_pre_actor,
			action='save',
			user=getattr(request, 'user', None),
			venue=getattr(request, 'venue', None),
			signal_uid=thread_local.auditlog['signal_uid']
		)
		set_delete_actor = partial(
			self.set_pre_actor,
			action='delete',
			user=getattr(request, 'user', None),
			venue=getattr(request, 'venue', None),
			signal_uid=thread_local.auditlog['signal_uid']
		)
		pre_save.connect(
			set_save_actor,
			sender=None,
			dispatch_uid=thread_local.auditlog['signal_uid'],
			weak=False
		)
		pre_delete.connect(
			set_delete_actor,
			sender=None,
			dispatch_uid=thread_local.auditlog['signal_uid'],
			weak=False
		)

	def process_response(self, request, response):
		""" Disconnects the signal receiver to prevent it from staying active. """
		if hasattr(thread_local, 'auditlog'):
			pre_save.disconnect(sender=None, dispatch_uid=thread_local.auditlog['signal_uid'])
		return response

	def process_exception(self, request, exception):
		"""
		Disconnects the signal receiver to prevent it from staying active in case of an exception.
		"""
		if hasattr(thread_local, 'auditlog'):
			pre_save.disconnect(sender=None, dispatch_uid=thread_local.auditlog['signal_uid'])

		return None

	@staticmethod
	def set_pre_actor(sender, instance, **kwargs):
		"""
		Signal receiver with an extra, required 'user' and 'venue' kwarg.
		This method becomes a real (valid) signal receiver when
		it is curried with the actor.
		"""
		if kwargs.get('signal_uid') != thread_local.auditlog['signal_uid']:
			return

		if hasattr(thread_local, 'auditlog'):
			kwargs['remote_addr'] = thread_local.auditlog['remote_addr']

		if ContentType.objects.get_for_model(sender).name == str(AuditLog._meta.verbose_name):
			# dont save audit log modifications, will create infinite loop
			return

		info = dict()
		obj = model_to_dict(instance)
		info['table_name'] = instance._meta.db_table
		info['table_pk'] = instance.pk
		info['action'] = kwargs.get('action')
		info['prev_entity'] = json.dumps(obj, cls=CCJSONEncoder)
		info['user'] = kwargs.get('user')
		info['venue'] = kwargs.get('venue')

		query_kwargs = dict()
		query_kwargs[instance._meta.pk.name] = info['table_pk']
		try:
			prev_instance = sender.objects.get(**query_kwargs)
			info['prev_entity'] = json.dumps(model_to_dict(prev_instance), cls=CCJSONEncoder)
		except ObjectDoesNotExist as e:
			log.info("Signals: creating new instance of " + str(sender))

		audit = AuditLog.objects.create(**info)
		audit.save()
