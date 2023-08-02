from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Actor
from theatre.serializers import ActorSerializer

ACTOR_URL = reverse("theatre:actor-list")


def detail_url(actor_id):
    return reverse("theatre:actor-detail", args=[actor_id])


class UnauthenticatedActorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ACTOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedActorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_actors(self):
        Actor.objects.create(first_name="Actor 1", last_name="Last 1")
        Actor.objects.create(first_name="Actor 2", last_name="Last 2")

        res = self.client.get(ACTOR_URL)

        actors = Actor.objects.order_by("id")
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_actor_detail(self):
        actor = Actor.objects.create(first_name="Actor 1", last_name="Last 1")

        url = detail_url(actor.id)
        res = self.client.get(url)

        serializer = ActorSerializer(actor)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_actor_forbidden(self):
        payload = {
            "first_name": "Actor 1",
            "last_name": "Last 1"
        }
        res = self.client.post(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_actor(self):
        payload = {
            "first_name": "Actor 1",
            "last_name": "Last 1"
        }
        res = self.client.post(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        actor = Actor.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(actor, key))

    def test_update_actor(self):
        actor = Actor.objects.create(first_name="Actor 1", last_name="Last 1")
        payload = {
            "first_name": "Actor 123",
            "last_name": "Last 123"
        }
        url = detail_url(actor.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actor = Actor.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(actor, key))

    def test_partial_update_actor(self):
        actor = Actor.objects.create(first_name="Actor 1", last_name="Last 1")
        payload = {
            "first_name": "Actor 123",
        }
        url = detail_url(actor.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actor = Actor.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(actor, key))

    def test_delete_actor(self):
        actor = Actor.objects.create(first_name="Actor 1", last_name="Last 1")
        url = detail_url(actor.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
