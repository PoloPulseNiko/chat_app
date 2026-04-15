from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification


@login_required
def notification_list(request):
    notifications = request.user.profile.notifications.select_related("actor", "room", "message")
    unread_count = notifications.filter(is_read=False).count()
    return render(
        request,
        "notifications_app/notification_list.html",
        {"notifications": notifications, "unread_count": unread_count},
    )


@login_required
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user.profile)
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return redirect("notification_list")


@login_required
def notification_mark_all_read(request):
    request.user.profile.notifications.filter(is_read=False).update(is_read=True)
    return redirect("notification_list")

