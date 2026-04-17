from django.urls import path

from .views import StaffBroadcastView, StaffDashboardView


urlpatterns = [
    path("", StaffDashboardView.as_view(), name="staff_dashboard"),
    path("broadcast/", StaffBroadcastView.as_view(), name="staff_broadcast"),
]
