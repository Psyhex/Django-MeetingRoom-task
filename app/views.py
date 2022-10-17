from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from app.serializer import UserSerializer, MeetingRoomSerializer, MeetingRoomReservationSerializer
from app.models import User, MeetingRoom, MeetingRoomReservation


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all().order_by('id')
    serializer_class = MeetingRoomSerializer
    permission_classes = [permissions.AllowAny]


class MeetingRoomReservationViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoomReservation.objects.order_by('-created_at')
    serializer_class = MeetingRoomReservationSerializer
    permission_classes = [permissions.AllowAny]



