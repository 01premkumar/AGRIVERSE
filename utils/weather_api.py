# ==========================================================
# AGRIVERSE WEATHER API
# Current Weather + 5-Day Forecast
# ==========================================================

import requests
from datetime import datetime

from config.config import WEATHER_API_KEY


# ==========================================================
# OPENWEATHER API URLS
# ==========================================================

CURRENT_WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

FORECAST_URL = (
    "https://api.openweathermap.org/data/2.5/forecast"
)


# ==========================================================
# COMMON PARAMETERS
# ==========================================================

def _get_params(city):
    return {
        "q": f"{city},IN",
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }


# ==========================================================
# CURRENT WEATHER
# ==========================================================

def get_weather(city):

    if not WEATHER_API_KEY:
        raise Exception(
            "Weather API key is not configured."
        )

    params = _get_params(city)

    response = requests.get(
        CURRENT_WEATHER_URL,
        params=params,
        timeout=15,
    )

    # Raise error for 4xx / 5xx responses
    response.raise_for_status()

    data = response.json()

    # OpenWeather error response protection
    if data.get("cod") not in [200, "200"]:
        raise Exception(
            data.get(
                "message",
                "Unable to fetch weather data.",
            )
        )

    return data


# ==========================================================
# FORECAST WEATHER
# ==========================================================

def get_forecast(city):

    if not WEATHER_API_KEY:
        raise Exception(
            "Weather API key is not configured."
        )

    params = _get_params(city)

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("cod") not in [200, "200"]:
        raise Exception(
            data.get(
                "message",
                "Unable to fetch forecast data.",
            )
        )

    return data


# ==========================================================
# SAFE FLOAT
# ==========================================================

def _safe_float(value, default=0.0):

    try:
        return float(value)
    except (
        TypeError,
        ValueError,
    ):
        return default


# ==========================================================
# PROCESS FORECAST
# ==========================================================

def get_processed_forecast(city):

    data = get_forecast(city)

    forecast_list = data.get(
        "list",
        [],
    )

    processed = []

    # --------------------------------------------------------
    # Each OpenWeather forecast item is approximately
    # 3 hours apart.
    # --------------------------------------------------------

    for item in forecast_list:

        dt_txt = item.get(
            "dt_txt",
            "",
        )

        if not dt_txt:
            continue

        main = item.get(
            "main",
            {},
        )

        weather_list = item.get(
            "weather",
            [],
        )

        wind = item.get(
            "wind",
            {},
        )

        rain_data = item.get(
            "rain",
            {},
        )

        # ----------------------------------------------------
        # Rainfall for this 3-hour forecast
        # ----------------------------------------------------

        rainfall_3h = _safe_float(
            rain_data.get(
                "3h",
                0,
            )
        )

        # ----------------------------------------------------
        # Rain probability
        # OpenWeather gives probability as 0 to 1
        # ----------------------------------------------------

        rain_probability = (
            _safe_float(
                item.get(
                    "pop",
                    0,
                )
            )
            * 100
        )

        # ----------------------------------------------------
        # Weather condition
        # ----------------------------------------------------

        weather_main = "Unknown"
        weather_description = ""

        if weather_list:

            weather_main = weather_list[0].get(
                "main",
                "Unknown",
            )

            weather_description = (
                weather_list[0].get(
                    "description",
                    "",
                )
            )

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        forecast_datetime = datetime.strptime(
            dt_txt,
            "%Y-%m-%d %H:%M:%S",
        )

        processed.append(
            {
                "datetime": dt_txt,

                "date":
                    forecast_datetime.strftime(
                        "%Y-%m-%d"
                    ),

                "time":
                    forecast_datetime.strftime(
                        "%H:%M"
                    ),

                "temperature":
                    _safe_float(
                        main.get(
                            "temp",
                            0,
                        )
                    ),

                "humidity":
                    _safe_float(
                        main.get(
                            "humidity",
                            0,
                        )
                    ),

                "pressure":
                    _safe_float(
                        main.get(
                            "pressure",
                            0,
                        )
                    ),

                "rainfall_3h":
                    rainfall_3h,

                "rain_probability":
                    rain_probability,

                "weather":
                    weather_main,

                "description":
                    weather_description,

                "wind_speed":
                    _safe_float(
                        wind.get(
                            "speed",
                            0,
                        )
                    ),
            }
        )

    return processed


# ==========================================================
# DATE-WISE FORECAST
# ==========================================================

def get_forecast_for_date(
    city,
    target_date,
):

    forecast = get_processed_forecast(
        city
    )

    # --------------------------------------------------------
    # Accept:
    #   2026-08-30
    # or
    #   datetime/date-like object
    # --------------------------------------------------------

    if hasattr(
        target_date,
        "strftime",
    ):
        target_date_string = (
            target_date.strftime(
                "%Y-%m-%d"
            )
        )
    else:
        target_date_string = str(
            target_date
        )[:10]

    matching_forecasts = [
        item
        for item in forecast
        if item["date"]
        == target_date_string
    ]

    # --------------------------------------------------------
    # No forecast available
    # --------------------------------------------------------

    if not matching_forecasts:
        return {
            "date":
                target_date_string,

            "available":
                False,

            "forecast":
                [],
        }

    # --------------------------------------------------------
    # Calculate daily values
    # --------------------------------------------------------

    temperatures = [
        item["temperature"]
        for item in matching_forecasts
    ]

    humidities = [
        item["humidity"]
        for item in matching_forecasts
    ]

    rainfall_values = [
        item["rainfall_3h"]
        for item in matching_forecasts
    ]

    rain_probabilities = [
        item["rain_probability"]
        for item in matching_forecasts
    ]

    # Maximum rain probability
    max_rain_probability = max(
        rain_probabilities,
        default=0,
    )

    # Total forecast rainfall
    total_rainfall = sum(
        rainfall_values
    )

    # Average temperature
    average_temperature = (
        sum(temperatures)
        / len(temperatures)
        if temperatures
        else 0
    )

    # Average humidity
    average_humidity = (
        sum(humidities)
        / len(humidities)
        if humidities
        else 0
    )

    # --------------------------------------------------------
    # Rain detected
    # --------------------------------------------------------

    rain_detected = (
        total_rainfall >= 5
        or max_rain_probability >= 60
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {
        "date":
            target_date_string,

        "available":
            True,

        "average_temperature":
            round(
                average_temperature,
                2,
            ),

        "average_humidity":
            round(
                average_humidity,
                2,
            ),

        "total_rainfall":
            round(
                total_rainfall,
                2,
            ),

        "rain_probability":
            round(
                max_rain_probability,
                2,
            ),

        "rain_detected":
            rain_detected,

        "forecast":
            matching_forecasts,
    }


# ==========================================================
# WEATHER + FORECAST FOR AGRIVERSE
# ==========================================================

def get_weather_and_forecast(
    city,
):

    current_weather = get_weather(
        city
    )

    forecast = get_processed_forecast(
        city
    )

    return {
        "current": current_weather,
        "forecast": forecast,
    }