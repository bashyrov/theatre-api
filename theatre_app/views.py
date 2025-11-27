from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from theatre_app.models import (TheatreHall,
                                Actor,
                                Genre,
                                Play,
                                Performance,
                                Ticket,
                                Reservation
                                )
from theatre_app.permissions import IsAdminOrIfAuthenticatedReadOnly
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='actors',
                description='Filter by actor id (ex. ?actors=2,5)',
                type={"type": "list", "items": {"type": "number"}},
            ),
            OpenApiParameter(
                name='genres',
                description='Filter by genre id (ex. ?genres=2,5)',
                type={"type": "list", "items": {"type": "number"}},
            ),
            OpenApiParameter(
                name='title',
                description='Filter by movie title (ex. ?title=fiction)',
                type=OpenApiTypes.STR
            ),
        ],
        description='Filters plays by genres, actors and title.',
        auth=None,
        operation_id=None,
        operation=None,
    )
    def list(self, request):
        return super().list(request)

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


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='play',
                description='Filter by play id (ex. ?play=2)',
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='date',
                description='Filter by datetime (ex. ?date=2022-10-23)',
                required=False,
                type=OpenApiTypes.DATE
            ),
        ],
        description='Filters performances by plays and datetime.',
        auth=None,
        operation_id=None,
        operation=None,
    )
    def list(self, request):
        return super().list(request)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            self.serializer_class = PerformanceListSerializer
        elif self.action == 'retrieve':
            self.serializer_class = PerformanceDetailSerializer
        else:
            self.serializer_class = PerformanceSerializer

        return super().get_serializer(*args, **kwargs)


class TicketViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
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