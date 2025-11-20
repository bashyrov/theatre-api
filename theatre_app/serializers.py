from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        fields = "id", "first_name", "last_name", "full_name"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "id", "name"


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = "id", "title", "description", "genres", "actors", "image"


class PlayDetailSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.SlugRelatedField(read_only=True, slug_field="full_name", many=True)


class PlayListSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = "id", "title", "genres", "actors", "image"


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = "id", "play", "theatre_hall", "show_time"


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source='play.title', read_only=True)
    theatre_hall_name = serializers.CharField(source='theatre_hall.name', read_only=True)

    class Meta:
        model = Performance
        fields = "id", "play_title", "theatre_hall_name", "show_time", "available_seats"


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayDetailSerializer(read_only=True, many=False)
    theatre_hall = TheatreHallSerializer(read_only=True, many=False)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "id", "row", "seat_number", "performance"

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat_number"],
            attrs["performance"].theatre_hall
        )
        return data


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(read_only=True, many=False)
    class Meta:
        model = Ticket
        fields = "id", "row", "seat_number", "performance"


class TicketDetailSerializer(TicketSerializer):
    performance = PerformanceDetailSerializer(read_only=True, many=False)


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "user", "tickets", "created_at")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, write_only=True, allow_empty=False)

    class Meta:
        model = Reservation
        fields = "id", "created_at", "user", "tickets"

    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        with transaction.atomic:
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                performance = Performance.objects.get(
                    id=ticket_data['performance'].id if isinstance(ticket_data['performance'], Performance) else
                    ticket_data['performance'])
                Ticket.objects.create(
                    reservation=reservation,
                    row=ticket_data['row'],
                    seat_number=ticket_data['seat_number'],
                    performance=performance
                )
            return reservation


class ReservationDetailSerializer(ReservationListSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=True)