from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from Administrator.models import *
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from .forms import *
from .utils import *
from .models import *

def userReg(request):
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, "Password do not match.")
            return render(request,'user/signup.html')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_no = request.POST.get('phone')
        rights = 'user'
        try:
            user = User.objects.create(
                name = name,
                email = email,
                address = address,
                phone_no = phone_no,
                password = password,
                rights = rights,
                approved = True
            )
            messages.success(request, "User created successfully.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Failed to create user.")
    return render(request,'user/signup.html')


def userHome(request):
    user = User.objects.get(id=request.session['userid'])
    try:
        trip = Trip.objects.get(passenger=user, isFinished=False)
        if trip:
            return redirect('booking_status')
    except Trip.DoesNotExist:
        trip = None

    if request.method == "POST":
        searchForm = searchAuto(request.POST)
        if searchForm.is_valid():
            data = searchForm.cleaned_data
            from_loc = data['from_loc']
            to_loc = data['to_loc']
            landmark = data['landmark']
            available_vehicles = Vehicle.objects.filter(
                is_active=True,
                current_location=from_loc
            ).select_related('user')

            if not available_vehicles.exists():
                messages.error(request, "No Taxi Available.")
                searchForm = searchAuto()
                return render(request,'user/user-home.html',{'searchForm': searchForm})
            
            dis = get_distance_between_places(from_loc, to_loc)
            price = calculate_trip_price(dis)
            
            request.session['from_location']=from_loc
            request.session['to_location']=to_loc
            request.session['landmark']=landmark
            request.session['dis']=dis
            request.session['price']=price
            return redirect('search_Auto')
    searchForm = searchAuto()
    return render(request,'user/user-home.html',{'searchForm': searchForm})


def search_Auto(request):
        from_loc,dis,vehicles = driversearcher(request)
        searchForm = searchAuto()
        obj = {}
        booked = False
        if 'BookDriver' in request.GET:
            vehicle = Vehicle.objects.get(id=request.session['id'])
            booked_vehicle = vehicle
            driver = User.objects.get(id=booked_vehicle.user.id)
            user = User.objects.get(id=request.session['userid'])
            status = 'requested'
            requested_at = now()
            from_location = request.session['from_location']
            to_location = request.session['to_location']
            landmark = request.session['landmark']
            distance = request.session['dis']
            fare = request.session['price'][vehicle.vehicle_type]
 
        
            trip = Trip.objects.create(
            passenger = user,
            driver = driver,
            vehicle = booked_vehicle,
            from_location = from_location,
            to_location = to_location,
            landmark = landmark,
            status = status,
            otp = generate_otp(),
            fare = fare,
            distance = distance,
            requested_at = now()
            )
            request.session['booking'] = trip.id
            return redirect('booking_status')
        viewTaxi = False
        if 'viewProfile' in request.GET:
            id = request.GET.get('viewProfile')
            vehicle = Vehicle.objects.get(id=id)
            driver = User.objects.get(id = vehicle.user.id)
            price = request.session['price'][vehicle.vehicle_type]
            obj['driver'] = driver
            obj['vehicle'] = vehicle
            review = Review.objects.filter(driver=driver)
            temp = 0
            for re in review:
                temp += re.rating
            rating = temp / len(review) if len(review) > 0 else 0
            obj['rating'] = int(rating)
            obj['review'] = review
            obj['price'] = price
            viewTaxi = True

        if 'look' in request.GET:
            id = request.GET.get('look')
            vehicle = Vehicle.objects.get(id=id)
            driver = User.objects.get(id = vehicle.user.id)
            price = request.session['price'][vehicle.vehicle_type]
            request.session['id'] = id
            booked = True
            from_location = request.session['from_location']
            to_location = request.session['to_location']
            landmark = request.session['landmark']
            distance = request.session['dis']
            review = Review.objects.filter(driver=driver)
            temp = 0
            for re in review:
                temp += re.rating
            rating = temp / len(review) if len(review) > 0 else 0
            obj['rating'] = int(rating)
            obj['lookupdriver'] = driver
            obj['lookupvehicle'] = vehicle
            obj['lookupprice'] = price
            obj['lookupfrom'] = from_location.split(',')[0] if from_location else ''
            obj['lookupto'] = to_location.split(',')[0] if to_location else ''
            obj['lookuplandmark'] = landmark
            obj['lookupdistance'] = distance
            obj['lookupfare'] = price
            viewTaxi = False
            
        if 'Back' in request.GET:
            booked = False
            return redirect('search_Auto')
        return render(request,'user/options.html',{'viewTaxi':viewTaxi,'booked':booked,'obj':obj,'searchForm':searchForm,'vehicles': vehicles,'location':from_loc,'dis':dis,'to':request.session['to_location'],'land':request.session['landmark']})   

