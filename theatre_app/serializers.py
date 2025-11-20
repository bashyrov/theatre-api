from rest_framework import serializers
from theatre_app.models import (TheatreHall,
                                Actor,
                                Genre,
                                Play,
                                Performance,
                                Ticket,
                                Reservation
                                )


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
        slug_field="name",
        queryset=Genre.objects.all()
    )

    actors = serializers.SlugRelatedField(
        many=True,
        slug_field="full_name",
        queryset=Actor.objects.all()
    )

    class Meta:
        model = Play
        fields = "id", "title", "description", "genres", "actors"


class PlayCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = "id", "title", "description", "genres", "actors"


class PerformanceSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source='play.title', read_only=True)
    theatre_hall_name = serializers.CharField(source='theatre_hall.name', read_only=True)

    class Meta:
        model = Performance
        fields = "id", "play_title", "theatre_hall_name", "show_time"


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True, many=False)
    theatre_hall = TheatreHallSerializer(read_only=True, many=False)

    class Meta:
        model = Performance
        fields = "id", "play", "theatre_hall", "show_time"


class TicketSerializer(serializers.ModelSerializer):
    performance_title = serializers.CharField(source="performance.play.title", read_only=True)

    class Meta:
        model = Ticket
        fields = "id", "row", "seat_number", "performance_title", "reservation"

class TicketDetailSerializer(TicketSerializer):
    performance = PerformanceDetailSerializer(read_only=True, many=False)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, source='ticket_set')

    class Meta:
        model = Reservation
        fields = "id", "created_at", "user", "tickets"