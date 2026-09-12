# ============================================================
# AGRIVERSE - CROP TIMELINE SERVICE
# ============================================================

from datetime import timedelta

from backend.services.weather_service import (
    weather_prediction,
    weather_forecast_for_date,
    get_weather_advice,
)


# ============================================================
# CROP TIMELINES
# ============================================================
#
# Day 1 = planting/sowing day
# Day 2 = one day after planting
#
# Add more crops here whenever required.
# ============================================================

CROP_TIMELINES = {

    # ========================================================
    # COTTON
    # ========================================================

    "cotton": [
        {
            "day": 1,
            "task": "Seed Sowing",
            "type": "sowing",
        },
        {
            "day": 7,
            "task": "First Irrigation",
            "type": "irrigation",
        },
        {
            "day": 15,
            "task": "Crop Growth Check",
            "type": "growth",
        },
        {
            "day": 25,
            "task": "Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 35,
            "task": "Irrigation",
            "type": "irrigation",
        },
        {
            "day": 60,
            "task": "Flowering Stage Care",
            "type": "growth",
        },
        {
            "day": 90,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 120,
            "task": "Boll Development Care",
            "type": "growth",
        },
        {
            "day": 150,
            "task": "Harvest Preparation",
            "type": "harvest",
        },
        {
            "day": 180,
            "task": "Harvest",
            "type": "harvest",
        },
    ],


    # ========================================================
    # RICE
    # ========================================================

    "rice": [
        {
            "day": 1,
            "task": "Seed / Nursery Preparation",
            "type": "sowing",
        },
        {
            "day": 10,
            "task": "Nursery / Seedling Check",
            "type": "growth",
        },
        {
            "day": 20,
            "task": "Transplanting Preparation",
            "type": "growth",
        },
        {
            "day": 25,
            "task": "Transplanting",
            "type": "sowing",
        },
        {
            "day": 35,
            "task": "First Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 50,
            "task": "Water Management Check",
            "type": "irrigation",
        },
        {
            "day": 70,
            "task": "Crop Growth Check",
            "type": "growth",
        },
        {
            "day": 90,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 110,
            "task": "Panicle Development Check",
            "type": "growth",
        },
        {
            "day": 130,
            "task": "Grain Development Check",
            "type": "growth",
        },
        {
            "day": 150,
            "task": "Harvest Preparation",
            "type": "harvest",
        },
        {
            "day": 150,
            "task": "Harvest",
            "type": "harvest",
        },
    ],


    # ========================================================
    # MAIZE
    # ========================================================

    "maize": [
        {
            "day": 1,
            "task": "Seed Sowing",
            "type": "sowing",
        },
        {
            "day": 7,
            "task": "Germination Check",
            "type": "growth",
        },
        {
            "day": 15,
            "task": "Crop Growth Check",
            "type": "growth",
        },
        {
            "day": 25,
            "task": "Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 35,
            "task": "Irrigation",
            "type": "irrigation",
        },
        {
            "day": 50,
            "task": "Weed and Crop Check",
            "type": "growth",
        },
        {
            "day": 65,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 80,
            "task": "Flowering Stage Check",
            "type": "growth",
        },
        {
            "day": 100,
            "task": "Grain Development Check",
            "type": "growth",
        },
        {
            "day": 120,
            "task": "Harvest Preparation",
            "type": "harvest",
        },
        {
            "day": 130,
            "task": "Harvest",
            "type": "harvest",
        },
    ],


    # ========================================================
    # GROUNDNUT
    # ========================================================

    "groundnut": [
        {
            "day": 1,
            "task": "Seed Sowing",
            "type": "sowing",
        },
        {
            "day": 7,
            "task": "Germination Check",
            "type": "growth",
        },
        {
            "day": 20,
            "task": "Crop Growth Check",
            "type": "growth",
        },
        {
            "day": 30,
            "task": "Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 40,
            "task": "Irrigation",
            "type": "irrigation",
        },
        {
            "day": 55,
            "task": "Flowering Check",
            "type": "growth",
        },
        {
            "day": 70,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 90,
            "task": "Pegging and Pod Development Check",
            "type": "growth",
        },
        {
            "day": 105,
            "task": "Harvest Preparation",
            "type": "harvest",
        },
        {
            "day": 120,
            "task": "Harvest",
            "type": "harvest",
        },
    ],


    # ========================================================
    # TOMATO
    # ========================================================

    "tomato": [
        {
            "day": 1,
            "task": "Seedling / Transplanting",
            "type": "sowing",
        },
        {
            "day": 10,
            "task": "Seedling Growth Check",
            "type": "growth",
        },
        {
            "day": 20,
            "task": "Irrigation",
            "type": "irrigation",
        },
        {
            "day": 30,
            "task": "Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 40,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 55,
            "task": "Flowering Stage Care",
            "type": "growth",
        },
        {
            "day": 70,
            "task": "Fruit Development Check",
            "type": "growth",
        },
        {
            "day": 85,
            "task": "Harvest Preparation",
            "type": "harvest",
        },
        {
            "day": 90,
            "task": "Harvest",
            "type": "harvest",
        },
    ],


    # ========================================================
    # CHILLI
    # ========================================================

    "chilli": [
        {
            "day": 1,
            "task": "Seedling / Transplanting",
            "type": "sowing",
        },
        {
            "day": 15,
            "task": "Crop Growth Check",
            "type": "growth",
        },
        {
            "day": 30,
            "task": "Irrigation",
            "type": "irrigation",
        },
        {
            "day": 40,
            "task": "Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 55,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 70,
            "task": "Flowering Stage Care",
            "type": "growth",
        },
        {
            "day": 90,
            "task": "Fruit Development Check",
            "type": "growth",
        },
        {
            "day": 110,
            "task": "Harvest Preparation",
            "type": "harvest",
        },
        {
            "day": 120,
            "task": "Harvest",
            "type": "harvest",
        },
    ],


    # ========================================================
    # OKRA
    # ========================================================

    "okra": [
        {
            "day": 1,
            "task": "Seed Sowing",
            "type": "sowing",
        },
        {
            "day": 7,
            "task": "Germination Check",
            "type": "growth",
        },
        {
            "day": 20,
            "task": "Crop Growth Check",
            "type": "growth",
        },
        {
            "day": 30,
            "task": "Fertilizer Application",
            "type": "fertilizer",
        },
        {
            "day": 40,
            "task": "Irrigation",
            "type": "irrigation",
        },
        {
            "day": 50,
            "task": "Pest and Disease Check",
            "type": "pest_check",
        },
        {
            "day": 60,
            "task": "Flowering Check",
            "type": "growth",
        },
        {
            "day": 65,
            "task": "First Harvest",
            "type": "harvest",
        },
        {
            "day": 80,
            "task": "Continued Harvest",
            "type": "harvest",
        },
    ],
}


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(value, default=0.0):

    try:
        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):

        return default


