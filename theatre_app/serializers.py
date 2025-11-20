from rest_framework import serializers

from theatre_app.models import TheatreHall, Genre, Actor, Play, Performance, Reservation, Ticket

class TheatreHallSerializer(serializers.ModelSerializer):
    count_seats = serializers.IntegerField(source='total_seats', read_only=True)

    class Meta:
        model = TheatreHall
        fields = "id", "name", "rows", "seats_per_row", "count_seats"

class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = "id", "first_name", "last_name"

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "id", "name"

class PlaySerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )

    class Meta:
        model = Play
        fields = "id", "title", "description", "genres", "actors"