from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "actor", "notification_type", "target_preview", "is_read", "created_at")
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("recipient__nickname", "actor__nickname", "text")

    @admin.display(description="Target")
    def target_preview(self, obj):
        if obj.direct_message_id:
            return f"Direct message #{obj.direct_message_id}"
        if obj.message_id:
            return f"Room message #{obj.message_id}"
        if obj.room_id:
            return f"Room #{obj.room_id}"
        return "-"
