from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from Administrator.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404

def home(request):
    # for testing
    # if 'userid' in request.session:
    #     user = User.objects.get(id=request.session['userid'])
    #     if user.rights == "admin":
    #         return redirect('adminDashboard')
    #     elif user.rights == "driver" and user.approved:
    #         return redirect('driverDashboard')
    #     elif user.rights == "user":
    #         return redirect('userDashboard')
    return render(request,'home.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.password == password:
                
                if user.rights == "admin":
                    messages.success(request, "Login successfully.")
                    return redirect('adminDashboard')
                elif user.rights == "driver":
                    request.session['driverid'] = user.id 
                    messages.success(request, "Login successfully.")
                    if not user.approved:
                        return redirect('notapproved')
                    return redirect('driverDashboard')
                elif user.rights == "user":
                    request.session['userid'] = user.id
                    messages.success(request, "Login successfully.")
                    return redirect('userDashboard')
                else: 
                    return redirect('home')
            else:
                messages.error(request, "Invalid Password.")
        except User.DoesNotExist:
            messages.error(request, "User not found.") 
    users = User.objects.all()
    print(users[0].email)
    return render(request,'signin.html',{'users': users})