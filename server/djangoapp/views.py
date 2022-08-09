from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_from_cf_by_id
from django.contrib.auth import login, logout, authenticate
import logging
from datetime import datetime
from .models import CarModel

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
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_from_cf_by_id(url, dealer_id)
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars
        context["dealer"] = dealer
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        url = "https://83647813.us-south.apigw.appdomain.cloud/dealershipapi/review/?dealerId=" + \
            str(dealer_id)
        cars = CarModel.objects.filter(dealerId=dealer_id)
        for car in cars:
            if car.id == int(request.POST['car']):
                review_car = car

        print(review_car.year.strftime("%Y"))
        #url = body['url']

        if 'purchasecheck' in request.POST:
            was_purchased = True
        else:
            was_purchased = False
        print(was_purchased)
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.POST['name']
        review["dealership"] = 13
        review["review"] = request.POST['content']
        review["id"] = dealer_id
        review["purchase"] = was_purchased
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = review_car.car.name
        review["car_model"] = review_car.name
        review["car_year"] = review_car.year.strftime("%Y")
        json_payload = {}
        json_payload["review"] = review
        response = post_request(url, json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
