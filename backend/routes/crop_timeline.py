from fastapi import APIRouter, HTTPException

from backend.schemas.crop_timeline_schema import (
    CropTimelineRequest
)

from backend.services.crop_timeline_service import (
    get_crop_timeline
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/crop-timeline",
    tags=["Crop Timeline"]
)


# ============================================================
# GENERATE CROP TIMELINE
# ============================================================

@router.post("/generate")
def generate_timeline(
    data: CropTimelineRequest
):

    # --------------------------------------------------------
    # Validate district
    # --------------------------------------------------------

    district = data.district.strip()

    if not district:

        raise HTTPException(
            status_code=400,
            detail="District is required."
        )


    # --------------------------------------------------------
    # Validate crop
    # --------------------------------------------------------

    crop = data.crop.strip()

    if not crop:

        raise HTTPException(
            status_code=400,
            detail="Crop name is required."
        )


    # --------------------------------------------------------
    # Generate timeline
    # --------------------------------------------------------

    try:

        result = get_crop_timeline(
            crop,
            data.planting_date,
            district
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to generate crop timeline."
            )
        ) from error


    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return result