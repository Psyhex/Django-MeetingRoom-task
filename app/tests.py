import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import User, MeetingRoom, MeetingRoomReservation


class CreateMeetingRoomTest(APITestCase):
    def test_create_meeting_room(self):
        url = reverse("meeting_room-list")
        data = {
            "name": "Michael`s Room",
            "capacity": 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(MeetingRoom.objects.count(), 1)
        self.assertEqual(MeetingRoom.objects.get().name, "Michael`s Room")
        self.assertEqual(MeetingRoom.objects.get().capacity, 20)

    def test_create_meeting_room_negative_capacity(self):
        url = reverse("meeting_room-list")
        data = {
            "name": "Teemo room",
            "capacity": -2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_create_meeting_room_zero_capacity(self):
        url = reverse("meeting_room-list")
        data = {
            "name": "Teemo room",
            "capacity": 0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)


class CreateMeetingRoomReservationTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            first_name="Rokas", last_name="Sapola", email="rokas.sapola@gmail.com", password="123456")
        self.user2 = User.objects.create(
            first_name="Rokas2", last_name="Sapola2", email="rokas.sapola2@gmail.com", password="123456")
        self.user3 = User.objects.create(
            first_name="Rokas3", last_name="Sapola3", email="rokas.sapola3@gmail.com", password="123456")
        self.meeting_room1 = MeetingRoom.objects.create(name="Michael`s Room", capacity=20)
        self.meeting_room2 = MeetingRoom.objects.create(name="Kenny`s Room", capacity=2)

        self.meeting_room_reservation1 = MeetingRoomReservation.objects.create(
            organizer=self.user1, meeting_start=datetime.datetime(2022, 5, 17, 18, 0),
            meeting_end=datetime.datetime(2022, 5, 17, 19, 30), meeting_room=self.meeting_room1
        )
        self.meeting_room_reservation1.attendees.set([self.user1, self.user2, self.user3])

        self.meeting_room_reservation2 = MeetingRoomReservation.objects.create(
            organizer=self.user1, meeting_start=datetime.datetime(2022, 5, 17, 19, 30),
            meeting_end=datetime.datetime(2022, 5, 17, 20, 30), meeting_room=self.meeting_room2
        )
        self.meeting_room_reservation2.attendees.set([self.user1, self.user3])
        self.url = reverse("meeting_room_reservation-list")

    def test_create_meeting_room_reservation(self):
        data = {
            "organizer": self.user1.id,
            "meeting_start": datetime.datetime(2022, 5, 17, 20, 0),
            "meeting_end": datetime.datetime(2022, 5, 17, 20, 30),
            "meeting_room": self.meeting_room1.id,
            "attendees": [self.user1.id, self.user2.id, self.user3.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(MeetingRoomReservation.objects.count(), 3)

    def test_create_meeting_room_reservation_time_overlap(self):
        data = {
            "organizer": self.user1.id,
            "meeting_start": datetime.datetime(2022, 5, 17, 18, 0),
            "meeting_end": datetime.datetime(2022, 5, 17, 20, 30),
            "meeting_room": self.meeting_room1.id,
            "attendees": [self.user1.id, self.user2.id, self.user3.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_create_meeting_room_reservation_capacity_fail(self):
        data = {
            "organizer": self.user1.id,
            "meeting_start": datetime.datetime(2022, 5, 17, 18, 0),
            "meeting_end": datetime.datetime(2022, 5, 17, 20, 30),
            "meeting_room": self.meeting_room2.id,
            "attendees": [self.user1.id, self.user3.id, self.user2.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_create_meeting_room_reservation_capacity_success(self):
        data = {
            "organizer": self.user1.id,
            "meeting_start": datetime.datetime(2022, 5, 17, 21, 0),
            "meeting_end": datetime.datetime(2022, 5, 17, 21, 30),
            "meeting_room": self.meeting_room2.id,
            "attendees": [self.user1.id, self.user3.id]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
