from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from .forms import MessageForm
from .models import Message


class MessageAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        message = self.get_object()
        return self.request.user.is_authenticated and message.sender == self.request.user.profile


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
