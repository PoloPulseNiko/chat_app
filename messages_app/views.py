from django.shortcuts import render, get_object_or_404, redirect
from .models import Message

# Create your views here.
def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        room_pk = message.room.pk
        message.delete()
        return redirect("room_detail", pk=room_pk)
    return render(request, "messages_app/message_confirm_delete.html", {"message": message})

