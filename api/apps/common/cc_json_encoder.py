from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model


class CCJSONEncoder(DjangoJSONEncoder):
	def default(self, o):
		if isinstance(o, Model):
			return '{} - {}'.format(o.pk, str(o))

		return super(CCJSONEncoder, self).default(o)
