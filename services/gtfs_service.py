import os

import requests
from dotenv import load_dotenv
from google.protobuf.message import DecodeError
from google.transit import gtfs_realtime_pb2

load_dotenv()


def fetch_gtfs_data():
    api_key = os.getenv("NTA_API_KEY")
    url = os.getenv("NTA_GTFS_URL")

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

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        all_delays = []
        delayed_stop_updates = 0
        delayed_trip_ids = set()
        trip_update_count = 0

        for entity in feed.entity:
            if not entity.HasField("trip_update"):
                continue

            trip_update_count += 1
            trip_update = entity.trip_update

            trip_id = (
                trip_update.trip.trip_id
                if trip_update.trip.trip_id
                else entity.id
            )

            trip_is_delayed = False

            for stop_update in trip_update.stop_time_update:
                if (
                    stop_update.HasField("arrival")
                    and stop_update.arrival.HasField("delay")
                ):
                    delay_seconds = stop_update.arrival.delay
                    all_delays.append(delay_seconds)

                    if delay_seconds > 120:
                        delayed_stop_updates += 1
                        trip_is_delayed = True

            if trip_is_delayed:
                delayed_trip_ids.add(trip_id)

        average_delay_seconds = (
            sum(all_delays) / len(all_delays)
            if all_delays
            else 0
        )

        return {
            "success": True,
            "entities": len(feed.entity),
            "trip_updates": trip_update_count,
            "delay_samples": len(all_delays),
            "average_delay_seconds": round(
                average_delay_seconds,
                2
            ),
            "average_delay_minutes": round(
                average_delay_seconds / 60,
                2
            ),
            "delayed_trips": len(delayed_trip_ids),
            "delayed_stop_updates": delayed_stop_updates,
            "delay_threshold_seconds": 120
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "error": "Failed to retrieve NTA GTFS-Realtime data",
            "details": str(error)
        }

    except DecodeError as error:
        return {
            "success": False,
            "error": "The NTA response was not valid GTFS-Realtime data",
            "details": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "error": "Unexpected GTFS processing error",
            "details": str(error)
        }