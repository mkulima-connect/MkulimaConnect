from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ChatRoom


@login_required
def room(request, room_name):
    chat_room, _ = ChatRoom.objects.get_or_create(name=room_name)
    messages = chat_room.messages.select_related("sender").order_by("timestamp")[:50]
    return render(request, "chat/room.html", {"room_name": chat_room.name, "chat_messages": messages})
