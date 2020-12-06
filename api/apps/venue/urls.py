from django.urls import path, re_path

from api.apps.venue import views

app_name = 'api.apps.venue'

urlpatterns = [
	path('', views.VenuesListView.as_view(), name="list"),
	path('settings/', views.VenueSettingsView.as_view(), name="settings"),
	re_path(r'settings/(?P<path>[\w-]+)/', views.VenueSettingsUpdateView.as_view(), name="setting")
]
