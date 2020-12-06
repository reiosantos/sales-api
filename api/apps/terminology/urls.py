from django.urls import path

from api.apps.terminology import views

app_name = 'api.apps.terminology'

urlpatterns = [
	path('', views.TerminologyListView.as_view(), name='list'),
]
