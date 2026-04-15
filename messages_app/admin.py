from django.contrib import admin
from .models import Message, Reaction

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "room", "text", "created_at")
    list_filter = ("room", "created_at")
    search_fields = ("text",)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("profile", "message", "reaction_type", "created_at")
    list_filter = ("reaction_type", "created_at")
    search_fields = ("profile__nickname", "message__text")
