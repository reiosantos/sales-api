from rest_framework.viewsets import ModelViewSet

from api.apps.inventory.models import ItemVendor, ItemCategory, ItemSubCategory, ItemType
from api.apps.inventory.serializers import ItemVendorSerializer, ItemCategorySerializer, \
	ItemSubCategorySerializer, ItemTypeSerializer


class ItemVendorViewSet(ModelViewSet):
	serializer_class = ItemVendorSerializer
	queryset = ItemVendor.objects.all()


class ItemCategoryViewSet(ModelViewSet):
	serializer_class = ItemCategorySerializer

	def get_queryset(self):
		return ItemCategory.objects.filter(venue=self.request.venue)


class ItemSubCategoryViewSet(ModelViewSet):
	serializer_class = ItemSubCategorySerializer

	def get_queryset(self):
		return ItemSubCategory.objects.filter(category__venue=self.request.venue)


class ItemTypeViewSet(ModelViewSet):
	serializer_class = ItemTypeSerializer

	def get_queryset(self):
		return ItemType.objects.filter(venue=self.request.venue)
