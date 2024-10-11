from django.shortcuts import render

# Create your views here.
import csv
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import DroneData
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import pytz 

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Drone, DroneData
from .serializers import DroneDataSerializer

from math import radians, sin, cos, sqrt, atan2

from django.shortcuts import render


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Extract drone name from the CSV file name (without extension)
            drone_name = csv_file.name.rsplit('.', 1)[0]

            # Check if the drone already exists, or create a new one
            drone, created = Drone.objects.get_or_create(name=drone_name)

            # Parse the CSV file
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip the header

            for row in reader:
                naive_datetime = parse_datetime(row[0])  # Parse the timestamp from the first column
                if naive_datetime is not None:
                    # Make the datetime aware (add timezone information)
                    aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.UTC)

                    # Assume the CSV format: timestamp, latitude, longitude, altitude
                    DroneData.objects.create(
                        drone=drone,  # Associate the data point with the drone
                        timestamp=aware_datetime,
                        latitude=row[1],
                        longitude=row[2],
                        altitude=row[3]
                    )

            return redirect('success')
    else:
        form = CSVUploadForm()

    return render(request, 'drones/upload.html', {'form': form})

@api_view(['GET'])
def get_available_drones(request):
    drones = Drone.objects.all().values('id', 'name') 
    return Response(list(drones))

@api_view(['GET'])
def get_drone_data(request):
    data = DroneData.objects.all()
    serializer = DroneDataSerializer(data, many=True)
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [d['longitude'], d['latitude']]
                },
                "properties": {
                    "altitude": d['altitude'],
                    "timestamp": d['timestamp']
                }
            } for d in serializer.data
        ]
    }
    return Response(geojson_data)

def map_view(request):
    return render(request, 'map/map.html')

def success_view(request):
    return render(request, 'general/success.html')

@api_view(['GET'])
def replay_drone_data(request, drone_id):
    drone_data = DroneData.objects.filter(drone__id=drone_id).order_by('timestamp')
    features = []
    
    for data in drone_data:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data.longitude, data.latitude],
            },
            "properties": {
                "altitude": data.altitude,
                "timestamp": data.timestamp.isoformat(),
            }
        })
    
    return Response({"type": "FeatureCollection", "features": features})

# Function to calculate distance using the Haversine formula
def haversine(coord1, coord2):
    R = 6371.0  # Radius of the Earth in kilometers
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Distance in kilometers

    return distance

@api_view(['POST'])
def measure_distance(request):
    drone1_id = request.data.get('drone1_id')
    drone2_id = request.data.get('drone2_id')

    if drone1_id and drone2_id:
        drone1 = Drone.objects.get(id=drone1_id)
        drone2 = Drone.objects.get(id=drone2_id)

        # Calculate distance
        distance = haversine((drone1.latitude, drone1.longitude), (drone2.latitude, drone2.longitude))

        return Response({'distance': distance}, status=200)
    return Response({'error': 'Invalid drone IDs'}, status=400)
