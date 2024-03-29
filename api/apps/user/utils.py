from api.apps.common.camel_case.util import camel_to_underscore
from api.apps.common.util import CustomTemplate
from api.apps.venue.models import UsersVenues, UserData, User


def ensure_user_associated_with_venue(user, venue):
	"""
	Checks whether the user is associated with the venue, and if not,
	associates the user with the venue.
	"""
	UsersVenues.objects.get_or_create(user=user, venue=venue)


def user_exists_as_email(email):
	"""
	return true if email exists in this server
	"""
	return User.objects.filter(email=email).exists()


def user_exists_as_mobile(mobile):
	"""
	return if user exist in this server
	"""
	return UserData.objects.filter(mobile=mobile).exists()


def filter_order_by(request, sqs):
	# Ordering
	order_by = request.GET.get('order')
	if order_by:
		# Strip off initial '+'
		if order_by.startswith('+'):
			order_by = order_by[1:]
		# Field name can arrive in camelCase
		order_by = camel_to_underscore(order_by)
		sqs = sqs.order_by(order_by)
	return sqs


class UserCustomTemplate(CustomTemplate):
	"""
	UserCustomTemplate with booking map fields
	"""
	template_fields = {
		'EMAIL': 'email',
		'FIRST_NAME': 'profile.first_name',
		'LAST_NAME': 'profile.last_name',
		'FULL_NAME': 'full_name',
		'MOBILE': 'profile.mobile',
		'ADDRESS1': 'profile.address1',
		'ADDRESS2': 'profile.address2',
		'CITY': 'profile.city',
		'COUNTRY': 'profile.country'
	}
	time_fields = []
	date_fields = []
