import logging

from django.conf import settings
from django.core import signing
from django.core.signing import TimestampSigner
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.apps.email.utils import site_url, VerifyUserEmail
from api.apps.user import serializers
from api.apps.user.utils import user_exists_as_email, user_exists_as_mobile
from api.apps.venue.models import User, Venue

log = logging.getLogger('api')


class RetrieveUserView(RetrieveModelMixin, GenericViewSet):
	"""
	Info about the current User.
	"""
	queryset = User.objects.filter(is_active=True)
	serializer_class = serializers.UserSerializer


class CurrentUserView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
	"""
	Info about the current User.
	"""

	def get_serializer_class(self):
		if self.request.method in ['PATCH', 'PUT']:
			return serializers.EditUserSerializer

		return serializers.UserSerializer

	def get_object(self):
		return self.request.user

	@transaction.atomic
	def patch(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)

	@transaction.atomic
	def put(self, request, *args, **kwargs):
		return self.partial_update(request, *args, **kwargs)

	@transaction.atomic
	def delete(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.is_active = False
		instance.save()
		return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUserView(CreateAPIView):
	"""
	Create a User.
	"""
	permission_classes = [AllowAny]
	serializer_class = serializers.CreateUserSerializer

	@transaction.atomic
	def perform_create(self, serializer):
		venue: Venue = self.request.venue
		if not venue:
			raise ValidationError({"error": "Venue param is required to access this endpoint"})

		serializer.save()
		user: User = serializer.instance
		company = venue.company.id

		data = TimestampSigner().sign(signing.dumps({'user': user.id, company: company}))

		uri = 'dashboard/home?data={0}'.format(data)
		if (
			self.request.venue and
			self.request.venue.get_setting_value('DISABLE_EMAIL_VERIFICATION') and
			bool(int(self.request.venue.get_setting_value('DISABLE_EMAIL_VERIFICATION')))
		):
			uri = 'dashboard/home'

		link = site_url(self.request, uri)
		context = {
			'request': self.request,
			'to': user.email,
			'link': link
		}
		VerifyUserEmail(user, context).send()


class ActivateUserView(UpdateAPIView):
	"""
	Activate a User.
	{
		"user_id": "1" # gotten from the verifyEmail param from frontend link sent to first email
	}
	"""
	permission_classes = [AllowAny]
	serializer_class = serializers.ActivateUserSerializer

	def get_object(self):
		data = self.request.data.get('data')
		data = signing.loads(
			TimestampSigner().unsign(data, max_age=settings.PASSWORD_RESET_TIMEOUT))
		return User.objects.get(pk=data['user'])


class UserExistView(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		if self.request.GET.get('mobile', False):
			return Response(user_exists_as_mobile(self.request.GET.get('mobile')))
		elif self.request.GET.get('email', False):
			return Response(user_exists_as_email(self.request.GET.get('email')))

		return Response(False)
