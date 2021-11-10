from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from api.apps.venue.models import Venue, VenueSettingValue, User, UserData, \
	UsersVenues, VenueSetting


class VenueSettingValueInline(admin.TabularInline):
	model = VenueSettingValue


class VenueAdmin(ImportExportModelAdmin):
	search_fields = ('name',)
	list_display = ('name', 'url_component', 'address',)
	inlines = [VenueSettingValueInline]


class UserAdmin(admin.ModelAdmin):
	search_fields = ('email',)
	list_display = ('email',)
	fields = ('email', 'is_active', 'is_admin', 'date_joined', 'last_login',)
	readonly_fields = ('date_joined', 'last_login', 'created_at', 'modified_at')


admin.site.register(Venue, VenueAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserData)
admin.site.register(UsersVenues)
admin.site.register(VenueSetting)
admin.site.register(VenueSettingValue)
