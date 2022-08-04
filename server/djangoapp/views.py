from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to=reverse('admin:index'))
        else:
            return redirect('djangoapp:index')

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    return render(request, 'djangoapp/registration.html')

def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"]=dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context = {}
    url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/review"
    dealer_details = get_dealer_reviews_from_cf(url,dealer_id)
    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    print(context)
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

