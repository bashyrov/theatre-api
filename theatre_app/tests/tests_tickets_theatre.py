from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre_app.models import Ticket, Reservation
from theatre_app.tests.tests_performance_theatre import sample_performance
from theatre_app.serializers import TicketListSerializer, TicketDetailSerializer, TicketSerializer

TICKET_URL = reverse("theatre:ticket-list")


def sample_reservation(**params) -> Reservation:
    reservation_obj = Reservation.objects.create(**params)

    return reservation_obj


def sample_ticket(**params) -> Ticket:

    performance_obj = params.pop("performance", None)
    if performance_obj is None:
        performance_obj = sample_performance()

    ticket_default = {
        "row": f"{performance_obj.theatre_hall.rows - 1}",
        "seat_number": f"{performance_obj.theatre_hall.seats_per_row - 1}",
        "performance": performance_obj
    }

    ticket_default.update(params)
    ticket_obj = Ticket.objects.create(**ticket_default)

    return ticket_obj


def get_ticket_detail_url(ticket: Ticket):
    return reverse("theatre:ticket-detail", args=[ticket.id])


class UnauthenticatedTicketApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response_ticket_list = self.client.get(TICKET_URL)

        self.assertEqual(response_ticket_list.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@example.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_tickets_list(self):
        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()

        sample_ticket(reservation=reservation_obj, performance=performance_obj)

        response = self.client.get(TICKET_URL)
        tickets_qrs = Ticket.objects.all().filter(reservation__user=self.user)
        serializer = TicketListSerializer(tickets_qrs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


    def test_retrieve_ticket_detail(self):
        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()

        ticket_obj = sample_ticket(reservation=reservation_obj, performance=performance_obj)

        serialized_ticket = TicketDetailSerializer(ticket_obj)

        url = get_ticket_detail_url(ticket_obj)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serialized_ticket.data, response.data)

    def test_create_ticket_forbidden(self):

        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()
        theatre_hall_obj = performance_obj.theatre_hall

        payload = {
            "row": theatre_hall_obj.rows - 1,
            "seat_number": theatre_hall_obj.seats_per_row - 1,
            "performance": performance_obj.id,
            "reservation": reservation_obj.id
        }
        response = self.client.post(TICKET_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_ticket_success(self):

        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()
        ticket_obj = sample_ticket(reservation=reservation_obj, performance=performance_obj)
        theatre_hall_obj = performance_obj.theatre_hall

        second_performance_obj = sample_performance()
        payload = {
            "row": theatre_hall_obj.rows - 1,
            "seat_number": theatre_hall_obj.seats_per_row - 1,
            "performance": second_performance_obj.id,
            "reservation": reservation_obj.id
        }

        url = get_ticket_detail_url(ticket_obj)

        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ticket_success(self):
        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()

        ticket_obj = sample_ticket(reservation=reservation_obj, performance=performance_obj)
        url = get_ticket_detail_url(ticket_obj)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validate_seat(self):
        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()

        data = {
            "reservation": reservation_obj,
            "performance": performance_obj.id,
            "row": 43,
            "seat_number": 1
        }

        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "row number must be in range",
            str(serializer.errors)
        )


class AdminPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

