from rest_framework import viewsets
from theatre_app.models import TheatreHall
from theatre_app.serializers import TheatreHallSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer