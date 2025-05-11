from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('Driver-Signin/',driverReg,name="driverSignup"),
    path('Driver-not-approved/',notapproved,name="notapproved"),
    path('driver-dashboard/', driverHome ,name="driverDashboard"),
    path('driver-on-duty/', driverOnDuty ,name="driverOnDuty"),
    path('accept_user/<int:id>/',accept_user,name="accept_user"),
    path('reject_user/<int:id>/',reject_user,name="reject_user"),
    path('booking-view',booking_view,name="bookingView"),
    path('driver-profile/', driverProfile ,name="driverProfile"),
    path('trip-history/',history,name="historytrip"),
    path('driverVehicles/',DrVehicles,name="driverVehicles"),
    path('editVehicles/<int:id>',editVehicle,name="editVehicles"),
    path('add-vehicles/',addVehicle,name="addVehicle"),
    path('updateVehicle/<int:id>',setprimaryVehicle,name="updateVehicle"),
    path('deleteVehicle/<int:id>',deleteVehicle,name="deleteVehicle"),
    path('reviewsOfDriver/',reviewsOfDriver,name="reviewsOfDriver"),
    path('logoutDriver/',logout,name="logoutDriver"),
]