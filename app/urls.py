from django.urls import path
from .views import get_exchange_rates, convert_currency

urlpatterns = [
    path("rates/", get_exchange_rates, name="get_rates"),
    path("convert/", convert_currency, name="convert_currency"),
]
