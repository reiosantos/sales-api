import datetime
import logging

from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView, \
	UpdateAPIView
from rest_framework.response import Response

from api.apps.common.permission_utils import with_default_permission_classes
from api.apps.permission.permissions import IsVenueManager, IsSuperAdmin
from api.apps.venue.models import Venue, VenueSetting, VenueSettingValue
from api.apps.venue.serializers import VenueSettingValueSerializer, VenueSerializer

log = logging.getLogger(__name__)


class VenueSettingsView(UpdateAPIView, ListCreateAPIView):
	serializer_class = VenueSettingValueSerializer

	def get_queryset(self):
		venue = self.request.venue
		if not venue:
			raise ValidationError({'error': 'Invalid Venue'})

		if not self.request.method == 'GET' and (
			not self.request.user or not self.request.user.is_authenticated
		):
			raise NotAuthenticated(detail={'error': 'Not Authenticated'})

		return venue.setting_values.exclude(setting__var_define__isnull=True) \
			.select_related('setting')

	def list(self, request, *args, **kwargs):
		"""Add logo url"""

		queryset = self.get_queryset()
		serializer = self.get_serializer(queryset, many=True)
		data = serializer.data
		data += [{
			'path': 'venueName',
			'value': self.request.venue.name
		}, {
			'path': 'venueId',
			'value': self.request.venue.pk
		}, {
			'path': 'venueLocalTimeZone',
			'value': self.request.venue.local_timezone.zone
		}, {
			'path': 'venueLocalTimeZoneOffset',
			'value': datetime.datetime.now(self.request.venue.local_timezone).strftime('%z')
		}]
		return Response(data)


# @with_default_permission_classes()
class VenuesListView(ListAPIView):
	"""
	List all venues.
	"""
	permission_classes = [IsSuperAdmin]
	serializer_class = VenueSerializer
	queryset = Venue.objects.filter(active=True)


@with_default_permission_classes()
class VenueSettingsUpdateView(RetrieveUpdateAPIView):
	serializer_class = VenueSettingValueSerializer,
	permission_classes = [IsVenueManager]
	lookup_field = 'path'

	def get_object(self):
		try:
			setting = VenueSetting.objects.get(var_define=self.kwargs[self.lookup_field])
			obj = VenueSettingValue.objects.get_or_create(
				setting=setting, venue=self.request.venue)[0]
			self.check_object_permissions(self.request, obj)
			return obj
		except (TypeError, ValueError) as e:
			raise ValidationError({'error': e.message})

	def get_queryset(self):
		venue = self.request.venue
		if not venue:
			raise ValidationError({'error': 'Invalid venue'})
		return venue.setting_values.exclude(setting__var_define__isnull=True)
