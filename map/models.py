from django.db import models

# Create your models here.

class Drone(models.Model):
    name = models.CharField(max_length=100)  # Name or identifier of the drone
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class DroneData(models.Model):
    drone = models.ForeignKey(Drone, related_name='data', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()

    def __str__(self):
        return f"{self.drone.name} at {self.timestamp}"