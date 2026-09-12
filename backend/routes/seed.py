from fastapi import APIRouter, HTTPException

from backend.services.seed_service import (
    get_seed_guidance
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/seed",
    tags=["Seed Guidance"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def seed_status():

    return {
        "status": "Seed Guidance is working"
    }


# ============================================================
# GET GUIDANCE
# ============================================================

@router.get("/guidance/{crop}")
def seed_guidance(crop: str):

    result = get_seed_guidance(
        crop
    )

    if not result["success"]:

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result