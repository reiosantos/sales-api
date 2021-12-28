from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.apps.customers.models import Customer
from api.apps.customers.serializers import CustomerSerializer
from api.apps.inventory.models import ItemType
from api.apps.inventory.serializers import ItemTypeSerializer
from api.apps.sales.models import ItemSale
from api.apps.user.serializers import UserSerializer
from api.apps.venue.models import User


class ItemSaleSerializer(serializers.ModelSerializer):
	ref = serializers.CharField(read_only=True)
	item = serializers.PrimaryKeyRelatedField(queryset=ItemType.objects.all(), required=True)
	sold_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)
	unit_price = serializers.DecimalField(required=True, decimal_places=3, max_digits=13)
	quantity = serializers.IntegerField(required=True)
	sold_length = serializers.DecimalField(
		required=False, allow_null=True, decimal_places=3, max_digits=13,
		help_text="Length of wire sold")
	price_per_meter = serializers.DecimalField(
		required=False, allow_null=True, decimal_places=3, max_digits=13)

	item_detail = ItemTypeSerializer(source='item', read_only=True)
	customer_detail = CustomerSerializer(source='customer', read_only=True)
	sold_by_detail = UserSerializer(source='sold_by', read_only=True)

	def create(self, validated_data):
		sp = validated_data['item'].unit_selling_price
		if validated_data['unit_price'] < sp:
			raise ValidationError({
				"error": f"Selling price cannot be less than the minimum set price of {sp}"
			})

		available = validated_data['item'].available_qty

		err = f"Quantity is not available in stock. We only have {available} item(s) available, but you are invoicing {validated_data['quantity']} items"
		if validated_data['quantity'] > available:
			raise ValidationError({"error": err})

		with transaction.atomic():
			instance: ItemSale = super(ItemSaleSerializer, self).create(validated_data)
			item = instance.item
			item.available_qty -= instance.quantity
			item.save()

		return instance

	class Meta:
		model = ItemSale
		fields = '__all__'


class EditItemSaleSerializer(ItemSaleSerializer):
	item = serializers.PrimaryKeyRelatedField(queryset=ItemType.objects.all(), required=False)
	unit_price = serializers.DecimalField(required=False, decimal_places=3, max_digits=13)
	quantity = serializers.IntegerField(required=False)

	def update(self, instance, validated_data):

		item = validated_data.get('item', instance.item)
		unit_price = validated_data.get('unit_price')
		min_sell_price = item.unit_selling_price

		if unit_price and unit_price < min_sell_price:
			raise ValidationError({
				"error": f"Selling price cannot be less than the minimum set price of {min_sell_price}"
			})

		with transaction.atomic():
			if validated_data.get('quantity'):
				old_qty = instance.quantity

				item: ItemType = instance.item
				qty = item.available_qty
				qty += old_qty

				if qty < validated_data['quantity']:
					err = f"Quantity is not available in stock. We only have {qty} item(s) available, but you are invoicing {validated_data['quantity']} items"
					raise ValidationError({"error": err})

				qty -= validated_data['quantity']
				item.available_qty = qty
				item.save()

			return super(ItemSaleSerializer, self).update(instance, validated_data)
