from datetime import datetime

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
    permission_classes = (IsAuthenticated, )


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAuthenticated, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated, )


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            self.serializer_class = PlayDetailSerializer
        elif self.action == 'list':
            self.serializer_class = PlayListSerializer
        else:
            self.serializer_class = PlaySerializer

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres_ids)

        if actors:
            actors_ids = self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors_ids)

        return queryset.distinct()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminUser()]
        return super().get_permissions()


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        date = self.request.query_params.get("date")
        play_id_str = self.request.query_params.get("play")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if play_id_str:
            queryset = queryset.filter(play_id=int(play_id_str))

        return queryset

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

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)