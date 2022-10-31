from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class DriverAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("avatar_file",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("avatar",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("first_name", "last_name", "avatar",)}),)
    )
