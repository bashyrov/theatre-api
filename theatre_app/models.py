import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

user_model = get_user_model()

class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_per_row = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def total_seats(self):
        return self.rows * self.seats_per_row


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Performance(models.Model):
    play = models.ForeignKey('Play', on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play} at {self.show_time} in {self.theatre_hall.name}"

    @property
    def available_seats(self):
        total_seats = self.theatre_hall.total_seats
        booked_seats = Ticket.objects.filter(performance=self).count()
        return total_seats - booked_seats


class Ticket(models.Model):
    row = models.IntegerField()
    seat_number = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("performance", "row", "seat_number")
        error_messages = {
            "unique_together": {
                ("performance", "row", "seat_number"):
                    "Ticket with this Performance, Row and Seat number already exists."
            }
        }

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat_number,
            self.performance.theatre_hall,
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @staticmethod
    def validate_ticket(row, seat, theatre_hall):

        for ticket_value, ticket_name, hall_attr in [
            (row, "row", "rows"),
            (seat, "seat_number", "seats_per_row"),
        ]:
            max_value = getattr(theatre_hall, hall_attr)
            if not (1 <= ticket_value <= max_value):
                raise ValidationError(
                    {
                        ticket_name: f"{ticket_name} number must be in range 1-{max_value}"
                    }
                )

    def __str__(self):
        return f"Seat {self.seat_number} in row {self.row} for {self.performance}"


def create_custom_path(instance, filename):
   _, extension = os.path.splitext(filename)
   return os.path.join(
       "uploads/images/",
       f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"
   )


class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='plays')
    genres = models.ManyToManyField(Genre, related_name='plays')
    image = models.ImageField(null=True, upload_to=create_custom_path)

    def __str__(self):
        return self.title


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user_model, related_name="reservations", on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation {self.id} by {self.user} at {self.created_at}"
