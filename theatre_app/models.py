from django.db import models
from rest_framework.exceptions import ValidationError


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
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('performance', 'row', 'seat_number')

    def clean(self):
        self.validate_seat()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def validate_seat(self):
        hall = self.performance.theatre_hall

        if self.row < 1 or self.row > hall.rows:
            raise ValidationError("Row number out of range.")

        if self.seat_number < 1 or self.seat_number > hall.seats_per_row:
            raise ValidationError("Seat number out of range.")

    def __str__(self):
        return f"Seat {self.seat_number} in row {self.row} for {self.performance}"


class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='plays')
    genres = models.ManyToManyField(Genre, related_name='plays')

    def __str__(self):
        return self.title


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100)  #TODO: Change to ForeignKey to User model when created

    def __str__(self):
        return f"Reservation {self.id} by {self.user} at {self.created_at}"
