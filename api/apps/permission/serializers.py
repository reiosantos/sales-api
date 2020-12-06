from rest_framework import serializers

from api.apps.permission.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = ('permission_name',)
