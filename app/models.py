from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now


class CreatedUpdatedAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class User(CreatedUpdatedAt):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"Email: {self.email}"


class MeetingRoom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Meeting room name: {self.name}"


class MeetingRoomReservation(CreatedUpdatedAt):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_room_reservation')
    meeting_start = models.DateTimeField(default=now, blank=True)
    meeting_end = models.DateTimeField(default=now, blank=True)
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, related_name='meeting_room_reservation')
    attendees = models.ManyToManyField(User)

    def __str__(self):
        return f"Organizer: {self.organizer}, Meeting_start: {self.meeting_start}, Meeting_end: {self.meeting_end}"
