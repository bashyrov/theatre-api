from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre_app.models import Reservation
from theatre_app.tests.tests_performance_theatre import sample_play, sample_performance
from theatre_app.serializers import ReservationSerializer, ReservationDetailSerializer, ReservationListSerializer
from theatre_app.tests.tests_tickets_theatre import sample_ticket, sample_reservation

RESERVATION_URL = reverse("theatre:reservation-list")


def get_reservation_detail_url(reservation: Reservation):
    return reverse("theatre:reservation-detail", args=[reservation.id])


class UnauthenticatedReservationApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response_reservation_list = self.client.get(RESERVATION_URL)

        self.assertEqual(response_reservation_list.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@example.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_reservation_list(self):
        reservation_obj = sample_reservation(user=self.user)
        performance_obj = sample_performance()

        sample_ticket(reservation=reservation_obj, performance=performance_obj)

        response = self.client.get(RESERVATION_URL)
        reservation_qrs = Reservation.objects.all().filter(user=self.user)
        serializer = ReservationListSerializer(reservation_qrs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


    def test_retrieve_reservation_detail(self):
        reservation_obj = sample_reservation(user=self.user)

        serialized_reservation = ReservationDetailSerializer(reservation_obj)

        url = get_reservation_detail_url(reservation_obj)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serialized_reservation.data, response.data)

    def test_create_reservation_success(self):
        performance_obj = sample_performance()

        payload = {
                "tickets": [
                    {
                        "row": performance_obj.theatre_hall.rows - 1,
                        "seat_number": performance_obj.theatre_hall.seats_per_row - 1,
                        "performance": performance_obj.id
                    }
                ]
        }

        response = self.client.post(RESERVATION_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_delete_reservation_success(self):
        reservation_obj = sample_reservation(user=self.user)

        url = get_reservation_detail_url(reservation_obj)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AdminPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)
