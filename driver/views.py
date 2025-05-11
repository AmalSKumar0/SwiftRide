from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from Administrator.models import User, Vehicle  
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from .forms import DriverLocForm
from user.models import *

def driverReg(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, "Password do not match.")
            return render(request, 'driver/signup.html')
        name = request.POST.get('name')
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'driver/signup.html')
        address = request.POST.get('address')
        phone_no = request.POST.get('phone')
        if User.objects.filter(phone_no=phone_no).exists():
            messages.error(request, "Phone no already exists.")
            return render(request, 'driver/signup.html')
        rights = 'driver'
        
        vehicle_type = request.POST.get('vehicle_type')
        manufacture_date = request.POST.get('manufacture_date')
        license_number = request.POST.get('license_number')
        if Vehicle.objects.filter(license_number=license_number).exists():
            messages.error(request, "license already exists.")
            return render(request, 'driver/signup.html')
        vehicle_number = request.POST.get('vehicle_number')
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "vehicle already exists.")
            return render(request, 'driver/signup.html')
        vehicle_image = request.FILES.get('vehicle_image')
        
        try:
            user = User.objects.create(
                name=name,
                email=email,
                address=address,
                phone_no=phone_no,
                password=password,
                rights=rights,
                approved=False
            )
            
            Vehicle.objects.create(
                user=user,
                vehicle_type=vehicle_type,
                manufacture_date=manufacture_date,
                license_number=license_number,
                vehicle_number=vehicle_number,
                vehicle_image=vehicle_image,
                is_active=True
            )
            
            messages.success(request, "registered successfully.")
            return redirect('login')
        except Exception as e:
            messages.error(request, e)
    return render(request, 'driver/signup.html')

def notapproved(request):
    return render(request, 'driver/not_approved.html')

def driverHome(request):
    driver = User.objects.get(id=request.session['driverid'])
    if driver.is_active:
        return redirect('driverOnDuty')
    if not driver.approved:
        return redirect('notapproved')
    if not Vehicle.objects.filter(user=driver, is_active=True).exists():
        messages.error(request, "Please add vehicle.")
        return redirect('driverVehicles')
    if request.method == 'POST':
        driver_location = DriverLocForm(request.POST)
        if driver_location.is_valid():
            location = driver_location.cleaned_data['location']
            request.session['location'] = location
            vehicle = Vehicle.objects.get(user=driver, is_active=True)
            vehicle.current_location = location
            driver.is_active = True
            driver.save()
            vehicle.save() 
            messages.success(request, "You are discoverable.")
            return redirect('driverOnDuty')
    else:
        driver_location = DriverLocForm()
    return render(request, 'driver/driver_home.html',{'form': driver_location,})

def driverOnDuty(request):
    driver = User.objects.get(id=request.session['driverid'])

    if Trip.objects.filter(driver=driver, status='accepted').exists():
        return redirect('bookingView')

    if 'offline' in request.GET:
        vehicle = Vehicle.objects.get(user=driver, is_active=True)
        vehicle.current_location = ""
        driver.is_active = False
        driver.save()
        vehicle.save() 
        return redirect('home')
    
    
    if 'change' in request.GET:
        driver_location = DriverLocForm()
        return render(request, 'driver/driver_home.html',{'form': driver_location,})
    
    trip = Trip.objects.filter(
        driver = driver,
        status = 'requested'
    )
    # messages.success(request, "You are discoverable.")
    data = Vehicle.objects.get(user=driver.id, is_active=True)
    return render(request, 'driver/driver-deployed.html',{
        'booking':trip,
        'data':data,
    })

def booking_view(request):
    driver = User.objects.get(id=request.session['driverid'])
    if not Trip.objects.filter(driver=driver, status="accepted", isFinished="False").exists():
        return redirect('driverOnDuty')
    trip = Trip.objects.get(driver=driver,status = "accepted",isFinished = "False")
    thanks = False
    if 'done' in request.GET:
        messages.success(request,'Trip completed')
        return redirect('driverOnDuty')
    if 'otp' in request.GET:
        if request.GET['otp'] == trip.otp:
            trip.status = "completed"
            trip.completed_at = now()
            trip.save()
            thanks = True
        else:
            messages.success(request,'invalid otp')
    data = Vehicle.objects.get(user=trip.driver, is_active=True)
    trip.from_location = trip.from_location.split(',')[0]
    trip.to_location = trip.to_location.split(',')[0]
    return render(request, 'driver/booking_view.html',{'trip':trip,'data':data,'thanks':thanks})


def accept_user(request, id):
    trip = Trip.objects.get(id=id)
    trip.status = "accepted"
    trip.started_at = now()
    trip.save()
    messages.success(request, "Trip accepted.")
    return redirect('bookingView')

def reject_user(request, id):
    trip = Trip.objects.get(id=id)
    trip.status = "cancelled"
    trip.save()
    messages.success(request, "Trip cancelled.")
    return redirect('driverOnDuty')



# --------------- profile ---------------

