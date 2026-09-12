from fastapi import APIRouter, HTTPException

from backend.services.irrigation_service import (
    get_irrigation_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/irrigation",
    tags=["Irrigation / Water Management"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def irrigation_status():

    return {
        "status": "Irrigation Guidance is working"
    }


# ============================================================
# GUIDANCE
# ============================================================

@router.get("/guidance/{crop}")
def irrigation_guidance(
    crop: str
):

    result = get_irrigation_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result