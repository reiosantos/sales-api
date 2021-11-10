from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.apps.sales.models import ItemSale
from api.apps.sales.serializers import ItemSaleSerializer, EditItemSaleSerializer


class ItemSaleViewSet(ModelViewSet):

	def get_serializer_class(self):
		if self.request.method in ['PUT', 'PATCH']:
			return EditItemSaleSerializer
		return ItemSaleSerializer

	def get_queryset(self):
		venue = self.request.venue
		with_deleted = self.request.query_params.get('with_deleted', 'false')

		queryset = ItemSale.objects.filter(item__venue=venue)
		if with_deleted.lower() == 'true' and self.request.user.is_venue_manager(venue):
			return queryset
		return queryset.filter(~Q(deleted=True))

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		instance: ItemSale = self.get_object()

		instance.deleted = True
		instance.deletion_reason = request.data.get('reason')
		instance.save()

		return Response(status=status.HTTP_204_NO_CONTENT)
