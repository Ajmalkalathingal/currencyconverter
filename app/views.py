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



# Convert amount from one currency to another
@api_view(["POST"])
def convert_currency(request):
    from_currency = request.data.get("from", "USD")  # Default: USD
    to_currency = request.data.get("to")
    amount = float(request.data.get("amount", 0))

    if not to_currency or amount <= 0:
        return Response({"error": "Invalid request parameters"}, status=400)

    params = {
        "app_id": settings.OPEN_EXCHANGE_API_KEY,
        "base": from_currency
    }

    try:
        response = requests.get(EXCHANGE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates", {})
        conversion_rate = rates.get(to_currency)

        if not conversion_rate:
            return Response({"error": "Invalid target currency"}, status=400)

        converted_amount = amount * conversion_rate
        return Response({
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": round(converted_amount, 2)
        })

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

