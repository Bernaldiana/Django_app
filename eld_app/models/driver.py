from django.db import models


class Driver(models.Model):
    driver_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    driver_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.driver_id})"
