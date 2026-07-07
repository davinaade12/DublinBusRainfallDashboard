from flask import Blueprint, jsonify

from services.gtfs_service import fetch_gtfs_data

gtfs_bp = Blueprint("gtfs", __name__)


@gtfs_bp.route("/gtfs")
def gtfs():

    return jsonify(fetch_gtfs_data())