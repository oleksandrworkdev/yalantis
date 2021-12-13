from django.urls import path

from . import views

app_name = 'cars_park_api'
urlpatterns = [
    path('drivers/driver/', views.driver_index, name='driver_index'),
    path('drivers/driver/<int:driver_id>/', views.driver_detail, name='driver_detail'),
    path('vehicles/vehicle/', views.vehicle_index, name='vehicle_index'),
    path('vehicles/vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/set_driver/<int:vehicle_id>/', views.vehicle_set_driver, name='vehicle_set_driver')
]
