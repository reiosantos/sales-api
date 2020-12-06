from django.apps import apps
from rest_framework import exceptions
from rest_framework_jwt.utils import jwt_decode_handler


def custom_jwt_decode_handler(token):
	"""
	Check if decoded payload have the same id
	and email from the database
	"""

	payload = jwt_decode_handler(token)
	user_id = payload['user_id']
	email = payload['email']

	user_model = apps.get_model(app_label='venue', model_name='User')

	try:
		user = user_model.objects.get(pk=user_id)

		if user.email != email:
			raise exceptions.AuthenticationFailed()
	except user_model.DoesNotExist:
		raise exceptions.AuthenticationFailed()
	return payload
