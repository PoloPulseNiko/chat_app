from django.urls import path

from .views import StaffBroadcastView, StaffDashboardView, StaffRoomAccessUpdateView


urlpatterns = [
    path("", StaffDashboardView.as_view(), name="staff_dashboard"),
    path("broadcast/", StaffBroadcastView.as_view(), name="staff_broadcast"),
    path("rooms/access/", StaffRoomAccessUpdateView.as_view(), name="staff_room_access"),
]
