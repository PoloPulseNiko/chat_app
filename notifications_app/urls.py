from django.urls import path

from .api_views import NotificationListAPIView
from .views import NotificationListView, NotificationMarkAllReadView, NotificationMarkReadView


urlpatterns = [
    path("", NotificationListView.as_view(), name="notification_list"),
    path("<int:pk>/read/", NotificationMarkReadView.as_view(), name="notification_mark_read"),
    path("read-all/", NotificationMarkAllReadView.as_view(), name="notification_mark_all_read"),
    path("api/", NotificationListAPIView.as_view(), name="api_notification_list"),
]