def driverProfile(request):
    driver = User.objects.get(id=request.session['driverid'])
    vehicle = Vehicle.objects.get(user=driver.id, is_active=True)
    if request.method == 'POST':
        driver.name = request.POST.get('name')
        driver.email = request.POST.get('email')
        driver.address = request.POST.get('address')
        driver.phone_no = request.POST.get('phone')
        driver.save()
        messages.success(request, "Profile updated successfully.")
    return render(request, 'driver/profile/editptofile.html', {'driver': driver, 'vehicle': vehicle,'pg':1})

def history(request):
    driver = User.objects.get(id=request.session['driverid'])
    trips = Trip.objects.filter(driver=driver)
    distance = 0
    price = 0
    for trip in trips:
        distance+=trip.distance
        price+=trip.fare

    return render(request, 'driver/profile/triphistory.html', {'pg':2,'trips':trips,'distance':distance,'price':price})

def DrVehicles(request):
    driver = User.objects.get(id=request.session['driverid'])
    vehicles = Vehicle.objects.filter(user=driver)
    return render(request,'driver/profile/vehicles.html',{'pg':3,'datas':vehicles})

def editVehicle(request,id):
    vehicle = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        vehicle.vehicle_type = request.POST.get('vehicle_type')
        vehicle.manufacture_date = request.POST.get('manufacture_date')
        vehicle.license_number = request.POST.get('license_number')
        vehicle.vehicle_number = request.POST.get('vehicle_number')
        if 'img' in request.FILES:
            vehicle.vehicle_image = request.FILES['img']
        vehicle.save()
        messages.success(request, "Vehicle details updated successfully.")
        return redirect('driverVehicles')
    return render(request, 'driver/profile/editVehicles.html', {'pg': 3, 'data': vehicle})

def addVehicle(request):
    driver = User.objects.get(id=request.session['driverid'])
    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle_type')
        manufacture_date = request.POST.get('manufacture_date')
        license_number = request.POST.get('license_number')
        vehicle_number = request.POST.get('vehicle_number')
        vehicle_image = request.FILES.get('img')
        
        Vehicle.objects.create(
            user=driver,
            vehicle_type=vehicle_type,
            manufacture_date=manufacture_date,
            license_number=license_number,
            vehicle_number=vehicle_number,
            vehicle_image=vehicle_image,
            is_active=False
        )
        
        messages.success(request, "Vehicle added successfully.")
        return redirect('driverVehicles')
    return render(request, 'driver/profile/addVehicle.html', {'pg': 4})

def setprimaryVehicle(request,id):
    driver = User.objects.get(id=request.session['driverid'])
    # if not Vehicle.objects.filter(user=driver, is_active=True).exists():
    #     v = Vehicle.objects.filter(user=driver).first()
    #     v.is_active=True
    #     v.save()
    #     messages.success(request, "Vehicle set as primary.")
    #     return redirect('driverVehicles')
    vehicles = Vehicle.objects.filter(user=driver, is_active=True)
    if Trip.objects.filter(driver=driver, status='accepted').exists():
        messages.error(request, "You cannot change vehicle.")
        return redirect('driverVehicles')
    if Trip.objects.filter(driver=driver, status='requested').exists():
        for trip in Trip.objects.filter(driver=driver, status='requested'):
            trip.status = 'cancelled'
            trip.save()
    for vehicle in vehicles:
        vehicle.is_active = False
        vehicle.save() 
    vehicle = Vehicle.objects.get(id=id)
    vehicle.is_active = True
    vehicle.current_location = request.session['location']
    vehicle.save()
    messages.success(request, "Vehicle set as primary.")
    return redirect('driverVehicles')

def deleteVehicle(request,id):
    driver = User.objects.get(id=request.session['driverid'])
    vehicle = Vehicle.objects.get(id=id)
    if Trip.objects.filter(driver=driver, status='accepted').exists():
        messages.error(request, "You cannot delete vehicle.")
        return redirect('driverVehicles')
    if Trip.objects.filter(driver=driver, status='requested').exists():
        for trip in Trip.objects.filter(driver=driver, status='requested'):
            trip.status = 'cancelled'
            trip.save()
    if vehicle.is_active:
        newPrimary = Vehicle.objects.filter(user=driver, is_active=False).first()
        if newPrimary:
            newPrimary.is_active = True
            newPrimary.current_location = vehicle.current_location
            newPrimary.save()
        else:
            messages.error(request, "need least two vehicle.")
            return redirect('driverVehicles')
    vehicle.delete()
    messages.success(request, "Vehicle deleted successfully.")
    return redirect('driverVehicles')

def reviewsOfDriver(request):
    driver = User.objects.get(id=request.session['driverid'])
    reviews = Review.objects.filter(driver=driver)
    return render(request, 'driver/profile/yourreviews.html', {'pg': 5, 'reviews': reviews})

def logout(request):
    driver = User.objects.get(id=request.session['driverid'])
    driver.is_active = False
    driver.save()
    try:
        del request.session['driverid']
        messages.success(request, "Logout successfully.")
    except KeyError:
        pass
    return redirect('home')