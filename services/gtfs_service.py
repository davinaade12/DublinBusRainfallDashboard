import os
import requests
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2

load_dotenv()


def fetch_gtfs_data():
    api_key = os.getenv("NTA_API_KEY")
    url = os.getenv("NTA_GTFS_URL")

    print("API Key loaded:", api_key is not None and api_key != "")
    print("GTFS URL:", url)

    if not api_key:
        return {
            "success": False,
            "error": "NTA_API_KEY is missing from .env"
        }

    if not url:
        return {
            "success": False,
            "error": "NTA_GTFS_URL is missing from .env"
        }

    headers = {
        "x-api-key": api_key,
        "Ocp-Apim-Subscription-Key": api_key
    }

    response = requests.get(url, headers=headers, timeout=30)

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    if response.status_code != 200:
        return {
            "success": False,
            "error": "NTA request failed",
            "status": response.status_code,
            "preview": response.text[:300]
        }

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    delays = []

    for entity in feed.entity:
        if entity.HasField("trip_update"):
            for stop in entity.trip_update.stop_time_update:
                if stop.HasField("arrival") and stop.arrival.HasField("delay"):
                    delays.append(stop.arrival.delay)

    average_delay = sum(delays) / len(delays) if delays else 0

    delayed_trips = len([delay for delay in delays if delay > 120])

    return {
        "success": True,
        "entities": len(feed.entity),
        "delay_samples": len(delays),
        "average_delay_minutes": round(average_delay / 60, 2),
        "delayed_trips": delayed_trips
    }