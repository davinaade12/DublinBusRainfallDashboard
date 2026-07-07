import requests
import xmltodict
import os

def get_rain_bin(rainfall):
    if rainfall == 0:
        return "None"
    elif rainfall <= 1:
        return "Light"
    elif rainfall <= 4:
        return "Moderate"
    else:
        return "Heavy"


def fetch_weather():

    url = os.getenv("MET_FORECAST_URL")

    response = requests.get(url)

    data = xmltodict.parse(response.text)

    times = data["weatherdata"]["product"]["time"]

    rainfall = 0

    forecast_time = ""

    for item in times:

        location = item.get("location")

        if location and "precipitation" in location:

            rainfall = float(location["precipitation"]["@value"])

            forecast_time = item["@from"]

            break

    return {

        "rainfall": rainfall,

        "rain_bin": get_rain_bin(rainfall),

        "forecast_time": forecast_time

    }

