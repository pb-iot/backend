from django.contrib import admin

from greenhouse_management.models import *


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'functionality')
    list_filter = ('functionality',)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'coordinates')
    search_fields = ("name",)


@admin.register(CustomUser)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('date_joined', 'is_staff', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(GreenHouse)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'display_location', 'display_authorized_users', 'display_owner')
    list_filter = ('crop_type', 'location__name', 'owner')
    search_fields = ('name',)

    def display_authorized_users(self, obj):
        return ', '.join(f'{user.first_name} {user.last_name}' for user in obj.authorized_users.all())

    def display_owner(self, obj):
        return f'{obj.owner.first_name} {obj.owner.last_name}'

    def display_location(self, obj):
        return obj.location.name

    display_authorized_users.short_description = 'Authorized users'
    display_owner.short_description = 'Owner'
    display_location.short_description = 'Location'


admin.site.site_title = "GreenHouse site admin"
admin.site.site_header = "GreenHouse administration"
admin.site.index_title = "Site administration"
