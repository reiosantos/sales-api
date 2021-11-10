from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.apps.user import views

app_name = 'api.apps.user'

router = DefaultRouter()

urlpatterns = [
	path('', views.CreateUserView.as_view(), name='signup'),
	path('me/', views.CurrentUserView.as_view(), name='current'),
	path('activate/', views.ActivateUserView.as_view(), name='activate'),
	path('verify-exists/', views.UserExistView.as_view(), name='verify-user'),
	path('', include(router.urls)),
	path('<int:pk>/', views.RetrieveUserView.as_view({'get': 'retrieve'}), name='user-details'),
]
