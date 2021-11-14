from django.contrib import admin

from .models import Permission, UserRole


class UserRoleAdmin(admin.ModelAdmin):
	list_display = list_display_links = ('role', 'venue', 'user')
	list_filter = ('venue', 'user')


admin.site.register(Permission)
admin.site.register(UserRole, UserRoleAdmin)
