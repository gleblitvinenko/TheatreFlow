from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    TheatreHall,
    Reservation, Ticket,
)


class ActorModelTests(TestCase):
    def test_actor_str(self):
        actor = Actor.objects.create(
            first_name="Test first", last_name="Test last"
        )

        self.assertEqual(str(actor), f"{actor.first_name} {actor.last_name}")


class GenreModelTests(TestCase):
    def test_genre_str(self):
        genre = Genre.objects.create(name="Test name")

        self.assertEqual(str(genre), genre.name)


class PerformanceModelTests(TestCase):
    def test_performance_str(self):
        play = Play.objects.create(title="Test Play")
        theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_row=10
        )
        performance = Performance.objects.create(
            play=play,
            theatre_hall=theatre_hall,
            show_time=datetime(2023, 7, 21, 19, 30)
        )

        expected_str = f"{play.title}"
        self.assertEqual(str(performance), expected_str)


class PlayModelTests(TestCase):
    def test_play_str(self):
        play = Play.objects.create(title="Test title")

        self.assertEqual(str(play), play.title)


class ReservationModelTests(TestCase):
    def test_reservation_str(self):
        user = get_user_model().objects.create_user(
            email="user@test.com", password="testpassword"
        )
        reservation = Reservation.objects.create(user=user)

        expected_str = str(reservation.created_at)
        self.assertEqual(str(reservation), expected_str)


class TheatreHallModelTests(TestCase):
    def test_theatre_hall_str(self):
        theatre_hall = TheatreHall.objects.create(
            name="Test name", rows=10, seats_in_row=10
        )

        self.assertEqual(str(theatre_hall), theatre_hall.name)

    def test_theatre_hall_capacity(self):
        theatre_hall = TheatreHall.objects.create(
            name="Test name", rows=10, seats_in_row=10
        )

        self.assertEqual(theatre_hall.capacity, 100)


class TicketModelTests(TestCase):
    def test_ticket_str(self):
        theatre_hall = TheatreHall.objects.create(
            name="Test Theatre", rows=5, seats_in_row=10
        )
        play = Play.objects.create(title="Test Play")
        performance = Performance.objects.create(
            play=play,
            theatre_hall=theatre_hall,
            show_time=datetime(2023, 7, 21, 19, 30)
        )
        user = get_user_model().objects.create_user(
            email="user@test.com", password="testpassword"
        )
        reservation = Reservation.objects.create(user=user)
        ticket = Ticket.objects.create(
            row=2, seat=5, performance=performance, reservation=reservation
        )

        expected_str = f"{str(performance)} (row: 2, seat: 5)"
        self.assertEqual(str(ticket), expected_str)
