from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.apps.customers import views

app_name = 'api.apps.customers'

router = SimpleRouter()
router.register('', views.CustomerViewSet, basename='customers')

urlpatterns = [
	path('', include(router.urls))
]
