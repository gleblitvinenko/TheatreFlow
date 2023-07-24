from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import TheatreHall
from theatre.serializers import TheatreHallSerializer

THEATRE_HALL_URL = reverse("theatre:theatrehall-list")


def detail_url(theatre_hall_id):
    return reverse("theatre:theatrehall-detail", args=[theatre_hall_id])


class UnauthenticatedTheatreHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()


class AuthenticatedTheatreHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_theatre_halls(self):
        TheatreHall.objects.create(name="TheatreHall 1", rows=10, seats_in_row=15)
        TheatreHall.objects.create(name="TheatreHall 2", rows=10, seats_in_row=15)

        res = self.client.get(THEATRE_HALL_URL)

        theatre_halls = TheatreHall.objects.order_by("id")
        serializer = TheatreHallSerializer(theatre_halls, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_theatre_hall_detail(self):
        theatre_hall = TheatreHall.objects.create(name="TheatreHall 1", rows=10, seats_in_row=15)

        url = detail_url(theatre_hall.id)
        res = self.client.get(url)

        serializer = TheatreHallSerializer(theatre_hall)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminTheatreHallApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_theatre_hall(self):
        payload = {
            "name": "TheatreHall 1",
            "rows": 10,
            "seats_in_row": 15
        }
        res = self.client.post(THEATRE_HALL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        theatre_hall = TheatreHall.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(theatre_hall, key))

    def test_update_theatre_hall(self):
        theatre_hall = TheatreHall.objects.create(name="TheatreHall 1", rows=10, seats_in_row=15)
        payload = {
            "name": "TheatreHall 2",
            "rows": 20,
            "seats_in_row": 10
        }
        url = detail_url(theatre_hall.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        theatre_hall = TheatreHall.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(theatre_hall, key))

    def test_partial_update_theatre_hall(self):
        theatre_hall = TheatreHall.objects.create(name="TheatreHall 1", rows=10, seats_in_row=15)
        payload = {
            "name": "TheatreHall 123",
        }
        url = detail_url(theatre_hall.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        theatre_hall = TheatreHall.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(theatre_hall, key))

    def test_delete_theatre_hall(self):
        theatre_hall = TheatreHall.objects.create(name="TheatreHall 1", rows=10, seats_in_row=15)
        url = detail_url(theatre_hall.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
