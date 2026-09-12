# ==========================================================
# AGRIVERSE WEATHER SERVICE
# Current Weather + Forecast
# ==========================================================

from datetime import datetime

from utils.weather_api import (
    get_weather,
    get_forecast_for_date,
)


# ==========================================================
# SEASON
# ==========================================================

def get_season(month):

    if month in [6, 7, 8, 9, 10]:
        return "Kharif"

    elif month in [11, 12, 1, 2]:
        return "Rabi"

    else:
        return "Zaid"


# ==========================================================
# CURRENT WEATHER
# ==========================================================

def weather_prediction(district):

    data = get_weather(
        district
    )

    now = datetime.now()

    current_month = now.strftime(
        "%B"
    )

    month_number = now.month

    season = get_season(
        month_number
    )

    # --------------------------------------------------------
    # Rainfall
    # --------------------------------------------------------

    rainfall = (
        data.get("rain", {})
        .get("1h", 0)
    )

    # --------------------------------------------------------
    # Safe weather extraction
    # --------------------------------------------------------

    main = data.get(
        "main",
        {}
    )

    weather_list = data.get(
        "weather",
        []
    )

    wind = data.get(
        "wind",
        {}
    )

    weather_main = "Unknown"
    description = ""

    if weather_list:

        weather_main = (
            weather_list[0]
            .get(
                "main",
                "Unknown"
            )
        )

        description = (
            weather_list[0]
            .get(
                "description",
                ""
            )
        )

    # --------------------------------------------------------
    # Return current weather
    # --------------------------------------------------------

    return {

        "district":
            district,

        "temperature":
            main.get(
                "temp",
                0
            ),

        "humidity":
            main.get(
                "humidity",
                0
            ),

        "pressure":
            main.get(
                "pressure",
                0
            ),

        "weather":
            weather_main,

        "description":
            description,

        "wind_speed":
            wind.get(
                "speed",
                0
            ),

        "rainfall":
            rainfall,

        "month":
            current_month,

        "season":
            season
    }


# ==========================================================
# FORECAST FOR SPECIFIC DATE
# ==========================================================

def weather_forecast_for_date(
    district,
    target_date
):

    forecast = get_forecast_for_date(
        district,
        target_date
    )

    return forecast


# ==========================================================
# SMART WEATHER ADVICE
# ==========================================================

def get_weather_advice(
    task_type,
    temperature=0,
    humidity=0,
    rainfall=0,
    rain_probability=0,
    rain_detected=False
):

    # --------------------------------------------------------
    # Safe values
    # --------------------------------------------------------

    try:
        temperature = float(
            temperature or 0
        )
    except (
        TypeError,
        ValueError
    ):
        temperature = 0

    try:
        humidity = float(
            humidity or 0
        )
    except (
        TypeError,
        ValueError
    ):
        humidity = 0

    try:
        rainfall = float(
            rainfall or 0
        )
    except (
        TypeError,
        ValueError
    ):
        rainfall = 0

    try:
        rain_probability = float(
            rain_probability or 0
        )
    except (
        TypeError,
        ValueError
    ):
        rain_probability = 0

    # ========================================================
    # IRRIGATION
    # ========================================================

    if task_type == "irrigation":

        if (
            rain_detected
            or rainfall >= 5
            or rain_probability >= 60
        ):
            return (
                "Rain is expected or detected. "
                "Check soil moisture before irrigation. "
                "Irrigation may not be required."
            )

        if temperature >= 35:

            return (
                "High temperature detected. "
                "Monitor crop water requirement carefully."
            )

        if temperature <= 20:

            return (
                "Temperature is relatively low. "
                "Check soil moisture before irrigation."
            )

        return (
            "Weather condition is suitable. "
            "Follow the irrigation schedule "
            "and check soil moisture."
        )

    # ========================================================
    # FERTILIZER
    # ========================================================

    if task_type == "fertilizer":

        if (
            rain_detected
            or rainfall >= 5
            or rain_probability >= 60
        ):
            return (
                "Rain is expected or detected. "
                "Avoid fertilizer application during "
                "heavy rainfall. Check field condition "
                "before applying fertilizer."
            )

        if humidity >= 85:

            return (
                "High humidity detected. "
                "Check crop condition before "
                "fertilizer application."
            )

        return (
            "Weather condition is suitable. "
            "Apply fertilizer according to "
            "crop requirement."
        )

    # ========================================================
    # GROWTH
    # ========================================================

    if task_type == "growth":

        if temperature >= 35:

            return (
                "High temperature detected. "
                "Monitor crop growth and "
                "water requirement."
            )

        if humidity >= 85:

            return (
                "High humidity detected. "
                "Monitor crop health carefully."
            )

        if (
            rain_detected
            or rainfall >= 5
        ):

            return (
                "Rainfall detected. "
                "Monitor crop growth and "
                "field moisture."
            )

        return (
            "Monitor crop growth "
            "and plant health."
        )

    # ========================================================
    # PEST CHECK
    # ========================================================

    if task_type == "pest_check":

        if humidity >= 80:

            return (
                "High humidity detected. "
                "Monitor the crop carefully "
                "for pest and disease symptoms."
            )

        if (
            rain_detected
            or rainfall >= 5
        ):

            return (
                "Rainfall detected. "
                "Inspect the crop for "
                "disease symptoms."
            )

        return (
            "Inspect the crop for pests "
            "and disease symptoms."
        )

    # ========================================================
    # HARVEST
    # ========================================================

    if task_type == "harvest":

        if (
            rain_detected
            or rainfall >= 5
            or rain_probability >= 60
        ):

            return (
                "Rain is expected or detected. "
                "Check field and crop condition "
                "before harvesting."
            )

        return (
            "Check crop maturity and "
            "prepare for harvesting."
        )

    # ========================================================
    # SOWING
    # ========================================================

    if task_type == "sowing":

        if (
            rain_detected
            or rainfall >= 5
        ):

            return (
                "Rainfall detected. "
                "Check soil moisture before sowing."
            )

        return (
            "Prepare the field and follow "
            "recommended sowing practices."
        )

    # ========================================================
    # DEFAULT
    # ========================================================

    return (
        "Monitor crop condition and "
        "follow recommended farming practices."
    )


# ==========================================================
# CURRENT WEATHER + SEASON
# ==========================================================

def get_current_weather_summary(
    district
):

    weather = weather_prediction(
        district
    )

    return {
        "district":
            district,

        "temperature":
            weather.get(
                "temperature",
                0
            ),

        "humidity":
            weather.get(
                "humidity",
                0
            ),

        "rainfall":
            weather.get(
                "rainfall",
                0
            ),

        "weather":
            weather.get(
                "weather",
                "Unknown"
            ),

        "description":
            weather.get(
                "description",
                ""
            ),

        "wind_speed":
            weather.get(
                "wind_speed",
                0
            ),

        "month":
            weather.get(
                "month",
                ""
            ),

        "season":
            weather.get(
                "season",
                ""
            )
    }