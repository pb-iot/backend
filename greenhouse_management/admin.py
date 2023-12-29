from django.contrib import admin

from greenhouse_management.models import *


class GreenHouseInline(admin.TabularInline):
    model = GreenHouse
    fields = ('name', 'crop_type', 'display_authorized_users', 'display_owner')

    readonly_fields = ('name', 'crop_type', 'display_authorized_users', 'display_owner')
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = True

    def display_authorized_users(self, obj):
        return ', '.join(f'{user.first_name} {user.last_name}' for user in obj.authorized_users.all())

    def display_owner(self, obj):
        return f'{obj.owner.first_name} {obj.owner.last_name}'

    display_authorized_users.short_description = 'Authorized users'
    display_owner.short_description = 'Owner'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'functionality')
    list_filter = ('functionality',)
    search_fields = ("name",)

    class Meta:
        ordering = ('name', 'functionality')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'coordinates')
    search_fields = ("name",)
    inlines = [GreenHouseInline]

    class Meta:
        ordering = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active')
    list_filter = ('date_joined', 'is_staff', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('date_joined', 'last_login')
    exclude = ('password',)

    class Meta:
        ordering = ('first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active')


@admin.register(GreenHouse)
class GreenHouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'location', 'display_authorized_users', 'display_owner')
    list_filter = ('crop_type', 'location__name', 'owner')
    search_fields = ('name',)

    class Meta:
        ordering = ('name', 'crop_type', 'location', 'display_owner')

    def display_authorized_users(self, obj):
        return ', '.join(f'{user.first_name} {user.last_name}' for user in obj.authorized_users.all())

    def display_owner(self, obj):
        return f'{obj.owner.first_name} {obj.owner.last_name}'

    display_authorized_users.short_description = 'Authorized users'
    display_owner.short_description = 'Owner'


admin.site.site_title = "GreenHouse site admin"
admin.site.site_header = "GreenHouse administration"
admin.site.index_title = "Site administration"
