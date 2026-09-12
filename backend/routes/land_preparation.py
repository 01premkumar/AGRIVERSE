from fastapi import APIRouter, HTTPException

from backend.services.land_preparation_service import (
    get_land_preparation_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/land-preparation",
    tags=["Land Preparation"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def land_preparation_status():

    return {
        "status": "Land Preparation Guidance is working"
    }


# ============================================================
# GUIDANCE
# ============================================================

@router.get("/guidance/{crop}")
def land_preparation_guidance(
    crop: str
):

    result = get_land_preparation_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result