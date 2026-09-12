from fastapi import APIRouter, HTTPException

from backend.services.harvest_service import (
    get_harvest_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/harvest",
    tags=["Harvesting Guidance"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def harvest_status():

    return {
        "status": "Harvesting Guidance is working"
    }


# ============================================================
# GUIDANCE
# ============================================================

@router.get("/guidance/{crop}")
def harvest_guidance(
    crop: str
):

    result = get_harvest_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result