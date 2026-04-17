from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from accounts_app.services import ensure_user_profile

from .forms import MessageForm
from .models import Message, Reaction


class MessageAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        message = self.get_object()
        profile = ensure_user_profile(self.request.user)
        return bool(profile and message.sender == profile)


class MessageUpdateView(LoginRequiredMixin, MessageAuthorRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messages_app/message_form.html"

    def get_success_url(self):
        return reverse_lazy("room_detail", kwargs={"pk": self.object.room.pk})


class MessageDeleteView(LoginRequiredMixin, MessageAuthorRequiredMixin, DeleteView):
    model = Message
    template_name = "messages_app/message_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("room_detail", kwargs={"pk": self.object.room.pk})


class MessageReactionToggleView(LoginRequiredMixin, View):
    def post(self, request, pk, reaction_type):
        message = get_object_or_404(Message, pk=pk)
        profile = ensure_user_profile(request.user)
        valid_reactions = {choice[0] for choice in Reaction.REACTION_CHOICES}

        if reaction_type not in valid_reactions:
            return redirect("room_detail", pk=message.room.pk)

        reaction, created = Reaction.objects.get_or_create(
            message=message,
            profile=profile,
            reaction_type=reaction_type,
        )
        if not created:
            reaction.delete()

        return redirect("room_detail", pk=message.room.pk)
