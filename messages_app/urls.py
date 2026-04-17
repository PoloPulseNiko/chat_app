from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),
    path("<int:pk>/edit/", views.MessageUpdateView.as_view(), name="message_edit"),
    path("<int:pk>/react/<str:reaction_type>/", views.MessageReactionToggleView.as_view(), name="message_react"),
]
