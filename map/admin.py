from django.contrib import admin
from .models import Drone, DroneData

# Register your models here.

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Adjust fields as necessary

@admin.register(DroneData)
class DroneDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'drone', 'timestamp', 'latitude', 'longitude', 'altitude')