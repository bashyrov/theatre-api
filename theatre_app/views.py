from rest_framework import viewsets
from theatre_app.models import (TheatreHall,
                                Actor,
                                Genre,
                                Play,
                                Performance,
                                Ticket,
                                Reservation
                                )
from theatre_app.serializers import (TheatreHallSerializer,
                                     ActorSerializer,
                                     GenreSerializer,
                                     PlaySerializer,
                                     PerformanceSerializer,
                                     TicketSerializer,
                                     ReservationSerializer,
                                     TicketDetailSerializer,
                                     PerformanceDetailSerializer,
                                     PlayCreateUpdateSerializer,
                                     PerformanceCreateUpdateSerializer,
                                     TicketCreateUpdateSerializer
                                     )


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'update', 'partial_update'):
            self.serializer_class = PlayCreateUpdateSerializer
        else:
            self.serializer_class = PlaySerializer

        return super().get_serializer(*args, **kwargs)

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'update', 'partial_update'):
            self.serializer_class = PerformanceCreateUpdateSerializer
        elif self.action == 'retrieve':
            self.serializer_class = PerformanceDetailSerializer
        else:
            self.serializer_class = PerformanceSerializer

        return super().get_serializer(*args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            self.serializer_class = TicketDetailSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            self.serializer_class = TicketCreateUpdateSerializer
        else:
            self.serializer_class = TicketSerializer

        return super().get_serializer(*args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer