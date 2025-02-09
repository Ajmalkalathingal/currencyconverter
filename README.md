# currencyconverter
1. Setup and Installation

1 Prerequisites

Python (3.11 recommended)


2
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows

3
pip install -r requirements.txt

4
Create a .env file in the project root and add:  OPEN_EXCHANGE_API_KEY=your_api_key_here

5
python manage.py migrate


2. API Endpoints

2.1 Get Exchange Rates
Endpoint: GET /rates/
Query Params: (Optional) ?base=USD

curl -X GET "http://127.0.0.1:8000/rates/?base=EUR"

Response:
{
    "base_currency": "EUR",
    "rates": {
        "USD": 1.1,
        "GBP": 0.85
    }
}


2.2 Convert Currency
Endpoint: POST /convert/
Request Body (JSON):
{
    "from": "USD",
    "to": "EUR",
    "amount": 100
}

Example Request: curl -X POST "http://127.0.0.1:8000/convert/" \
     -H "Content-Type: application/json" \
     -d '{"from": "USD", "to": "EUR", "amount": 100}'


response
{
    "from_currency": "USD",
    "to_currency": "EUR",
    "amount": 100,
    "converted_amount": 85.0
}


3. Running Tests
Ensure pytest is installed:  pip install pytest pytest-django

run test: pytest
