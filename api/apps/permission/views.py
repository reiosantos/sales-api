from rest_framework.generics import ListAPIView

from api.apps.common.permission_utils import with_default_permission_classes
from api.apps.permission.models import Permission
from api.apps.permission.permissions import ManagementPermissions
from api.apps.permission.serializers import PermissionSerializer


@with_default_permission_classes()
class PermissionListView(ListAPIView):
	serializer_class = PermissionSerializer
	permission_classes = (ManagementPermissions,)
	queryset = Permission.objects.all()
