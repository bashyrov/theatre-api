from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre_app.models import Performance, TheatreHall
from theatre_app.serializers import (PerformanceDetailSerializer,
                                     PerformanceListSerializer)
from theatre_app.tests.tests_play_theatre import sample_play

PERFORMANCE_URL = reverse("theatre:performance-list")
THEATRE_HALL_URL = reverse("theatre:theatrehall-list")


def sample_theatre_hall(**params) -> TheatreHall:
    theatre_hall_defaults = {
        "name": "Test Hall",
        "rows": 20,
        "seats_per_row": 8
    }
    theatre_hall_defaults.update(params)

    theatre_hall_obj = TheatreHall.objects.create(**theatre_hall_defaults)

    return theatre_hall_obj


def sample_performance(**params) -> Performance:

    play_obj = sample_play()
    theatre_hall_obj = sample_theatre_hall()

    performance_defaults = {
        "play": play_obj,
        "theatre_hall": theatre_hall_obj,
        "show_time": datetime(
            year=2025, month=12, day=31, hour=0, minute=0, tzinfo=timezone.utc
        ),
    }

    performance_defaults.update(params)

    performance_obj = Performance.objects.create(**performance_defaults)

    return performance_obj


def get_performance_detail_url(performance: Performance):
    return reverse("theatre:performance-detail", args=[performance.id])


class UnauthenticatedPerformanceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_not_required(self):
        response_performance_list = self.client.get(PERFORMANCE_URL)

        self.assertEqual(
            response_performance_list.status_code, status.HTTP_200_OK
        )


class AuthenticatedPerformanceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@example.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_performances_list(self):
        sample_performance()

        response = self.client.get(PERFORMANCE_URL)
        performances_qrs = Performance.objects.all()
        serialized_performances = PerformanceListSerializer(
            performances_qrs,
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            serialized_performances.data
        )

    def test_filtered_performances_by_show_time(self):
        performance_obj = sample_performance()
        show_time = performance_obj.show_time

        response = self.client.get(
            PERFORMANCE_URL,
            {
                "date": f"{show_time.year}-{show_time.month}-{show_time.day}",
            },
        )

        performances_qrs = Performance.objects.filter(show_time=show_time)
        serialized_performances = PerformanceListSerializer(
            performances_qrs,
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            serialized_performances.data
        )

    def test_filtered_performances_by_actors(self):
        performance_obj = sample_performance()
        play_obj = performance_obj.play

        response = self.client.get(
            PERFORMANCE_URL,
            {
                "play": f"{play_obj.id}",
            },
        )

        performances_qrs = Performance.objects.filter(play__id=play_obj.id)
        serialized_performances = PerformanceListSerializer(
            performances_qrs,
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            serialized_performances.data
        )

    def test_retrieve_performance_detail(self):
        performance_obj = sample_performance()

        serialized_performance = PerformanceDetailSerializer(performance_obj)

        url = get_performance_detail_url(performance_obj)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serialized_performance.data, response.data)

    def test_create_performance_forbidden(self):
        payload = {
            "title": "Forbidden Performance",
            "description": "Just a forbidden Performance",
        }
        response = self.client.post(PERFORMANCE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_performance_forbidden(self):
        play_obj = sample_play()
        performance_obj = sample_performance()

        payload = {
            "play": [play_obj.id],
        }
        url = get_performance_detail_url(performance_obj)

        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_performance_forbidden(self):
        performance_obj = sample_performance()
        url = get_performance_detail_url(performance_obj)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminPerformanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_performance_success(self):
        play_obj = sample_play()
        theatre_hall_obj = sample_theatre_hall()

        payload = {
            "play": [play_obj.id],
            "theatre_hall": [theatre_hall_obj.id],
            "show_time": datetime(
                year=2025,
                month=12,
                day=31,
                hour=0,
                minute=0,
                tzinfo=timezone.utc
            ),
        }
        response = self.client.post(PERFORMANCE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        performance_obj = Performance.objects.get(id=response.data["id"])

        for key in payload:
            if key in ("play", "theatre_hall"):
                self.assertEqual(
                    payload[key],
                    [
                        (getattr(performance_obj, key)).id
                    ]
                )
            else:
                self.assertEqual(payload[key], getattr(performance_obj, key))

    def test_patch_performance_success(self):
        performance_obj = sample_performance()
        theatre_hall_obj = sample_theatre_hall()

        payload = {
            "theatre_hall": [theatre_hall_obj.id],
        }
        url = get_performance_detail_url(performance_obj)

        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_performance_success(self):
        performance_obj = sample_performance()
        url = get_performance_detail_url(performance_obj)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
