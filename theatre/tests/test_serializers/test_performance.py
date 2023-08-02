from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Performance, TheatreHall, Play

PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_performance(**params):
    play = Play.objects.create(title="Title")
    theatre_hall = TheatreHall.objects.create(
        name="Main hall", rows=20, seats_in_row=20
    )

    defaults = {
        "show_time": "2023-07-21 14:00:00",
        "play": play,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(performance_id):
    return reverse("theatre:performance-detail", args=[performance_id])


class UnauthenticatedPerformanceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PERFORMANCE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPerformanceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_performances(self):
        sample_performance()
        sample_performance()

        res = self.client.get(PERFORMANCE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("play_title", res.data[0])
        self.assertIn("play_image", res.data[0])
        self.assertIn("theatre_hall_name", res.data[0])
        self.assertIn("theatre_hall_capacity", res.data[0])
        self.assertIn("tickets_available", res.data[0])

    def test_create_performance_forbidden(self):
        play = Play.objects.create(title="Title")
        theatre_hall = TheatreHall.objects.create(
            name="Main hall", rows=20, seats_in_row=20
        )
        payload = {
            "show_time": "2023-07-21 14:00:00",
            "play": play,
            "theatre_hall": theatre_hall,
        }
        res = self.client.post(PERFORMANCE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPerformanceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_performance(self):
        play = Play.objects.create(title="Title")
        theatre_hall = TheatreHall.objects.create(
            name="Main hall", rows=20, seats_in_row=20
        )
        payload = {
            "show_time": "2023-07-21 14:00:00",
            "play": play.id,
            "theatre_hall": theatre_hall.id,
        }
        res = self.client.post(PERFORMANCE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        performance = Performance.objects.get(id=res.data["id"])
        self.assertEqual(performance.play.id, play.id)
        self.assertEqual(performance.theatre_hall.id, theatre_hall.id)

    def test_update_performance(self):
        play = Play.objects.create(title="New Title")
        theatre_hall = TheatreHall.objects.create(
            name="Main hall", rows=20, seats_in_row=20
        )
        performance = sample_performance()
        payload = {
            "show_time": "2023-07-21 14:00:00",
            "play": play.id,
            "theatre_hall": theatre_hall.id,
        }
        url = detail_url(performance.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        performance = Performance.objects.get(id=res.data["id"])
        self.assertEqual(performance.play.id, play.id)
        self.assertEqual(performance.theatre_hall.id, theatre_hall.id)

    def test_partial_update_performance(self):
        performance = sample_performance()
        play = Play.objects.create(title="New Title")
        payload = {
            "play": play.id,
        }
        url = detail_url(performance.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        performance = Performance.objects.get(id=res.data["id"])
        self.assertEqual(performance.play.id, play.id)

    def test_delete_performance(self):
        performance = sample_performance()
        url = detail_url(performance.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
