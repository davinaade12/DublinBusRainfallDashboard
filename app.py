from services.analytics_service import save_snapshot, load_snapshots
from flask import Flask, render_template
from config import Config

from routes.weather import weather_bp
from routes.gtfs import gtfs_bp
from services.weather_service import fetch_weather
from services.gtfs_service import fetch_gtfs_data

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(weather_bp)
app.register_blueprint(gtfs_bp)

@app.route("/")
def home():

    weather = fetch_weather()

    gtfs = fetch_gtfs_data()

    save_snapshot(weather, gtfs)

    snapshots = load_snapshots()

    return render_template(
        "dashboard.html",
        weather=weather,
        gtfs=gtfs,
        snapshots=snapshots
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
