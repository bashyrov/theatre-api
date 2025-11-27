from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre_app.models import Actor, Genre, Play
from theatre_app.serializers import PlayDetailSerializer, PlayListSerializer

PLAY_URL = reverse("theatre:play-list")


def sample_actor(**params) -> Actor:

    actors_defaults = {
        "first_name": "Example FName",
        "last_name": "Example SName"
    }

    actors_defaults.update(params)
    actor_obj = Actor.objects.create(**actors_defaults)

    return actor_obj


def sample_genre(**params) -> Genre:

    genres_defaults = {"name": "Example Genre"}

    genres_defaults.update(params)
    genre_obj = Genre.objects.create(**genres_defaults)

    return genre_obj


def sample_play(**params) -> Play:

    play_defaults = {
        "title": "Example Title",
        "description": "Example Description",
    }
    play_defaults.update(params)
    play_obj = Play.objects.create(**play_defaults)

    return play_obj


def get_play_detail_url(play: Play):
    return reverse("theatre:play-detail", args=[play.id])


class UnauthenticatedPlayApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response_play_list = self.client.get(PLAY_URL)

        self.assertEqual(
            response_play_list.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class AuthenticatedPlayApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@example.com",
            password="password",
        )
        self.client.force_authenticate(self.user)

    def test_plays_list(self):
        sample_play()

        response = self.client.get(PLAY_URL)
        plays_qrs = Play.objects.all()
        serializer = PlayListSerializer(plays_qrs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filtered_plays_by_genres(self):
        play_obj = sample_play()
        genre_obj = sample_genre()

        play_obj.genres.add(genre_obj)

        response = self.client.get(
            PLAY_URL,
            {
                "genre": f"{genre_obj.id}",
            },
        )

        play_qrst = Play.objects.filter(genres=genre_obj)
        serializer = PlayListSerializer(play_qrst, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filtered_plays_by_actors(self):
        play_obj = sample_play()
        actor_obj = sample_actor()

        play_obj.actors.add(actor_obj)

        response = self.client.get(
            PLAY_URL,
            {
                "actor": f"{actor_obj.id}",
            },
        )

        play_qrst = Play.objects.filter(actors=actor_obj)
        serializer = PlayListSerializer(play_qrst, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filtered_plays_by_title(self):
        play_obj = sample_play()

        response = self.client.get(
            PLAY_URL,
            {
                "title": f"{play_obj.title[:2]}",
            },
        )

        play_qrst = Play.objects.filter(title__icontains=play_obj.title[:2])
        serializer = PlayListSerializer(play_qrst, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_play_detail(self):
        play_obj = sample_play()
        actor_obj = sample_actor()
        genre_obj = sample_genre()

        play_obj.genres.add(genre_obj)
        play_obj.actors.add(actor_obj)

        serialized_play = PlayDetailSerializer(play_obj)

        url = get_play_detail_url(play_obj)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serialized_play.data, response.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Forbidden Play",
            "description": "Just a forbidden play",
        }
        response = self.client.post(PLAY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_play_forbidden(self):

        play_obj = sample_play()
        actor_obj = sample_actor()

        payload = {
            "actors": [actor_obj.id],
        }
        url = get_play_detail_url(play_obj)

        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_play_forbidden(self):

        play_obj = sample_play()
        url = get_play_detail_url(play_obj)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_play_success(self):
        actor_obj = sample_actor()
        genre_obj = sample_genre()

        payload = {
            "title": "Forbidden Play",
            "description": "Just a forbidden play",
            "genres": genre_obj.id,
            "actors": actor_obj.id,
        }
        response = self.client.post(PLAY_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        play_obj = Play.objects.get(id=response.data["id"])

        for key in payload:
            if key in ("actors", "genres"):
                related_ids = list(
                    getattr(
                        play_obj,
                        key
                    ).values_list("id", flat=True))
                self.assertEqual(payload[key], related_ids[0])
            else:
                self.assertEqual(payload[key], getattr(play_obj, key))

    def test_patch_play_success(self):
        play_obj = sample_play()
        actor_obj = sample_actor()

        payload = {
            "actors": [actor_obj.id],
        }
        url = get_play_detail_url(play_obj)

        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_play_success(self):
        play_obj = sample_play()
        url = get_play_detail_url(play_obj)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
