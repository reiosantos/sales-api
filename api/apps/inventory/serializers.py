from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.apps.common import logger
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
	ref = serializers.CharField(read_only=True)
	vendor = serializers.PrimaryKeyRelatedField(
		queryset=ItemVendor.objects.all(), required=True
	)
	subcategory = serializers.PrimaryKeyRelatedField(
		queryset=ItemSubCategory.objects.all(), required=True
	)
	venue = serializers.PrimaryKeyRelatedField(read_only=True)
	name = serializers.CharField(required=True)
	description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
	unit_buying_price = serializers.DecimalField(required=True, decimal_places=3, max_digits=13)
	unit_selling_price = serializers.DecimalField(required=True, decimal_places=3, max_digits=13)
	barcode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	total_qty = serializers.IntegerField(required=False, read_only=True)
	available_qty = serializers.IntegerField(required=False, read_only=True)
	latest_qty = serializers.IntegerField(required=True)
	image_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)

	is_wire_type = serializers.BooleanField(allow_null=True, required=False, default=False)
	is_available = serializers.BooleanField(allow_null=True, required=False, default=True)
	color = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	total_length = serializers.DecimalField(
		required=False, read_only=True, decimal_places=3, max_digits=13)
	available_length = serializers.DecimalField(
		required=False, read_only=True, decimal_places=3, max_digits=13)
	latest_length = serializers.DecimalField(
		required=False, allow_null=True, decimal_places=3, max_digits=13)
	unit_selling_price_per_meter = serializers.DecimalField(
		required=False, allow_null=True, decimal_places=3, max_digits=13)

	vendor_detail = ItemVendorSerializer(source="vendor", read_only=True)
	category_detail = ItemCategorySerializer(source="subcategory.category", read_only=True)
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

		if not validated_data.get('total_length'):
			validated_data['total_length'] = validated_data['latest_length']

		if not validated_data.get('available_length'):
			validated_data['available_length'] = validated_data['latest_length']

		try:
			return super(ItemTypeSerializer, self).create(validated_data)
		except IntegrityError as e:
			logger.exception(e)
			raise IntegrityError(
				"This item already exists, you might want to update the existing record instead")

	def update(self, instance: ItemType, validated_data):
		if validated_data.get('latest_qty'):
			latest_qty = int(validated_data.get('latest_qty'))
			instance.latest_qty = latest_qty
			instance.total_qty += latest_qty
			instance.available_qty += latest_qty

		if validated_data.get('latest_length'):
			latest_len = float(validated_data.get('latest_length'))
			instance.latest_length = latest_len
			instance.total_length += latest_len
			instance.available_length += latest_len

		return super(ItemTypeSerializer, self).update(instance, validated_data)

	class Meta:
		model = ItemType
		fields = '__all__'
