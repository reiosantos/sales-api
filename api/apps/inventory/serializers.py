from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.apps.inventory.models import ItemVendor, ItemCategory, ItemSubCategory, ItemType
from api.apps.venue.models import Venue


class ItemVendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = ItemVendor
		fields = '__all__'


class ItemSubCategorySerializer(serializers.ModelSerializer):
	name = serializers.CharField(required=True)
	category = serializers.PrimaryKeyRelatedField(
		queryset=ItemCategory.objects.all(), default=None, required=False)
	category_name = serializers.CharField(source="category.name", required=False, read_only=True)

	class Meta:
		model = ItemSubCategory
		fields = ['id', 'name', 'created_at', 'modified_at', 'category', 'category_name']


class ItemCategorySerializer(serializers.ModelSerializer):
	name = serializers.CharField(required=True)
	venue = serializers.PrimaryKeyRelatedField(read_only=True)
	subcategories = ItemSubCategorySerializer(many=True, read_only=True)

	def create(self, validated_data):
		validated_data['venue'] = self.context['request'].venue
		return super(ItemCategorySerializer, self).create(validated_data)

	class Meta:
		model = ItemCategory
		fields = ['id', 'venue', 'name', 'created_at', 'modified_at', 'subcategories']


class ItemTypeSerializer(serializers.ModelSerializer):
	vendor = serializers.PrimaryKeyRelatedField(
		queryset=ItemVendor.objects.all(), required=True
	)
	subcategory = serializers.PrimaryKeyRelatedField(
		queryset=ItemSubCategory.objects.all(), required=True
	)
	venue = serializers.PrimaryKeyRelatedField(read_only=True)
	name = serializers.CharField(required=True)
	description = serializers.CharField(required=False)
	unit_buying_price = serializers.DecimalField(required=True, decimal_places=3, max_digits=13)
	unit_selling_price = serializers.DecimalField(required=True, decimal_places=3, max_digits=13)
	barcode = serializers.CharField(required=False)
	total_qty = serializers.IntegerField(required=False, read_only=True)
	available_qty = serializers.IntegerField(required=False, read_only=True)
	latest_qty = serializers.IntegerField(required=True)
	image_url = serializers.CharField(required=False)

	vendor_detail = ItemVendorSerializer(source="vendor", read_only=True)
	category_detail = ItemSubCategorySerializer(source="subcategory.category", read_only=True)
	subcategory_detail = ItemSubCategorySerializer(source="subcategory", read_only=True)

	def validate(self, attrs):
		attrs = super(ItemTypeSerializer, self).validate(attrs)
		venue: Venue = self.context['request'].venue
		attrs['venue'] = venue

		try:
			if venue and (attrs['unit_selling_price'] or attrs['unit_buying_price']):
				setting = venue.get_setting_value('ALLOW_SELLING_PRICE_BELOW_BUYING_PRICE')
				if not setting or not bool(int(setting)):
					if attrs['unit_selling_price'] < attrs['unit_buying_price']:
						raise ValidationError(
							{"error": "Selling price cannot be less than Buying price"})
		except KeyError:
			raise ValidationError(
					{"error": "Both Selling price and Buying price are required"})

		return attrs

	def create(self, validated_data):
		if not validated_data.get('total_qty'):
			validated_data['total_qty'] = validated_data['latest_qty']

		if not validated_data.get('available_qty'):
			validated_data['available_qty'] = validated_data['latest_qty']

		return super(ItemTypeSerializer, self).create(validated_data)

	def update(self, instance: ItemType, validated_data):
		if validated_data.get('latest_qty'):
			latest_qty = int(validated_data.get('latest_qty'))
			instance.latest_qty = latest_qty
			instance.total_qty += latest_qty
			instance.available_qty += latest_qty

		return super(ItemTypeSerializer, self).update(instance, validated_data)

	class Meta:
		model = ItemType
		fields = '__all__'
