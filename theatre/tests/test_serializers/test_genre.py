from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Genre
from theatre.serializers import GenreSerializer

GENRE_URL = reverse("theatre:genre-list")


def detail_url(genre_id):
    return reverse("theatre:genre-detail", args=[genre_id])


class UnauthenticatedGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(GENRE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_genres(self):
        Genre.objects.create(name="Genre 1")
        Genre.objects.create(name="Genre 2")

        res = self.client.get(GENRE_URL)

        genres = Genre.objects.order_by("id")
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_genre_detail(self):
        genre = Genre.objects.create(name="Genre 1")

        url = detail_url(genre.id)
        res = self.client.get(url)

        serializer = GenreSerializer(genre)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_genre_forbidden(self):
        payload = {"name": "Genre 1"}
        res = self.client.post(GENRE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminGenreApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_genre(self):
        payload = {"name": "Genre 1"}
        res = self.client.post(GENRE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        genre = Genre.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(genre, key))

    def test_update_genre(self):
        genre = Genre.objects.create(name="Genre 1")
        payload = {"name": "Genre 11111"}
        url = detail_url(genre.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        genre = Genre.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(genre, key))

    def test_delete_genre(self):
        genre = Genre.objects.create(name="Genre 1")
        url = detail_url(genre.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
