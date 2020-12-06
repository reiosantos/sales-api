import collections
import logging
import re

from django.template import Template, Context

logger = logging.getLogger(__name__)


def validate_date_range_venue(value: str):
	date_range = value.split(',')
	if len(date_range) != 2:
		return False
	else:
		try:
			from_date = int(date_range[0])
			to_date = int(date_range[1])
			if from_date > to_date:
				return False
		except Exception as e:
			logger.error("Error: %s" % e)
			return False
	return True


def convert_to_python_date_string_format(string: str) -> str:
	"""Converts angular/php date time string format to python string format"""

	values = collections.OrderedDict([
		('yyyy', '%Y'),
		('yy', '%y'),
		('MMMM', '%B'),
		('MMM', '%b'),
		('MM', '%m'),
		('dd', '%d'),
		('HH', '%H'),
		('hh', '%I'),
		('h', '%I'),
		('a', '%p'),
		('mm', '%M'),
		('ss', '%S'),
		('EEEE', '%A'),
		('EEE', '%a'),
		('ww', '%W'),
		('Z', '%z'),
	])

	for word, initial in values.items():
		src_str = re.compile(word)
		string = src_str.sub(initial, string)

	return string


def getattr_model_nested(instance, field):
	"""
	Get nested model field by dotted string, exmaple: 'user.first_name'
	"""

	def get_repr(value):
		if callable(value):
			return '%s' % value()
		return value

	def get_f(_instance, _field):
		field_path = _field.split('.')
		attr = _instance
		for elem in field_path:
			try:
				attr = get_repr(getattr(attr, elem))
			except AttributeError:
				return None
		return attr

	return get_repr(get_f(instance, field))


class CustomTemplate:
	"""
	CustomTemplate class for templating <EXAMPLE> keys with instance values
	Examples for template string:
	Scheduled/Checked In: <SCHEDULED_TIME_IN>/<ARRIVED_AT>
		Date: <DATE>
		Declare template map fields `template_booking_fields`
		TAG FIELD: instance field
		Example:
			{
			'BOOKING_REF': 'ref',
			'ACCESS_POINT': 'booking_vehicle.access_point_name'
			}
	Declare time fields `time_fields`, keys from `template_booking_fields` mapper
	It will be converted to venue format time
	Declare date fields `date_fields`, keys from `template_booking_fields` mapper
	It will be converted to venue format date
	"""

	template_fields = {}
	time_fields = []
	date_fields = []

	def __init__(self, instance):
		self.instance = instance

	def render(self, string, autoescape=True):
		"""
		Render template with real data values
		"""
		if not string:
			return string

		string = self.replace_chars(string)

		context = {}
		for key in self.template_fields:
			context[key] = self.get_key_value(key)

		return Template(string).render(context=Context(context, autoescape=autoescape))

	def get_key_value(self, key):
		"""
		Get value for key with formatting
		"""

		value = getattr_model_nested(self.instance, self.template_fields[key])

		if value:
			if key in self.time_fields:
				value = value.strftime(self.instance.venue.formatted_time)
			elif key in self.date_fields:
				value = value.strftime(self.instance.venue.formatted_date)

		return value

	def replace_chars(self, string):
		string = string.replace('<%', '{{')
		string = string.replace('%>', '}}')
		return string
