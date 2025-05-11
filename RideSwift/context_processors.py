from django.shortcuts import *
from django.http import HttpResponse
from django.contrib import messages
from Administrator.models import *
from driver.models import *
from user.models import *

def common_data(request):
    login = False
    user = None 
    login = "userid" in request.session
    driver = None
    logdr = "driverid" in request.session
    if logdr:
        driver_id = request.session.get("driverid")
        driver = User.objects.get(id=driver_id)
    if login:
        user_id = request.session.get("userid")
        user = User.objects.get(id=user_id)
    return {
        "login": login,
        "user": user,
        "logdr": logdr,
        "driver":driver
    }