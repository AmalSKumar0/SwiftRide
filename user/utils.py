import os
import json
import requests
from math import radians, sin, cos, sqrt, atan2
import random
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
from opencage.geocoder import OpenCageGeocode
from Administrator.models import VehiclePrice

# Mock cache function (you should replace it with actual cache logic)
def get_cache(place):
    # Simulate a cache lookup
    return None

# Function to fetch data from OpenCage API
def fetch_place_data(place, api_key):
    cached = get_cache(place)
    if cached:
        return cached  # Return cached result if available

    # URL encoding and constructing the OpenCage API URL
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': place,
        'key': api_key,
        'limit': 1
    }
    # Encode the parameters for the URL
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        response = requests.get(url, timeout=5)  # 5 seconds timeout
        return response.json()
    except requests.RequestException as e:
        return None  # Handle error (e.g., timeout or network issues)

# Main function to handle multiple places concurrently
def get_geocode_data(place, api_key):
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(place)  # Pass the place directly, no need for formatting
    
    if results and len(results) > 0:  # Ensure results are available
        lat = results[0]['geometry']['lat']
        lon = results[0]['geometry']['lng']
        return (lat, lon)  # Return as a tuple
    else:
        return None  # Return None if no results are found


    
def haversine_distance(coord1, coord2):
    """
    Calculate the great-circle distance between two points on the Earth
    specified in decimal degrees (latitude and longitude).
    """
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in kilometers
    earth_radius = 6371.0
    distance = earth_radius * c

    return round(distance)

# Function to get distance between two places
def get_distance_between_places(place1, place2):
    api_key = '7a3a0c1b40264ee896db8d29b4f3c388'
    coord1 = get_geocode_data(place1, api_key)
    coord2 = get_geocode_data(place2, api_key)

    if coord1 and coord2:  # Ensure both coordinates are valid
        return haversine_distance(coord1, coord2)
    else:
        return None  

def calculate_trip_price(distance):
    if not isinstance(distance, (int, float)):
        return {"error": "Invalid input: Distance must be a numeric value."}

    choices = ['Auto Rickshaw', 'Economy Car', 'Sedan', 'Luxury Car']
    price_list = {}

    # Fetch all vehicle prices in one query
    vehicle_prices = {vp.vehicle_type: vp for vp in VehiclePrice.objects.filter(vehicle_type__in=choices)}

    for choice in choices:
        pri = vehicle_prices.get(choice)  # Get vehicle price object if available
        if pri:
            base_fare = pri.base_fare
            base_distance = pri.base_distance
            rate_per_km = pri.rate_per_km
            commission_rate = pri.commission_rate

            if distance <= base_distance:
                fare = base_fare  
            else:
                additional_distance = distance - base_distance
                fare = base_fare + (additional_distance * rate_per_km)

            commission = fare * commission_rate
            total_price = round(fare + commission)

            price_list[choice] = total_price
        else:
            price_list[choice] = 0  # If vehicle price doesn't exist, return 0

    return price_list
 

def generate_otp(length=6):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