# ============================================================
# FORECAST VALUE EXTRACTION
# ============================================================

def extract_forecast_values(forecast):

    if not isinstance(forecast, dict):

        return {
            "temperature": 0,
            "humidity": 0,
            "rainfall": 0,
            "rain_probability": 0,
            "rain_detected": False,
        }

    temperature = safe_float(
        forecast.get(
            "temperature",
            forecast.get("temp", 0),
        )
    )

    humidity = safe_float(
        forecast.get(
            "humidity",
            0,
        )
    )

    rainfall = safe_float(
        forecast.get(
            "rainfall",
            forecast.get("rain", 0),
        )
    )

    rain_probability = safe_float(
        forecast.get(
            "rain_probability",
            forecast.get(
                "rain_chance",
                forecast.get(
                    "precipitation_probability",
                    0,
                ),
            ),
        )
    )

    rain_detected = bool(
        forecast.get(
            "rain_detected",
            False,
        )
    )

    return {
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "rain_probability": rain_probability,
        "rain_detected": rain_detected,
    }


# ============================================================
# CURRENT WEATHER FALLBACK
# ============================================================

def get_current_weather_values(weather):

    if not isinstance(weather, dict):

        return {
            "temperature": 0,
            "humidity": 0,
            "rainfall": 0,
            "rain_probability": 0,
            "rain_detected": False,
        }

    weather_name = str(
        weather.get(
            "weather",
            "",
        )
    ).lower()

    description = str(
        weather.get(
            "description",
            "",
        )
    ).lower()

    rain_detected = (
        "rain" in weather_name
        or "rain" in description
        or "drizzle" in weather_name
        or "thunderstorm" in weather_name
    )

    return {
        "temperature": safe_float(
            weather.get(
                "temperature",
                0,
            )
        ),
        "humidity": safe_float(
            weather.get(
                "humidity",
                0,
            )
        ),
        "rainfall": safe_float(
            weather.get(
                "rainfall",
                0,
            )
        ),
        "rain_probability": 0,
        "rain_detected": rain_detected,
    }


# ============================================================
# GET WEATHER FOR TIMELINE DATE
# ============================================================

