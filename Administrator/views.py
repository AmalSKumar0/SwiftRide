from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import *
from user.models import *
from driver.models import *
from datetime import timedelta
from django.utils.timezone import now
from collections import defaultdict
from django.utils.timezone import localtime

def dashboard(request):
    if request.method == "POST":
        vehicle_prices = VehiclePrice.objects.all()

        for index, vehicle in enumerate(vehicle_prices, start=1):
            base_distance = request.POST.get(f"base_distance_{index}")
            rate_per_km = request.POST.get(f"rate_per_km_{index}")
            commission_rate = request.POST.get(f"commission_rate_{index}")

            if base_distance and rate_per_km and commission_rate:
                vehicle.base_distance = float(base_distance)
                vehicle.rate_per_km = float(rate_per_km)
                vehicle.commission_rate = float(commission_rate)
                vehicle.save()
        messages.success(request,'Price Updated')

    data_price = VehiclePrice.objects.all()
    user = User.objects.all()
    driver = user.filter(rights='driver').count()
    us = user.filter(rights='user').count()
    vehicle = Vehicle.objects.all().count()
    review = Review.objects.all().count()

    last_7_days = now() - timedelta(days=7)
    new_driver = user.filter(rights='driver', created_at__gte=last_7_days).count()
    new_user = user.filter(rights='user', created_at__gte=last_7_days).count()
    trip = Trip.objects.all().count()
    new_review = Review.objects.filter(created_at__gte=last_7_days).count()

    
    trip_details = Trip.objects.all()
    data_graph = defaultdict(int)

    for i in range(10):
        day = now() - timedelta(days=i)
        day_start = localtime(day).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = localtime(day).replace(hour=23, minute=59, second=59, microsecond=999999)
        count = trip_details.filter(requested_at__range=(day_start, day_end)).count()
        data_graph[day_start.date()] = count

    # Sort by date ascending
    sorted_data = dict(sorted(data_graph.items()))

    trip_today = trip_details.filter(requested_at__date=now().date())
    t1 = trip_today.filter(status='completed').count()
    t2 = trip_today.filter(status='cancelled').count()
    t3 = trip_today.filter(status='requested').count() 

    labels = [date.strftime("%b %d") for date in sorted_data.keys()]  # Ex: "Apr 16"
    data = list(sorted_data.values())
    return render(request, 'Administrator/admin-view.html',{'label':labels,'data':data,'new_driver':new_driver,'new_user':new_user,'trip':trip,'new_review':new_review,'flag':1,'data_price':data_price,'driver':driver,'us':us,'vehicle':vehicle,'review':review,'t1':t1,'t2':t2,'t3':t3})

def new_driver(request):
    drivers = User.objects.filter(rights = 'driver',approved=False)
    for driver in drivers:
        vehicle = Vehicle.objects.get(user = driver.id)
        driver.license_number = vehicle.license_number
        driver.vehicle_type = vehicle.vehicle_type
    return render(request, 'Administrator/newDrivers.html', {'drivers': drivers,'flag':2})

def accept_driver(request, id):
    driver = User.objects.get(id=id)
    driver.approved = True
    driver.save()
    messages.success(request, 'Driver has been approved')
    return redirect('newDriver')

def delete_driver(request, id):
    driver = User.objects.get(id=id)
    driver.delete()
    messages.success(request, 'Driver has been removed')
    return redirect('allDrivers')

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'User has been removed')
    return redirect('allPassengers')

def delete_trip(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    messages.success(request, 'Trip has been removed')
    return redirect('allTrips') 

def all_driver(request):
    drivers = User.objects.filter(rights = 'driver',approved=True)
    for driver in drivers:
        if not Vehicle.objects.filter(user = driver.id).first():
             driver.license_number = None
             driver.vehicle_number = None
        else:
             vehicle = Vehicle.objects.filter(user = driver.id).first()
             driver.license_number = vehicle.license_number
             driver.vehicle_number = vehicle.vehicle_number
    
    return render(request, 'Administrator/all_driver.html', {'drivers': drivers,'flag':2})

def all_passenger(request):
    users = User.objects.filter(rights = 'user')
    return render(request, 'Administrator/all_passenger.html', {'users':users,'flag':3})

def all_vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'Administrator/all_vehicles.html', {'flag':4,'vehicles':vehicles})

def all_trips(request):
    trips = Trip.objects.all()
    return render(request, 'Administrator/all_trips.html', {'flag':5,'trips':trips})

def all_review(request):
    reviews = Review.objects.all()
    return render(request, 'Administrator/all_reviews.html', {'reviews':reviews,'flag':6})

def all_revenue(request):
    return render(request, 'Administrator/all_revenues.html', {'flag':7})

def deleteReview(request,id):
   review = Review.objects.get(id=id)
   review.delete()
   messages.success(request,'Review is deleted')
   return redirect('allReviews')