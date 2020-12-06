from django.contrib import admin

from api.apps.user.models import DashboardSection, VenueViewerType

admin.site.register(DashboardSection)
admin.site.register(VenueViewerType)
