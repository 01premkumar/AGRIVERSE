from fastapi import APIRouter, HTTPException

from backend.services.guidance_service import (
    get_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/guidance",
    tags=["Guidance"]
)


# ============================================================
# GET GUIDANCE
# ============================================================

@router.get("/{crop}")
def guidance(
    crop: str
):

    result = get_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result