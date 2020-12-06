from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def full_url(request, url):
	from api.apps.email.utils import site_url
	return site_url(request, static(url))


@register.simple_tag
def settings_value(name):
	return getattr(settings, name, "")
