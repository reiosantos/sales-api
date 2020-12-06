from django.db import models
from django.db.models import Q

from api.apps.common.model_mixins import BaseModelMixin
from api.apps.permission.models import Permission
from api.apps.user.constants import VIEWER_TYPE_DEFAULT
from api.apps.venue.models import Venue, User, Role


class DashboardSectionManager(models.Manager):
	def visible_to(self, user, venue):

		# Look for the user's 'special' viewer-types, e.g. venue-manager
		viewer_type_ids = user.viewer_types.filter(venue=venue).values_list('pk')

		# If there aren't any, then look for a 'default' viewer-type
		if not viewer_type_ids:
			viewer_type_ids = VenueViewerType.objects.filter(
				venue=venue,
				name=VIEWER_TYPE_DEFAULT
			).values_list('pk')

		# If there are viewer-type IDs, return the relevant dashboard sections
		if viewer_type_ids:
			return self.filter(viewer_types__in=viewer_type_ids).distinct()
		# Otherwise, return the dashboard sections which are visible to all
		else:
			return self.filter(is_visible_to_all=True)


class DashboardSection(BaseModelMixin):
	"""
	A section/page/route on the front-end dashboard.
	"""

	route_name = models.CharField(max_length=100)
	name = models.CharField(max_length=100, unique=True)
	is_visible_to_all = models.BooleanField(default=False)

	objects = DashboardSectionManager()

	def __str__(self):
		return self.name


class VenueViewerType(BaseModelMixin):
	"""
	Venues can set different viewer/user types, e.g. 'Booker', who can only
	use the dashboard for making bookings, or 'Venue Manager', who might be
	able to see all tabs in the dashboard.
	"""

	name = models.ForeignKey(Role, on_delete=models.CASCADE)
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	sections = models.ManyToManyField(DashboardSection, related_name='viewer_types')

	# The users that have this viewer-type
	users = models.ManyToManyField(User, related_name='viewer_types')

	# The permissions this viewer-type grants at its venue
	permissions = models.ManyToManyField(Permission)

	class Meta:
		unique_together = (('venue', 'name',),)

	def __str__(self):
		return '%s at %s' % (self.name, self.venue,)
