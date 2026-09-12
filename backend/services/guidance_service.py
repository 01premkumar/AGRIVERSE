import json
from pathlib import Path
from typing import Any


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

GUIDANCE_DIR = (
    BASE_DIR
    / "knowledge_base"
    / "guidance"
)


# ============================================================
# NORMALIZE CROP NAME
# ============================================================

def normalize_crop_name(
    crop: Any
) -> str:

    if crop is None:
        return ""

    return " ".join(
        str(crop).strip().lower().split()
    )


# ============================================================
# GET GUIDANCE
# ============================================================

def get_guidance(
    crop: str
):

    crop_key = normalize_crop_name(
        crop
    )

    # --------------------------------------------------------
    # Validate crop
    # --------------------------------------------------------

    if not crop_key:

        return {
            "success": False,
            "crop": crop,
            "message": "Crop name is required."
        }


    # --------------------------------------------------------
    # Check guidance directory
    # --------------------------------------------------------

    if not GUIDANCE_DIR.exists():

        return {
            "success": False,
            "crop": crop,
            "message": (
                "Guidance database is not available."
            )
        }


    # --------------------------------------------------------
    # Build safe filename
    # --------------------------------------------------------

    safe_crop = crop_key.replace(
        " ",
        "_"
    )

    guidance_file = (
        GUIDANCE_DIR
        / f"{safe_crop}.json"
    )


    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not guidance_file.exists():

        return {
            "success": False,
            "crop": crop.strip(),
            "message": (
                "Guidance is not available "
                "for this crop yet."
            )
        }


    # --------------------------------------------------------
    # Read JSON
    # --------------------------------------------------------

    try:

        with open(
            guidance_file,
            "r",
            encoding="utf-8"
        ) as file:

            guidance_data = json.load(
                file
            )

    except json.JSONDecodeError as error:

        return {
            "success": False,
            "crop": crop.strip(),
            "message": (
                "Guidance data is invalid."
            ),
            "error": str(error)
        }


    # --------------------------------------------------------
    # Validate JSON structure
    # --------------------------------------------------------

    if not isinstance(
        guidance_data,
        dict
    ):

        return {
            "success": False,
            "crop": crop.strip(),
            "message": (
                "Invalid guidance data "
                "for this crop."
            )
        }


    # --------------------------------------------------------
    # Return guidance
    # --------------------------------------------------------

    return {
        "success": True,
        "crop": crop.strip(),
        "guidance": guidance_data
    }