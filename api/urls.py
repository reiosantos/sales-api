"""
sales_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
	Function views
		1. Add an import:  from my_app import views
		2. Add a URL to urlpatterns:  path('', views.home, name='home')
	Class-based views
		1. Add an import: from other_app.views import Home
		2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
	Including another URLconf
		1. Import the include() function: from django.urls import include, path
		2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import VerifyJSONWebToken, ObtainJSONWebToken

from api.apps.common.views import HealthCheckView

schema_view = get_schema_view(
	openapi.Info(
		title='{} API'.format(settings.APP_NAME),
		default_version='v1',
		description='The Official API documentation for the {}'.format(settings.APP_NAME),
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email=settings.DEFAULT_SUPPORT_EMAIL),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(AllowAny,)
)

urlpatterns = [
	re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
			name='schema-json'),
	path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	path('auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('accounts/', include('django.contrib.auth.urls')),
	path('jwt/login/', ObtainJSONWebToken.as_view()),
	path('jwt/verify/', VerifyJSONWebToken.as_view(), name='verify'),
	path('health/', HealthCheckView.as_view({'get': 'get'}), name='health_check'),
	path('admin/', admin.site.urls),
	path('permissions/', include('api.apps.permission.urls', namespace='permissions')),
	path('users/', include('api.apps.user.urls', namespace='users')),
	path('venues/', include('api.apps.venue.urls', namespace='venues')),
]

if 'silk' in settings.INSTALLED_APPS:
	urlpatterns += [
		path('silk/', include('silk.urls', namespace='silk'))
	]

# Add 'prefix' to all urlpatterns (except static files)
if settings.URL_PREFIX:
	urlpatterns = [
		path(settings.URL_PREFIX, include(urlpatterns))
	]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
	path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT})
]
