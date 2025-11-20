from rest_framework import routers

from theatre_app.views import (TheatreHallViewSet,
                               ActorViewSet,
                               GenreViewSet,
                               PlayViewSet,
                               PerformanceViewSet,
                               TicketViewSet,
                               ReservationViewSet
                               )

default_router = routers.DefaultRouter()

default_router.register("theatre-halls", TheatreHallViewSet)
default_router.register("actors", ActorViewSet)
default_router.register("genres", GenreViewSet)
default_router.register("plays", PlayViewSet)
default_router.register("performances", PerformanceViewSet)
default_router.register("tickets", TicketViewSet)
default_router.register("reservations", ReservationViewSet)

urlpatterns = [
] + default_router.urls
