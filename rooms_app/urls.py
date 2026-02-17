from django.urls import path
from . import views

urlpatterns = [
    path("", views.room_list, name="room_list"),
    path("create/", views.room_create, name="room_create"),
    path("<int:pk>/", views.room_detail, name="room_detail"),
]