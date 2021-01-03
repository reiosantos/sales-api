from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from api.apps.customers.models import Customer
from api.apps.customers.serializers import CustomerSerializer


class CustomerViewSet(ModelViewSet):
	serializer_class = CustomerSerializer

	def get_queryset(self):
		return Customer.objects.filter(venue=self.request.venue)

	def destroy(self, request, *args, **kwargs):
		if not request.user.is_venue_manager(self.request.venue):
			raise PermissionDenied()
		return super(CustomerViewSet, self).destroy(request, *args, **kwargs)
