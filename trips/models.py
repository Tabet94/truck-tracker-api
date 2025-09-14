from django.db import models
import requests


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": self.name,
                "format": "json",
                "limit": 1
            }
            response = requests.get(url, params=params, headers={"User-Agent": "Django-App"})
            if response.status_code == 200 and response.json():
                data = response.json()[0]
                self.latitude = float(data["lat"])
                self.longitude = float(data["lon"])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


class Trip(models.Model):
    driver_name = models.CharField(max_length=100, default="Unknown")
    current_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="current_trips"
    )
    pickup_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="pickup_trips"
    )
    dropoff_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="dropoff_trips"
    )
    cycle_hours_used = models.FloatField(default=0)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Trip by {self.driver_name} from {self.pickup_location} to {self.dropoff_location}"


class ELDLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    driving_hours = models.FloatField()
    rest_hours = models.FloatField()
    pickup_dropoff_hours = models.FloatField()

    def __str__(self):
        return f"Log for {self.trip.driver_name} on {self.date}"
