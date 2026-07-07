from flask import Blueprint, jsonify

from services.weather_service import fetch_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/weather")

def weather():

    return jsonify(fetch_weather())