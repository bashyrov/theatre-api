from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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
                                     TicketListSerializer,
                                     TicketDetailSerializer,
                                     ReservationSerializer,
                                     PerformanceDetailSerializer,
                                     PlayDetailSerializer,
                                     PlayListSerializer,
                                     PerformanceListSerializer,
                                     ReservationListSerializer,
                                     ReservationDetailSerializer
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
        if self.action == 'retrieve':
            self.serializer_class = PlayDetailSerializer
        elif self.action == 'list':
            self.serializer_class = PlayListSerializer
        else:
            self.serializer_class = PlaySerializer

        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminUser()]
        return super().get_permissions()


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            self.serializer_class = PerformanceListSerializer
        elif self.action == 'retrieve':
            self.serializer_class = PerformanceDetailSerializer
        else:
            self.serializer_class = PerformanceSerializer

        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminUser()]
        return super().get_permissions()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated, )


    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            self.serializer_class = TicketDetailSerializer
        elif self.action == 'list':
            self.serializer_class = TicketListSerializer
        else:
            self.serializer_class = TicketSerializer

        return super().get_serializer(*args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer(self, *args, **kwargs):
        if self.action in 'retrieve':
            self.serializer_class = ReservationDetailSerializer
        elif self.action == 'list':
            self.serializer_class = ReservationListSerializer
        else:
            self.serializer_class = ReservationSerializer
        return super().get_serializer(*args, **kwargs)