def driversearcher(request):
    available_vehicles = Vehicle.objects.filter(
                current_location=request.session.get('from_location'),
                user__is_active=True
            ).select_related('user')
    from_loc = request.session['from_location']
    dis = request.session['dis']
    price = request.session['price']

    if not available_vehicles:
        available_vehicles = Vehicle.objects.filter(
                is_active=True,
                current_location=from_loc
            ).select_related('user')
    
    vehicles = []
    categories = ['Auto Rickshaw', 'Economy Car', 'Sedan', 'Luxury Car']
    for category in categories:
        filtered_vehicles = available_vehicles.filter(vehicle_type=category).first()
        if filtered_vehicles:
            filtered_vehicles.price = price[category]
            vehicles.append(filtered_vehicles)
    return from_loc,dis,vehicles

def logout_view(request):
    if "userid" in request.session:
        del request.session["userid"]  
    return redirect("home") 



def booking_status(request):
    user_id = request.session.get('userid')
    if not user_id:
        return redirect('login')  # Redirect if session is missing

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')  # Redirect if user not found

    reviewFlag = False
    trip = Trip.objects.filter(passenger=user, isFinished=False).first()
    
    if not trip:
        return redirect('search_Auto')  # Redirect if no ongoing trip

    if 'cancel' in request.GET:
        trip.isFinished = True
        trip.save()
        return redirect('search_Auto')

    if 'confirmTrip' in request.GET:
        trip.isFinished = True
        trip.save()
        return redirect('search_Auto')
    
    if 'review' in request.GET:
        reviewFlag = True
        if request.method == 'POST':
            trip = Trip.objects.get(id=request.POST.get('trip_id'))
            rating = request.POST.get('feedback')
            review = request.POST.get('review_text')
            r = Review.objects.create(
                passenger = trip.passenger,
                driver = trip.driver,
                vehicle = trip.vehicle,
                rating = rating,
                comment = review
            )
            messages.success(request, "Review submitted")
            return redirect('booking_status')

    trip.from_location = trip.from_location.split(',')[0] if trip.from_location else ''
    trip.to_location = trip.to_location.split(',')[0] if trip.to_location else ''

    return render(request, 'user/booked.html', {'trip': trip, 'reviewFlag': reviewFlag})


def passengerProfile(request):
    user = User.objects.get(id=request.session['userid'])
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.address = request.POST.get('address')
        user.phone_no = request.POST.get('phone')
        user.save()
        messages.success(request, "Profile updated successfully.")
    return render(request, 'user/profile/editptofile.html', {'driver': user,'pg':1})

def history(request):
    user = User.objects.get(id=request.session['userid'])
    trips = Trip.objects.filter(passenger=user)
    distance = 0
    price = 0
    for trip in trips:
        distance+=trip.distance
        price+=trip.fare

    return render(request, 'user/profile/triphistory.html', {'pg':2,'trips':trips,'distance':distance,'price':price})


def reviewsOfUser(request):
    user = User.objects.get(id=request.session['userid'])
    reviews = Review.objects.filter(passenger=user)
    return render(request, 'user/profile/yourreviews.html', {'pg': 5, 'reviews': reviews})

def deleteReview(request,id):
   review = Review.objects.get(id=id)
   review.delete()
   messages.success(request,'Review is deleted')
   return redirect('reviewsOfUser')
