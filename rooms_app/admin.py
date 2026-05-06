from django.contrib import admin
from .models import Category, Membership, Room, Tag

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "creator", "visibility", "posting_policy")
    list_filter = ("category", "visibility", "posting_policy")
    search_fields = ("name",)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("profile", "room", "role", "joined_at")
    list_filter = ("role", "joined_at")
    search_fields = ("profile__nickname", "room__name")
