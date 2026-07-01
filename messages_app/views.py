from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, TemplateView, UpdateView

from accounts_app.services import ensure_user_profile
from notifications_app.services import create_direct_message_notifications
from profiles_app.models import Profile

from .forms import DirectMessageForm, MessageForm
from .models import DirectConversation, DirectMessage, Message, Reaction


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
        if not message.room.can_view_content(user=request.user, profile=profile):
            return redirect("room_list")

        reaction, created = Reaction.objects.get_or_create(
            message=message,
            profile=profile,
            reaction_type=reaction_type,
        )
        if not created:
            reaction.delete()

        return redirect("room_detail", pk=message.room.pk)


class DirectConversationListView(LoginRequiredMixin, TemplateView):
    template_name = "messages_app/direct_conversation_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = ensure_user_profile(self.request.user)
        query = self.request.GET.get("q", "").strip()

        conversations = DirectConversation.objects.filter(participants=profile).prefetch_related(
            "participants",
            "direct_messages",
        )
        conversation_rows = [
            {
                "conversation": conversation,
                "other_profile": conversation.other_participant(profile),
                "last_message": conversation.direct_messages.order_by("-created_at").first(),
            }
            for conversation in conversations
        ]
        profiles = Profile.objects.exclude(pk=profile.pk).order_by("nickname")
        if query:
            profiles = profiles.filter(Q(nickname__icontains=query) | Q(user__username__icontains=query))

        context.update(
            {
                "profile": profile,
                "conversation_rows": conversation_rows,
                "profiles": profiles[:12],
                "query": query,
            }
        )
        return context

    def post(self, request):
        profile = ensure_user_profile(request.user)
        other_profile = get_object_or_404(Profile, pk=request.POST.get("profile_id"))
        if other_profile == profile:
            return redirect("direct_conversation_list")

        conversation = (
            DirectConversation.objects.filter(participants=profile)
            .filter(participants=other_profile)
            .first()
        )
        if not conversation:
            conversation = DirectConversation.objects.create()
            conversation.participants.add(profile, other_profile)

        return redirect("direct_conversation_detail", pk=conversation.pk)


class DirectConversationDetailView(LoginRequiredMixin, DetailView):
    model = DirectConversation
    template_name = "messages_app/direct_conversation_detail.html"
    context_object_name = "conversation"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = ensure_user_profile(request.user)
        if not self.object.participants.filter(pk=profile.pk).exists():
            return redirect("direct_conversation_list")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return DirectConversation.objects.prefetch_related("participants", "direct_messages__sender")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = ensure_user_profile(self.request.user)
        context.update(
            {
                "profile": profile,
                "other_profile": self.object.other_participant(profile),
                "direct_messages": self.object.direct_messages.select_related("sender"),
                "form": kwargs.get("form", DirectMessageForm()),
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = ensure_user_profile(request.user)
        if not self.object.participants.filter(pk=profile.pk).exists():
            return redirect("direct_conversation_list")

        form = DirectMessageForm(request.POST)
        if form.is_valid():
            direct_message = form.save(commit=False)
            direct_message.conversation = self.object
            direct_message.sender = profile
            direct_message.save()
            self.object.save(update_fields=["updated_at"])
            create_direct_message_notifications(direct_message)
            return redirect(
                f"{reverse_lazy('direct_conversation_detail', kwargs={'pk': self.object.pk})}#direct-message-{direct_message.pk}"
            )

        return self.render_to_response(self.get_context_data(form=form))
