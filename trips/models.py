from django.db import models


from django.db import models

class Trip(models.Model):
    driver_name = models.CharField(max_length=100, default="Unknown")
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    cycle_hours_used = models.FloatField(default=0)
    start_date = models.DateField(auto_now_add=True)

class ELDLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField()
    driving_hours = models.FloatField()
    rest_hours = models.FloatField()
    pickup_dropoff_hours = models.FloatField()
