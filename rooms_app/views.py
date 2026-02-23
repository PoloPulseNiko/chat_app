from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from .forms import RoomForm
from messages_app.forms import MessageForm
from profiles_app.models import Profile

def room_list(request):
    rooms = Room.objects.all()
    return render(request, "rooms_app/room_list.html", {"rooms": rooms})

def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    messages = room.messages.order_by("created_at")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = Profile.objects.first()
            message.room = room
            message.save()
            return redirect("room_detail", pk=room.pk)
    else:
        form = MessageForm()

    return render(request, "rooms_app/room_detail.html", {"room": room, "messages": messages, "form": form})

def room_create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = Profile.objects.first()
            room.save()
            return redirect("room_list")
    else:
        form = RoomForm()
    return render(request, "rooms_app/room_form.html", {"form": form})

def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room_detail", pk=room.pk)
    else:
        form = RoomForm(instance=room)
    return render(request, "rooms_app/room_form.html", {"form": form})
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        room.delete()
        return redirect("room_list")  # or wherever your list view is
    return render(request, "rooms_app/room_confirm_delete.html", {"room": room})