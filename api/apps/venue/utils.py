from django.utils.http import urlencode

from api.apps.venue.models import VenueSetting
from api.apps.venue.models import VenueSettingValue


def _add_venue_url_component(url, venue_url_component):
	"""URL with ?venue= query parameter"""
	return '%s?%s' % (url, urlencode({'venue': venue_url_component}))


def add_venue_to_url(url, venue):
	"""URL with ?venue= query parameter"""
	return _add_venue_url_component(url, venue.url_component)


def venue_has_setting(venue, venue_settings_string):
	try:
		setting = VenueSetting.objects.get(var_define=venue_settings_string)
		VenueSettingValue.objects.get(setting=setting, venue=venue)
		return True
	except VenueSettingValue.DoesNotExist:
		return False
