import json

import services.analytics_service as analytics_service


def test_calculate_correlation_requires_two_snapshots():
    result = analytics_service.calculate_correlation([])

    assert result["correlation"] is None
    assert "Not enough snapshots" in result["interpretation"]


def test_correlation_requires_rainfall_variation():
    snapshots = [
        {
            "rainfall_mm": 0,
            "average_delay_minutes": 1.2
        },
        {
            "rainfall_mm": 0,
            "average_delay_minutes": 2.4
        }
    ]

    result = analytics_service.calculate_correlation(snapshots)

    assert result["correlation"] is None
    assert "too similar" in result["interpretation"]


def test_positive_correlation():
    snapshots = [
        {
            "rainfall_mm": 0,
            "average_delay_minutes": 1
        },
        {
            "rainfall_mm": 1,
            "average_delay_minutes": 2
        },
        {
            "rainfall_mm": 2,
            "average_delay_minutes": 3
        }
    ]

    result = analytics_service.calculate_correlation(snapshots)

    assert result["correlation"] == 1.0
    assert "positive relationship" in result["interpretation"]


def test_save_and_load_snapshot(tmp_path, monkeypatch):
    temporary_file = tmp_path / "snapshots.json"

    monkeypatch.setattr(
        analytics_service,
        "DATA_FOLDER",
        str(tmp_path)
    )

    monkeypatch.setattr(
        analytics_service,
        "SNAPSHOT_FILE",
        str(temporary_file)
    )

    weather = {
        "rainfall_mm": 1.5,
        "rain_bin": "Moderate"
    }

    gtfs = {
        "average_delay_minutes": 2.3,
        "delayed_trips": 120,
        "entities": 900
    }

    saved_snapshot = analytics_service.save_snapshot(weather, gtfs)
    loaded_snapshots = analytics_service.load_snapshots()

    assert temporary_file.exists()
    assert len(loaded_snapshots) == 1
    assert saved_snapshot["rainfall_mm"] == 1.5
    assert saved_snapshot["rain_bin"] == "Moderate"
    assert saved_snapshot["average_delay_minutes"] == 2.3
    assert saved_snapshot["delayed_trips"] == 120
    assert saved_snapshot["live_trips"] == 900

    with open(temporary_file, "r", encoding="utf-8") as file:
        stored_data = json.load(file)

    assert stored_data == loaded_snapshots