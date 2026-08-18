from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "djangoapp"

urlpatterns = [
    path("register", views.registration, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("get_cars", views.get_cars, name="getcars"),
    path("get_dealers", views.get_dealerships, name="get_dealers"),
    path(
        "get_dealers/<str:state>",
        views.get_dealerships,
        name="get_dealers_by_state",
    ),
    path(
        "get_dealer/<int:dealer_id>",
        views.get_dealer_details,
        name="get_dealer_details",
    ),
    path(
        "get_dealer/<int:dealer_id>/reviews",
        views.get_dealer_reviews,
        name="get_dealer_reviews",
    ),
    # Aliases used by the Dealer React component.
    path(
        "dealer/<int:dealer_id>",
        views.get_dealer_details,
        name="dealer_details",
    ),
    path(
        "reviews/dealer/<int:dealer_id>",
        views.get_dealer_reviews,
        name="reviews_by_dealer",
    ),
    path("add_review", views.add_review, name="add_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
