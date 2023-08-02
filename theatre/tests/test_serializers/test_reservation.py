from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Reservation, Play, TheatreHall, Performance, Ticket
from theatre.serializers import ReservationListSerializer, ReservationSerializer

RESERVATION_URL = reverse("theatre:reservation-list")


class UnauthenticatedReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESERVATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_reservations(self):
        reservation = Reservation.objects.create(user=self.user)

        res = self.client.get(RESERVATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        expected_data = ReservationListSerializer([reservation], many=True).data
        self.assertIn(expected_data[0], res.data["results"])
