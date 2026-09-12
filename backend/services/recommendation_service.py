import json
from pathlib import Path
from typing import Any

from backend.services.weather_service import weather_prediction


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE = (
    BASE_DIR
    / "knowledge_base"
    / "crops"
    / "crop_database.json"
)


# ============================================================
# LOAD CROP DATABASE
# ============================================================

def load_database() -> dict[str, Any]:

    if not DATABASE.exists():
        raise FileNotFoundError(
            f"Crop database not found: {DATABASE}"
        )

    try:
        with open(
            DATABASE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid crop database JSON: {error}"
        )

    if not isinstance(data, dict):
        raise ValueError(
            "Crop database must contain a JSON object."
        )

    return data


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(value: Any) -> str:

    if value is None:
        return ""

    return " ".join(
        str(value).strip().lower().split()
    )


# ============================================================
# BUILD CROP DETAILS
# ============================================================

def build_crop_details(
    name: str,
    details: dict[str, Any]
) -> dict[str, Any]:

    return {
        "name": name,
        "season": details.get("season", []),
        "soil": details.get("soil", []),
        "water_requirement": details.get(
            "water_requirement",
            "Unknown"
        ),
        "duration": details.get(
            "duration",
            "Unknown"
        )
    }


# ============================================================
# GET CROP DETAILS
# ============================================================

def get_crop_details(crop_name: str):

    search_name = normalize_text(crop_name)

    if not search_name:
        return {
            "success": False,
            "message": "Crop name is required."
        }

    data = load_database()

    for name, details in data.items():

        if normalize_text(name) == search_name:

            result = build_crop_details(
                name,
                details
            )

            result["success"] = True

            return result

    return {
        "success": False,
        "message": (
            f"{crop_name} not found in crop database."
        )
    }


# ============================================================
# GET CROPS BY SOIL
# ============================================================

def get_crops_by_soil(soil_type: str):

    search_soil = normalize_text(soil_type)

    if not search_soil:
        return []

    data = load_database()

    suitable_crops = []

    for name, details in data.items():

        soils = details.get("soil", [])

        if not isinstance(soils, list):
            continue

        soil_match = any(
            normalize_text(soil) == search_soil
            for soil in soils
        )

        if soil_match:

            suitable_crops.append(
                build_crop_details(
                    name,
                    details
                )
            )

    return suitable_crops


# ============================================================
# SOIL + SEASON RECOMMENDATION
# ============================================================

def get_crops_by_soil_and_weather(
    soil_type: str,
    season: str
):

    search_soil = normalize_text(soil_type)
    search_season = normalize_text(season)

    if not search_soil or not search_season:
        return []

    data = load_database()

    suitable_crops = []

    for name, details in data.items():

        soils = details.get("soil", [])
        seasons = details.get("season", [])

        if not isinstance(soils, list):
            soils = []

        if not isinstance(seasons, list):
            seasons = []

        soil_match = any(
            normalize_text(soil) == search_soil
            for soil in soils
        )

        season_match = any(
            normalize_text(item) == search_season
            for item in seasons
        )

        if soil_match and season_match:

            suitable_crops.append(
                build_crop_details(
                    name,
                    details
                )
            )

    return suitable_crops


# ============================================================
# AUTO WEATHER + SOIL RECOMMENDATION
# ============================================================

def get_crop_recommendation(
    district: str,
    soil_type: str
):

    if not district or not district.strip():
        return {
            "success": False,
            "message": "District is required."
        }

    if not soil_type or not soil_type.strip():
        return {
            "success": False,
            "message": "Soil type is required."
        }

    # --------------------------------------------------------
    # FETCH WEATHER AUTOMATICALLY
    # --------------------------------------------------------

    try:

        weather = weather_prediction(
            district.strip()
        )

    except Exception as error:

        return {
            "success": False,
            "message": "Unable to fetch weather data.",
            "error": str(error)
        }

    if not isinstance(weather, dict):

        return {
            "success": False,
            "message": "Invalid weather data received."
        }

    # --------------------------------------------------------
    # GET SEASON FROM WEATHER API
    # --------------------------------------------------------

    season = weather.get("season")

    if not season:

        return {
            "success": False,
            "message": (
                "Season could not be determined "
                "from weather data."
            )
        }

    # --------------------------------------------------------
    # FIND SUITABLE CROPS
    # --------------------------------------------------------

    crops = get_crops_by_soil_and_weather(
        soil_type,
        season
    )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,

        "location": {
            "district": district.strip()
        },

        "soil": soil_type.strip(),

        "season": season,

        "weather": {
            "temperature": weather.get(
                "temperature"
            ),
            "humidity": weather.get(
                "humidity"
            ),
            "rainfall": weather.get(
                "rainfall"
            ),
            "weather": weather.get(
                "weather"
            ),
            "description": weather.get(
                "description"
            ),
            "wind_speed": weather.get(
                "wind_speed"
            )
        },

        "count": len(crops),

        "recommended_crops": crops
    }