from rest_framework import permissions
from rest_framework.exceptions import ValidationError, NotAuthenticated

from api.apps.venue.models import User


def validate_perm(request):
	if not request.venue:
		raise ValidationError({'error': 'Venue Not Found'})

	user = request.user
	if not isinstance(user, User) or not user.is_authenticated:
		raise NotAuthenticated({'error': 'Authentication credentials were not provided.'})

	return user


class IsSuperAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		user = validate_perm(request)
		return user.is_superuser


class IsVenueManager(permissions.BasePermission):
	def has_permission(self, request, view):
		user = validate_perm(request)
		return user.is_venue_manager(request.venue)


class IsVenueManagerOrReadOnly(IsVenueManager):
	"""
	Allows only venue managers to access the resource otherwise only allow get
	requests to other users
	"""

	def has_permission(self, request, view):
		user = validate_perm(request)
		restricted_methods = ['POST', 'PUT', 'DELETE', 'PATCH']

		if request.method == 'GET':
			return True
		elif request.method in restricted_methods and user.is_venue_manager(request.venue):
			return True

		return None


class IsVenueAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		user = validate_perm(request)
		return user.is_venue_admin(request.venue)


class IsVenueStaff(permissions.BasePermission):
	def has_permission(self, request, view):
		user = validate_perm(request)
		return user.is_staff(request.venue)


class AllowGetOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		# allow all GET requests
		if request.method == 'GET':
			return True

		# Otherwise, only allow authenticated requests
		return request.user and request.user.is_authenticated
