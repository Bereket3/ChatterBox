from rest_framework.generics import ListCreateAPIView

from .models import Room
from .serializer import RoomSerializer


class CreateOrListRoomsView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
