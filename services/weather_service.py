import os
import requests
import xmltodict


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
    try:
        url = os.getenv("MET_FORECAST_URL")

        if not url:
            return {
                "success": False,
                "error": "MET_FORECAST_URL is missing from .env"
            }

        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return {
                "success": False,
                "error": "Met Eireann request failed",
                "status_code": response.status_code,
                "preview": response.text[:200]
            }

        data = xmltodict.parse(response.text)

        times = data.get("weatherdata", {}).get("product", {}).get("time", [])

        if not isinstance(times, list):
            times = [times]

        rainfall = 0
        forecast_time = ""

        for item in times:
            location = item.get("location")

            if not location:
                continue

            if isinstance(location, list):
                locations = location
            else:
                locations = [location]

            for loc in locations:
                precipitation = loc.get("precipitation")

                if precipitation:
                    rainfall = float(precipitation.get("@value", 0))
                    forecast_time = item.get("@from", "")
                    return {
                        "success": True,
                        "source": "Met Eireann Forecast API",
                        "location": "Dublin",
                        "rainfall": rainfall,
                        "rainfall_mm": rainfall,
                        "rain_bin": get_rain_bin(rainfall),
                        "forecast_time": forecast_time
                    }

        return {
            "success": True,
            "source": "Met Eireann Forecast API",
            "location": "Dublin",
            "rainfall": 0,
            "rainfall_mm": 0,
            "rain_bin": "None",
            "forecast_time": forecast_time
        }

    except Exception as error:
        return {
            "success": False,
            "error": "Failed to fetch weather data",
            "details": str(error)
        }