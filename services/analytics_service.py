import json
import os
from datetime import datetime

DATA_FOLDER = "data"
SNAPSHOT_FILE = os.path.join(DATA_FOLDER, "snapshots.json")


def save_snapshot(weather, gtfs):
    os.makedirs(DATA_FOLDER, exist_ok=True)

    snapshots = []

    if os.path.exists(SNAPSHOT_FILE):
        try:
            with open(SNAPSHOT_FILE, "r") as file:
                snapshots = json.load(file)
        except json.JSONDecodeError:
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

    with open(SNAPSHOT_FILE, "w") as file:
        json.dump(snapshots, file, indent=4)

    return snapshot


def load_snapshots():
    if not os.path.exists(SNAPSHOT_FILE):
        return []

    try:
        with open(SNAPSHOT_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return [] 