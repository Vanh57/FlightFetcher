import azure.functions as func
import datetime
import logging
import requests
import os
import json

app = func.FunctionApp()

@app.timer_trigger(
    schedule="0 */2 * * * *",  # Runs every 2 minutes
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False
)
def FetchFlightData(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")
    
    logging.info("Timer trigger function started at %s", datetime.datetime.utcnow())

    # Fetch flight data from AviationStack
    API_KEY = os.getenv("AVIATIONSTACK_API_KEY")  # Retrieve from environment variable
    base_url = "https://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "flight_status": "active",
        "limit": 10  # Example: fetch 10 flights
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception on a bad HTTP status
        data = response.json()

        logging.info("=== AviationStack Data ===")
        # Log out partial flight info
        # for flight in data.get("data", []):
        #     flight_info = {
        #         "flight_number": flight.get("flight", {}).get("iata"),
        #         "departure_airport": flight.get("departure", {}).get("airport"),
        #         "arrival_airport":  flight.get("arrival", {}).get("airport"),
        #         "status":           flight.get("flight_status")
        #     }
        logging.info(json.dumps(data, indent=2))

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    logging.info("Timer trigger function completed.")
