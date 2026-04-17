from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .forms import NotificationFilterForm
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications_app/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        queryset = self.request.user.profile.notifications.select_related("actor", "room", "message")
        self.filter_form = NotificationFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            notification_type = self.filter_form.cleaned_data.get("notification_type")
            unread_only = self.filter_form.cleaned_data.get("unread_only")
            if notification_type:
                queryset = queryset.filter(notification_type=notification_type)
            if unread_only:
                queryset = queryset.filter(is_read=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unread_count"] = self.request.user.profile.notifications.filter(is_read=False).count()
        context["filter_form"] = self.filter_form
        return context


class NotificationMarkReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user.profile)
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return redirect("notification_list")


class NotificationMarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.profile.notifications.filter(is_read=False).update(is_read=True)
        return redirect("notification_list")
