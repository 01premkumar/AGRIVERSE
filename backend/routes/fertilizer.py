from fastapi import APIRouter, HTTPException

from backend.services.fertilizer_service import (
    get_fertilizer_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/fertilizer",
    tags=["Organic Fertilizer"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def fertilizer_status():

    return {
        "status": "Organic Fertilizer Guidance is working"
    }


# ============================================================
# GUIDANCE
# ============================================================

@router.get("/guidance/{crop}")
def fertilizer_guidance(
    crop: str
):

    result = get_fertilizer_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result