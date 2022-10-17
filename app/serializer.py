from django.db.models import Q
from rest_framework import serializers
from app.models import User, MeetingRoom, MeetingRoomReservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_name', 'first_name', 'email', 'password', 'created_at', 'updated_at']


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ['id', 'name', 'capacity']


class MeetingRoomReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoomReservation
        fields = ['id', 'organizer', 'meeting_start', 'meeting_end',
                  'meeting_room', 'attendees', 'created_at', 'updated_at']

    def validate(self, data):
        meeting_start = data['meeting_start']
        meeting_end = data['meeting_end']
        meeting_room = data['meeting_room']
        meeting_attendees_count = len(data['attendees'])

        query_room_reservation = MeetingRoomReservation.objects.filter(
            Q(meeting_room=meeting_room)
            & Q(meeting_end__gte=meeting_start)
            & Q(meeting_start__lte=meeting_end)
        ).exists()
        if query_room_reservation:
            raise serializers.ValidationError("There is a meeting reserved at this room and this time")
        print(meeting_attendees_count)

        if not meeting_room.capacity >= meeting_attendees_count:
            raise serializers.ValidationError("This room can`t fit this many people")
        return data
