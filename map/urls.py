from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('api/drone_data/', views.get_drone_data, name='get_drone_data'),
    path('map/', views.map_view, name='map_view'),
    path('success/', views.success_view, name='success'),
    path('api/replay/', views.replay_drone_data, name='replay_drone_data')
]