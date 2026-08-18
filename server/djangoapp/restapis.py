import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", "http://localhost:3030").rstrip("/")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", "http://localhost:5050/"
).rstrip("/") + "/"


def get_request(endpoint, **kwargs):
    """GET JSON data from the Express backend."""
    url = f"{backend_url}/{endpoint.lstrip('/')}"
    try:
        response = requests.get(url, params=kwargs or None, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as err:
        print(f"GET request failed for {url}: {err}")
        return None


def analyze_review_sentiments(text):
    """Return sentiment analysis for review text."""
    url = f"{sentiment_analyzer_url}analyze/{quote(str(text), safe='')}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as err:
        print(f"Sentiment request failed: {err}")
        return None


def post_review(data_dict):
    """Submit a dealer review to the Express backend."""
    url = f"{backend_url}/insert_review"
    try:
        response = requests.post(url, json=data_dict, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as err:
        print(f"POST request failed for {url}: {err}")
        raise
