import logging

import six
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

log = logging.getLogger(__name__)


class CCJSONEncoder(DjangoJSONEncoder):
	def default(self, o):
		if isinstance(o, Model):
			return '{} - {}'.format(o.pk, str(o))

		try:
			return super(CCJSONEncoder, self).default(o)
		except Exception as e:
			log.error(str(e))
			return six.text_type(o)
