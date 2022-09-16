import requests
import json
from .models import *
from requests.auth import HTTPBasicAuth
from django.http import Http404
from django.shortcuts import get_object_or_404
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time


# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    try:
        if 'api' in kwargs:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                     auth=HTTPBasicAuth('apikey', api_key))
            print(response,'api')
        elif kwargs:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
            print(params,"second")
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'})
            print('third')

    except Exception as e:
        
        print("Network exception occurred")
        
    status_code=response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function

# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,**kwargs)
    #print(json_result,"first")
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["row"]

        #print(dealers,"second")
        # For each dealer object
        #for dealer in dealers:
        for dealer in json_result:    
            # Get its content in `doc` object
            #dealer_doc = dealer["body"]
            #dealer_doc =json_result
            dealer_doc =dealer
            #print(dealer,"dealr")
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
#def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def get_dealer_from_cf_by_id(url, dealer_id):
    json_result = get_request(url, id=dealer_id)
    if json_result:
        print(json_result,'dealer_get')
        dealer = json_result[0]
        
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
    return dealer_obj


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, id=dealer_id)
    print(json_result,"dealer_id")
    if json_result:
        reviews = json_result
        for review in reviews:
            if review["purchase"]:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date=review["purchase_date"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"],
                    sentiment=analyze_review_sentiments(review["review"]),
                    id=review['id']
                )
            else:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date=None,
                    car_make=None,
                    car_model=None,
                    car_year=None,
                    sentiment=analyze_review_sentiments(review["review"]),
                    id=review['id']
                )
            results.append(review_obj)
    return results


def analyze_review_sentiments(dealer_review):
    API_KEY = "ASpAllqPyaDFSNxSG2Khl3t0rX9rB0W1IXyiDzcyGjL3"
    NLU_URL = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/b022da2f-9737-4658-b8dd-4e94d705dad4'
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(text=dealer_review, features=Features(
        sentiment=SentimentOptions(targets=[dealer_review]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)


