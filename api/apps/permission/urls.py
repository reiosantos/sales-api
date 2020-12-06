from django.urls import path

from api.apps.permission import views

app_name = 'api.apps.permission'

urlpatterns = [
	path('', views.PermissionListView.as_view(), name='list'),
]
