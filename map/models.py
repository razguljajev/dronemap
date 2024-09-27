from django.db import models

# Create your models here.

class DroneData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.timestamp}: {self.latitude}, {self.longitude}, {self.altitude}"