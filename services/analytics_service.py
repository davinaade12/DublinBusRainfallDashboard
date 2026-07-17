import json
import os
from datetime import datetime

from services.firebase_service import initialise_firebase

DATA_FOLDER = "data"
SNAPSHOT_FILE = os.path.join(DATA_FOLDER, "snapshots.json")


def save_snapshot(weather, gtfs):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    snapshots = []

    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, "r", encoding="utf-8") as file:
                snapshots = json.load(file)
        except (json.JSONDecodeError, OSError):
            snapshots = []

    snapshot = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rainfall_mm": weather.get("rainfall_mm", 0),
        "rain_bin": weather.get("rain_bin", "Unknown"),
        "average_delay_minutes": gtfs.get("average_delay_minutes", 0),
        "delayed_trips": gtfs.get("delayed_trips", 0),
        "live_trips": gtfs.get("entities", 0)
    }

    snapshots.append(snapshot)

    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as file:
        json.dump(snapshots, file, indent=4)

    try:
        database = initialise_firebase()
        database.collection("snapshots").add(snapshot)
    except Exception as error:
        print(f"Firebase save failed: {error}")

    return snapshot


def load_snapshots():
    try:
        database = initialise_firebase()

        documents = (
            database.collection("snapshots")
            .order_by("timestamp")
            .stream()
        )

        firebase_snapshots = [
            document.to_dict()
            for document in documents
        ]

        if firebase_snapshots:
            return firebase_snapshots

    except Exception as error:
        print(f"Firebase load failed: {error}")

    if not os.path.exists(SNAPSHOT_FILE):
        return []

    try:
        with open(SNAPSHOT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def calculate_correlation(snapshots):
    if len(snapshots) < 2:
        return {
            "correlation": None,
            "interpretation": "Not enough snapshots collected yet."
        }

    rainfall = [
        float(snapshot.get("rainfall_mm", 0))
        for snapshot in snapshots
    ]

    delays = [
        float(snapshot.get("average_delay_minutes", 0))
        for snapshot in snapshots
    ]

    if len(set(rainfall)) <= 1:
        return {
            "correlation": None,
            "interpretation": (
                "Rainfall values are currently too similar to calculate "
                "a meaningful correlation."
            )
        }

    if len(set(delays)) <= 1:
        return {
            "correlation": None,
            "interpretation": (
                "Delay values are currently too similar to calculate "
                "a meaningful correlation."
            )
        }

    number_of_snapshots = len(snapshots)

    mean_rainfall = sum(rainfall) / number_of_snapshots
    mean_delay = sum(delays) / number_of_snapshots

    numerator = sum(
        (rainfall[index] - mean_rainfall)
        * (delays[index] - mean_delay)
        for index in range(number_of_snapshots)
    )

    rainfall_denominator = sum(
        (value - mean_rainfall) ** 2
        for value in rainfall
    ) ** 0.5

    delay_denominator = sum(
        (value - mean_delay) ** 2
        for value in delays
    ) ** 0.5

    denominator = rainfall_denominator * delay_denominator

    if denominator == 0:
        return {
            "correlation": None,
            "interpretation": (
                "There is not enough variation in the saved data "
                "to calculate a meaningful correlation."
            )
        }

    correlation = numerator / denominator

    absolute_correlation = abs(correlation)

    if absolute_correlation >= 0.7:
        strength = "Strong"
    elif absolute_correlation >= 0.3:
        strength = "Moderate"
    else:
        strength = "Weak"

    if correlation > 0:
        interpretation = (
            f"{strength} positive relationship: higher rainfall is associated "
            "with higher average delay in the current sample."
        )
    elif correlation < 0:
        interpretation = (
            f"{strength} negative relationship: higher rainfall is associated "
            "with lower average delay in the current sample."
        )
    else:
        interpretation = "Little or no linear relationship."

    return {
        "correlation": round(correlation, 3),
        "interpretation": interpretation
    }