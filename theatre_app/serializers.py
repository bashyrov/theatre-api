from rest_framework import serializers

from theatre_app.models import TheatreHall, Genre, Actor, Play, Performance, Reservation, Ticket

class TheatreHallSerializer(serializers.ModelSerializer):
    count_seats = serializers.IntegerField(source='total_seats', read_only=True)

    class Meta:
        model = TheatreHall
        fields = "id", "name", "rows", "seats_per_row", "count_seats"
