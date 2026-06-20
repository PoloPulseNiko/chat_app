from django.urls import path
from . import views

urlpatterns = [
    path("direct/", views.DirectConversationListView.as_view(), name="direct_conversation_list"),
    path("direct/<int:pk>/", views.DirectConversationDetailView.as_view(), name="direct_conversation_detail"),
    path("<int:pk>/delete/", views.MessageDeleteView.as_view(), name="message_delete"),
    path("<int:pk>/edit/", views.MessageUpdateView.as_view(), name="message_edit"),
    path("<int:pk>/react/<str:reaction_type>/", views.MessageReactionToggleView.as_view(), name="message_react"),
]
