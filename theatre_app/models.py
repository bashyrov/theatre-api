from django.db import models

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

