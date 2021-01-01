from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.apps.inventory import views

app_name = 'api.apps.inventory'

router = SimpleRouter()
router.register('vendors', views.ItemVendorViewSet, basename='vendors')
router.register('categories', views.ItemCategoryViewSet, basename='categories')
router.register('subcategories', views.ItemSubCategoryViewSet, basename='subcategories')
router.register('items', views.ItemTypeViewSet, basename='items')

urlpatterns = [
	path('', include(router.urls))
]
