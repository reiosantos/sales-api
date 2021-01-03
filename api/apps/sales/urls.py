from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.apps.sales import views

app_name = 'api.apps.sales'

router = SimpleRouter()
router.register('', views.ItemSaleViewSet, basename='crud')

urlpatterns = [
	path('', include(router.urls))
]
