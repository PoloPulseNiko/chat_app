from django.shortcuts import render, get_object_or_404, redirect

from .forms import MessageForm
from .models import Message

# Create your views here.
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        room_pk = message.room.pk
        message.delete()
        return redirect("room_detail", pk=room_pk)
    return render(request, "messages_app/message_confirm_delete.html", {"message": message})

def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("room_detail", pk=message.room.pk)
    else:
        form = MessageForm(instance=message)

    return render(request, "messages_app/message_form.html", {"form": form})
