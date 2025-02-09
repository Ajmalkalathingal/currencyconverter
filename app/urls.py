from django.urls import path
from .views import get_exchange_rates
urlpatterns = [
    path("rates/", get_exchange_rates, name="get_rates"),
]
