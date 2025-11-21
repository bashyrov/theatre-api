from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
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
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + default_router.urls
