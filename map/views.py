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
from .models import DroneData
from .serializers import DroneDataSerializer

from django.shortcuts import render

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Parse the CSV file
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip the header
            for row in reader:
                naive_datetime = parse_datetime(row[0])
                if naive_datetime is not None:
                    aware_datetime = timezone.make_aware(naive_datetime, timezone=pytz.UTC)
                    # Assume CSV format: timestamp, latitude, longitude, altitude
                    DroneData.objects.create(
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
def replay_drone_data(request):
    drone_data = DroneData.objects.all().order_by('timestamp')
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