from django.db import models

from eld_app.models.driver import Driver
from eld_app.models.vehicle import Vehicle


class ELD(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='eld_records')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='eld_records')
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.driver} - {self.vehicle} - {self.timestamp}"
