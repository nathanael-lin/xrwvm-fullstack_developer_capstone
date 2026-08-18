import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username})


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data["userName"]
    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=data["firstName"],
        last_name=data["lastName"],
        password=data["password"],
        email=data["email"],
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"})


def get_cars(request):
    if not CarMake.objects.exists():
        initiate()
    cars = [
        {"CarModel": model.name, "CarMake": model.car_make.name}
        for model in CarModel.objects.select_related("car_make")
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint) or []
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    dealer = get_request(f"/fetchDealer/{dealer_id}")
    return JsonResponse({"status": 200, "dealer": dealer})


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}") or []
    for review in reviews:
        text = review.get("review", review.get("reviewText", ""))
        sentiment = analyze_review_sentiments(text) if text else None
        if isinstance(sentiment, dict):
            review["sentiment"] = sentiment.get("sentiment", sentiment.get("label"))
        else:
            review["sentiment"] = sentiment
    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "POST required"}, status=405)
    try:
        post_review(json.loads(request.body))
        return JsonResponse({"status": 200})
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({"status": 400, "message": "Invalid review data"}, status=400)
    except Exception:
        logger.exception("Error posting review")
        return JsonResponse({"status": 401, "message": "Error in posting review"}, status=401)
