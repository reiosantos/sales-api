from rest_framework import serializers

from api.apps.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
	ref = serializers.CharField(read_only=True)

	def validate(self, attrs):
		attrs = super(CustomerSerializer, self).validate(attrs)
		attrs['venue'] = self.context['request'].venue
		return attrs

	class Meta:
		model = Customer
		fields = '__all__'
