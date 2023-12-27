from django.contrib import admin

from greenhouse_management.models import *


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'functionality')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'coordinates')


@admin.register(CustomUser)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active')


@admin.register(GreenHouse)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'display_location', 'display_authorized_users', 'display_owner')

    def display_authorized_users(self, obj):
        return ', '.join(f'{user.first_name} {user.last_name}' for user in obj.authorized_users.all())

    def display_owner(self, obj):
        return f'{obj.owner.first_name} {obj.owner.last_name}'

    def display_location(self, obj):
        return obj.name

    display_authorized_users.short_description = 'Authorized users'
    display_owner.short_description = 'Owner'
    display_location.short_description = 'Location'
