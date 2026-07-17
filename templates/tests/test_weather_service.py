from services.weather_service import get_rain_bin


def test_zero_rainfall_is_none():
    assert get_rain_bin(0) == "None"


def test_light_rainfall():
    assert get_rain_bin(0.5) == "Light"
    assert get_rain_bin(1) == "Light"


def test_moderate_rainfall():
    assert get_rain_bin(1.5) == "Moderate"
    assert get_rain_bin(4) == "Moderate"


def test_heavy_rainfall():
    assert get_rain_bin(4.1) == "Heavy"
    assert get_rain_bin(10) == "Heavy"