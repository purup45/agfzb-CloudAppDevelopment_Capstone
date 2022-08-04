import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as e:
        print("Error " ,e)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result["body"]
        for review in reviews:
            review_doc = review["doc"]
            if "purchase_date" in review_doc:
                review_obj = DealerReview(
                    dealership=review_doc["dealership"],
                    name=review_doc["name"],
                    purchase=review_doc["purchase"],
                    review=review_doc["review"],
                    purchase_date=review_doc["purchase_date"],
                    car_make=review_doc["car_make"],
                    car_model=review_doc["car_model"],
                    car_year=review_doc["car_year"],
                    sentiment=analyze_review_sentiments(review_doc["review"]),
                    id=review_doc['id']
                    )
                results.append(review_obj)
    return results


def analyze_review_sentiments(text):
    API_KEY="56Uu0KyzSNEZ8u71Q9Nu4eqYmSiLxsMV0otoCXFUCIam"
    NLU_URL='https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/351966a8-a214-4fc1-a319-ea7f066c002c'
    params = json.dumps({"text": text, "features": {"sentiment": {}}})
    response = requests.post(NLU_URL,data=params,headers={'Content-Type':'application/json'},auth=HTTPBasicAuth("apikey", API_KEY))
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"


