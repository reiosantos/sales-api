from api.apps.permission.models import Permission
from api.apps.user.constants import VIEWER_TYPE_MANAGER
from api.apps.user.models import VenueViewerType
from api.apps.venue.models import Role


def make_user_venue_manager(user, venue):
	venue_manager, created = VenueViewerType.objects.get_or_create(
		venue=venue, role=Role.objects.get(name=VIEWER_TYPE_MANAGER)
	)

	if created:
		venue_manager.permissions = Permission.objects.all()

	venue_manager.users.add(user)
