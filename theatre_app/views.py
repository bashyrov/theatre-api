from rest_framework import viewsets
from theatre_app.models import TheatreHall, Actor
from theatre_app.serializers import TheatreHallSerializer, ActorSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer