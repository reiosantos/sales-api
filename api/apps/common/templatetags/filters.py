from django import template

from api.apps.terminology.models import Translation

register = template.Library()


@register.filter
def translate_for_venue(value, venue):
	return Translation.objects.value_for_venue(value, venue)


@register.filter
def format_short_time(datetime, venue):
	return datetime.strftime(venue.formatted_time)


@register.filter
def format_medium_date(datetime, venue):
	return datetime.strftime(venue.formatted_date)


@register.filter
def format_medium(datetime, venue):
	return datetime.strftime(venue.formatted_datetime)
