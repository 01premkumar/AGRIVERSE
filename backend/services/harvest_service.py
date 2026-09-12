import json
from pathlib import Path
from typing import Any


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    BASE_DIR
    / "knowledge_base"
    / "harvesting"
    / "harvest_database.json"
)


# ============================================================
# LOAD DATABASE
# ============================================================

def load_harvest_database() -> dict[str, Any]:

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Harvest database not found: {DATABASE_PATH}"
        )

    try:
        with open(
            DATABASE_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            database = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid harvest database JSON: {error}"
        )

    if not isinstance(database, dict):
        raise ValueError(
            "Harvest database must contain a JSON object."
        )

    return database


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value: Any) -> str:

    if value is None:
        return ""

    return " ".join(
        str(value).strip().lower().split()
    )


# ============================================================
# FIND CROP
# ============================================================

def find_crop(
    database: dict[str, Any],
    crop_name: str
):

    search_crop = normalize_text(crop_name)

    for name, data in database.items():

        if normalize_text(name) == search_crop:
            return name, data

    return None, None


# ============================================================
# GET HARVEST GUIDANCE
# ============================================================

def get_harvest_guidance(
    crop: str
):

    # --------------------------------------------------------
    # Validate crop
    # --------------------------------------------------------

    crop_key = normalize_text(crop)

    if not crop_key:

        return {
            "success": False,
            "crop": crop,
            "message": "Crop name is required."
        }


    # --------------------------------------------------------
    # Load database
    # --------------------------------------------------------

    database = load_harvest_database()


    # --------------------------------------------------------
    # Find crop
    # --------------------------------------------------------

    matched_crop, crop_data = find_crop(
        database,
        crop_key
    )


    # --------------------------------------------------------
    # Crop not found
    # --------------------------------------------------------

    if matched_crop is None:

        return {
            "success": False,
            "crop": crop.strip(),
            "message": (
                "Harvesting guidance is "
                "not available for this crop yet."
            )
        }


    # --------------------------------------------------------
    # Validate crop data
    # --------------------------------------------------------

    if not isinstance(crop_data, dict):

        return {
            "success": False,
            "crop": matched_crop,
            "message": (
                "Invalid harvesting guidance data "
                "for this crop."
            )
        }


    # --------------------------------------------------------
    # Return guidance
    # --------------------------------------------------------

    return {
        "success": True,
        "crop": matched_crop,

        "maturity_signs": crop_data.get(
            "maturity_signs",
            []
        ),

        "harvest_timing": crop_data.get(
            "harvest_timing",
            []
        ),

        "harvest_method": crop_data.get(
            "harvest_method",
            []
        ),

        "post_harvest": crop_data.get(
            "post_harvest",
            []
        ),

        "precautions": crop_data.get(
            "precautions",
            []
        )
    }