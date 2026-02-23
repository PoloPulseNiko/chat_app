from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/delete/", views.message_delete, name="message_delete"),
    path("<int:pk>/edit/", views.message_edit, name="message_edit"),
]
