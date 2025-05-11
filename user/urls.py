from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('User-Signin/',userReg,name="userSignup"),
    path('user-home/',userHome,name="userDashboard"),
    path('search-taxi/',search_Auto,name="search_Auto"),
    path('logout/',logout_view,name="logout"),
    path('booking-status/',booking_status,name="booking_status"),
    path('profile-user/',passengerProfile,name="passengerProfile"),
    path('history-user/',history,name="userhistory"),
    path('user-review/',reviewsOfUser,name="reviewsOfUser"),
    path('deleteReview/<int:id>',deleteReview,name="deleteReview")
]