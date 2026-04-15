from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomListView.as_view(), name="room_list"),
    path("create/", views.RoomCreateView.as_view(), name="room_create"),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("<int:pk>/edit/", views.RoomUpdateView.as_view(), name="room_edit"),
    path("<int:pk>/delete/", views.RoomDeleteView.as_view(), name="room_delete"),
    path("<int:pk>/join/", views.RoomJoinView.as_view(), name="room_join"),
    path("<int:pk>/leave/", views.RoomLeaveView.as_view(), name="room_leave"),
]
