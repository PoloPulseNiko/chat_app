from django.contrib import admin
from .models import DirectConversation, DirectMessage, Message, Reaction

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


@admin.register(DirectConversation)
class DirectConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    filter_horizontal = ("participants",)


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "conversation", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("sender__nickname", "text")
