from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ChatUser


@admin.register(ChatUser)
class ChatUserAdmin(UserAdmin):
    list_display = ("username", "email", "display_name", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Chat details", {"fields": ("display_name",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Chat details", {"fields": ("email", "display_name")}),
    )

