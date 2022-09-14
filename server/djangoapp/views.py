from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
 return render(request,'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method=="POST":
        print(request.POST['username'])
        print(request.POST['password'])
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user is not None:
            login(request, user)
            
            return render(request,'djangoapp/dealer_details.html')
        
        return render(request,'djangoapp/index.html', {'error':'wrong pwd or username'})

    return render(request,'djangoapp/index.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.method =='GET':
        #print(request.POST.user)
        logout(request)
        #print(user.username)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method=='POST':
        #print(request.POST['password'],request.POST['password2'])
        if request.POST['password']==request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request,'djangoapp/registration.html',{'error':'Username is taken!'})
            except User.DoesNotExist:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
                login(request,user)
                return redirect('djangoapp:dealer')
        else:
            return render(request,'djangoapp/registration.html',{'error':'Password doesnt match'})
    return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request):
    #dealer_id
    return render(request,"djangoapp/dealer_details.html")

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

