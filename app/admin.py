from django.contrib import admin
from app.models import User, MeetingRoom, MeetingRoomReservation


admin.site.register(User)
admin.site.register(MeetingRoom)
admin.site.register(MeetingRoomReservation)

