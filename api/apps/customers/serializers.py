from rest_framework import serializers

from api.apps.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
	ref = serializers.CharField(read_only=True)

	class Meta:
		model = Customer
		fields = '__all__'