def get_weather_for_timeline_date(
    district,
    target_date,
    current_weather,
):

    # --------------------------------------------------------
    # Try forecast
    # --------------------------------------------------------

    try:

        forecast = weather_forecast_for_date(
            district,
            target_date,
        )

        if isinstance(forecast, dict):

            values = extract_forecast_values(
                forecast
            )

            # Add date if API didn't provide one
            if "date" not in forecast:

                forecast["date"] = (
                    target_date.isoformat()
                )

            return {
                "weather": forecast,
                "values": values,
                "source": "forecast",
            }

    except Exception as e:

        print(
            "AGRIVERSE: Forecast unavailable "
            f"for {district} on "
            f"{target_date}: {e}"
        )

    # --------------------------------------------------------
    # Fallback to current weather
    # --------------------------------------------------------

    values = get_current_weather_values(
        current_weather
    )

    fallback_weather = {
        "district": district,
        "date": target_date.isoformat(),
        "temperature": values["temperature"],
        "humidity": values["humidity"],
        "rainfall": values["rainfall"],
        "rain_probability": values[
            "rain_probability"
        ],
        "rain_detected": values[
            "rain_detected"
        ],
        "weather": current_weather.get(
            "weather",
            "Unknown",
        )
        if isinstance(current_weather, dict)
        else "Unknown",
        "description": current_weather.get(
            "description",
            "",
        )
        if isinstance(current_weather, dict)
        else "",
    }

    return {
        "weather": fallback_weather,
        "values": values,
        "source": "current_weather_fallback",
    }


# ============================================================
# CROP TIMELINE
# ============================================================

def get_crop_timeline(
    crop_name,
    planting_date,
    district,
):

    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    crop_name = (
        str(crop_name)
        .lower()
        .strip()
    )

    district = (
        str(district)
        .strip()
    )

    # --------------------------------------------------------
    # CHECK CROP
    # --------------------------------------------------------

    if crop_name not in CROP_TIMELINES:

        return {
            "crop": crop_name,
            "district": district,
            "planting_date":
                planting_date.isoformat(),
            "weather": {},
            "timeline": [],
            "available_crops":
                sorted(
                    CROP_TIMELINES.keys()
                ),
            "message":
                "Crop timeline is not available yet.",
        }

    # --------------------------------------------------------
    # GET CURRENT WEATHER
    # --------------------------------------------------------

    try:

        current_weather = weather_prediction(
            district
        )

    except Exception as e:

        return {
            "crop": crop_name,
            "district": district,
            "planting_date":
                planting_date.isoformat(),
            "weather": {},
            "timeline": [],
            "weather_error":
                "Unable to fetch current weather.",
            "details": str(e),
        }

    # --------------------------------------------------------
    # BUILD TIMELINE
    # --------------------------------------------------------

    timeline = []

    for stage in CROP_TIMELINES[
        crop_name
    ]:

        day = int(
            stage.get(
                "day",
                1,
            )
        )

        task_date = (
            planting_date
            + timedelta(
                days=day - 1
            )
        )

        task_type = stage.get(
            "type",
            "growth",
        )

        task = stage.get(
            "task",
            "Farm activity",
        )

        # ----------------------------------------------------
        # Get forecast for this task date
        # ----------------------------------------------------

        weather_result = (
            get_weather_for_timeline_date(
                district,
                task_date,
                current_weather,
            )
        )

        task_weather = weather_result[
            "weather"
        ]

        values = weather_result[
            "values"
        ]

        weather_source = weather_result[
            "source"
        ]

        # ----------------------------------------------------
        # Generate smart advice
        # ----------------------------------------------------

        advice = get_weather_advice(

            task_type,

            temperature=values[
                "temperature"
            ],

            humidity=values[
                "humidity"
            ],

            rainfall=values[
                "rainfall"
            ],

            rain_probability=values[
                "rain_probability"
            ],

            rain_detected=values[
                "rain_detected"
            ],
        )

        # ----------------------------------------------------
        # Timeline item
        # ----------------------------------------------------

        timeline.append({

            "day": day,

            "date":
                task_date.isoformat(),

            "task": task,

            "type": task_type,

            "weather_advice":
                advice,

            "weather_source":
                weather_source,

            "forecast": task_weather,
        })

    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "crop": crop_name,

        "district": district,

        "planting_date":
            planting_date.isoformat(),

        # Current weather displayed
        # in the weather card
        "weather":
            current_weather,

        # Full crop timeline
        "timeline":
            timeline,

    }