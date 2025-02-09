import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_exchange_response():
    return {
        "rates": {"EUR": 0.85, "GBP": 0.75, "INR": 75.0},
        "base": "USD"
    }

@pytest.fixture
def mock_conversion_response():
    return {
        "rates": {"EUR": 0.85},
        "base": "USD"
    }

@patch("requests.get")
def test_get_exchange_rates(mock_get, api_client, mock_exchange_response):
    """Test GET /rates/ endpoint"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_exchange_response

    url = reverse("get_rates")
    response = api_client.get(url)

    assert response.status_code == 200
    assert "rates" in response.data
    assert response.data["base_currency"] == "USD"

@patch("requests.get")
def test_convert_currency(mock_get, api_client, mock_conversion_response):
    """Test POST /convert/ endpoint"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_conversion_response

    url = reverse("convert_currency")
    payload = {"from": "USD", "to": "EUR", "amount": 100}
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 200
    assert response.data["converted_amount"] == 85.0  # 100 * 0.85

def test_convert_currency_invalid_params(api_client):
    """Test invalid conversion request"""
    url = reverse("convert_currency")
    payload = {"from": "USD", "to": "", "amount": 0}
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 400
    assert "error" in response.data
