import csv
import io

from flask import Blueprint, render_template, Response
from services.analytics_service import (
    load_snapshots,
    calculate_correlation
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/analytics")
def analytics():
    snapshots = load_snapshots()

    total_snapshots = len(snapshots)

    if total_snapshots > 0:
        rainfall_values = [
            float(item.get("rainfall_mm", 0))
            for item in snapshots
        ]

        delay_values = [
            float(item.get("average_delay_minutes", 0))
            for item in snapshots
        ]

        average_rainfall = sum(rainfall_values) / total_snapshots
        average_delay = sum(delay_values) / total_snapshots
        highest_delay = max(delay_values)
    else:
        average_rainfall = 0
        average_delay = 0
        highest_delay = 0

    summary = {
        "total_snapshots": total_snapshots,
        "average_rainfall": round(average_rainfall, 2),
        "average_delay": round(average_delay, 2),
        "highest_delay": round(highest_delay, 2)
    }

    correlation_result = calculate_correlation(snapshots)

    return render_template(
        "analytics.html",
        snapshots=snapshots,
        summary=summary,
        correlation=correlation_result
    )


@dashboard_bp.route("/export-csv")
def export_csv():
    snapshots = load_snapshots()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Timestamp",
        "Rainfall (mm)",
        "Rain Category",
        "Average Delay (minutes)",
        "Delayed Trips",
        "Live Trips"
    ])

    for item in snapshots:
        writer.writerow([
            item.get("timestamp", ""),
            item.get("rainfall_mm", 0),
            item.get("rain_bin", "Unknown"),
            item.get("average_delay_minutes", 0),
            item.get("delayed_trips", 0),
            item.get("live_trips", 0)
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=dublin_bus_rainfall_snapshots.csv"
        }
    )