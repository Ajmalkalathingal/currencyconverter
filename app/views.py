import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Open Exchange Rates API URL
EXCHANGE_API_URL = "https://openexchangerates.org/api/latest.json"

@api_view(["GET"])
def get_exchange_rates(request):
    base_currency = request.GET.get("base", "USD")  # Default base: USD

    params = {
        "app_id": settings.OPEN_EXCHANGE_API_KEY,  # Use  API key from settings
        "base": base_currency
    }

    try:
        response = requests.get(EXCHANGE_API_URL, params=params)
        response.raise_for_status()  # Raise error if status_code != 200
        data = response.json()

        if "error" in data:
            return Response({"error": data["error"]}, status=400)

        return Response({"base_currency": base_currency, "rates": data.get("rates", {})})

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)




