from fastapi import APIRouter, HTTPException

from backend.services.weed_service import (
    get_weed_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/weed",
    tags=["Weed Management"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def weed_status():

    return {
        "status": "Weed Management Guidance is working"
    }


# ============================================================
# GUIDANCE
# ============================================================

@router.get("/guidance/{crop}")
def weed_guidance(
    crop: str
):

    result = get_weed_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result