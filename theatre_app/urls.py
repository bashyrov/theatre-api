"""
URL configuration for theatre project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
