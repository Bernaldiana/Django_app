from django.db import models


class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.vehicle_id
