from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('new-driver/', new_driver, name="newDriver"),
    path('dashboard/',dashboard,name="adminDashboard"),
    path('accept-driver/<int:id>/', accept_driver, name="acceptDriver"),
    path('delete-driver/<int:id>/', delete_driver, name="deleteDriver"),
    path('delete-trip/<int:id>/', delete_trip, name="deleteTrip"),
    path('delete-user/<int:id>/', delete_user, name="deleteUser"),
    path('all-drivers',all_driver,name="allDrivers"),
    path('all-passengers',all_passenger,name="allPassengers"),
    path('all-vehicles',all_vehicles,name="allVehicles"),
    path('all-trips',all_trips,name="allTrips"),
    path('all-reviews',all_review,name="allReviews"),
    path('new-drivers',new_driver,name="newDrivers"),
    path('deleteReview/<int:id>',deleteReview,name="deleteReview1"),
]