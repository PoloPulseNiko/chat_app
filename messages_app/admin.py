from django.contrib import admin
from .models import Message

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "room", "text", "created_at")
    list_filter = ("room", "created_at")
    search_fields = ("text",)