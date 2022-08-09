from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_from_cf_by_id
from django.contrib.auth import login, logout, authenticate
import logging

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
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/review/"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews"] = reviews
        dealer = get_dealer_from_cf_by_id(
            "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/dealership", dealer_id)
        print(dealer)
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
