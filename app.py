from flask import Flask, render_template
from config import Config

from routes.weather import weather_bp
from routes.gtfs import gtfs_bp
from routes.dashboard import dashboard_bp

from services.weather_service import fetch_weather
from services.gtfs_service import fetch_gtfs_data
from services.analytics_service import save_snapshot, load_snapshots


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(weather_bp)
app.register_blueprint(gtfs_bp)
app.register_blueprint(dashboard_bp)


def calculate_system_status(weather, gtfs):
    rainfall = float(weather.get("rainfall_mm", 0))
    average_delay = float(gtfs.get("average_delay_minutes", 0))

    # Project-defined thresholds
    if rainfall > 4 or average_delay > 5:
        return {
            "label": "Severe",
            "class_name": "danger",
            "message": "Significant rainfall or transport delays detected."
        }

    if rainfall > 1 or average_delay > 2:
        return {
            "label": "Moderate",
            "class_name": "warning",
            "message": "Some disruption may be affecting services."
        }

    return {
        "label": "Normal",
        "class_name": "success",
        "message": "Transport conditions are currently operating normally."
    }


@app.route("/")
def home():
    weather = fetch_weather()
    gtfs = fetch_gtfs_data()

    # Save the latest observation
    if weather.get("success") and gtfs.get("success"):
        save_snapshot(weather, gtfs)

    snapshots = load_snapshots()
    recent_snapshots = snapshots[-8:]

    system_status = calculate_system_status(weather, gtfs)

    latest_snapshot_time = (
        snapshots[-1].get("timestamp")
        if snapshots
        else "No snapshots saved"
    )

    return render_template(
        "dashboard.html",
        weather=weather,
        gtfs=gtfs,
        snapshots=recent_snapshots,
        system_status=system_status,
        latest_snapshot_time=latest_snapshot_time
    )


@app.route("/health")
def health():
    return {
        "status": "running",
        "application": "Dublin Bus Rainfall Dashboard"
    }


if __name__ == "__main__":
    print("===========================================")
    print(" Dublin Bus Rainfall Dashboard Starting...")
    print("===========================================")

    app.run(debug=True)