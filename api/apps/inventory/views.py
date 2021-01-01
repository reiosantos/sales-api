from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.apps.inventory.models import ItemVendor, ItemCategory, ItemSubCategory, ItemType
from api.apps.inventory.serializers import ItemVendorSerializer, ItemCategorySerializer, \
	ItemSubCategorySerializer, ItemTypeSerializer
from api.apps.permission.permissions import IsVenueManagerOrReadOnly


class ItemVendorViewSet(ModelViewSet):
	serializer_class = ItemVendorSerializer
	queryset = ItemVendor.objects.all()
	permission_classes = [IsAuthenticated, IsVenueManagerOrReadOnly]


class ItemCategoryViewSet(ModelViewSet):
	serializer_class = ItemCategorySerializer
	queryset = ItemCategory.objects.all()
	permission_classes = [IsAuthenticated, IsVenueManagerOrReadOnly]


class ItemSubCategoryViewSet(ModelViewSet):
	serializer_class = ItemSubCategorySerializer
	queryset = ItemSubCategory.objects.all()
	permission_classes = [IsAuthenticated, IsVenueManagerOrReadOnly]


class ItemTypeViewSet(ModelViewSet):
	serializer_class = ItemTypeSerializer
	queryset = ItemType.objects.all()
	permission_classes = [IsAuthenticated, IsVenueManagerOrReadOnly]
