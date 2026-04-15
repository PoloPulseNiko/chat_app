from django.urls import path

from .views import notification_list, notification_mark_all_read, notification_mark_read


urlpatterns = [
    path("", notification_list, name="notification_list"),
    path("<int:pk>/read/", notification_mark_read, name="notification_mark_read"),
    path("read-all/", notification_mark_all_read, name="notification_mark_all_read"),
]

