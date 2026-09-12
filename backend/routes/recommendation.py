from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.recommendation_service import (
    get_crop_details,
    get_crops_by_soil,
    get_crop_recommendation
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class CropRecommendationRequest(BaseModel):

    district: str = Field(
        ...,
        min_length=2,
        description="Tamil Nadu district"
    )

    soil: str = Field(
        ...,
        min_length=2,
        description="Soil type"
    )


# ============================================================
# CROP DETAILS
# ============================================================

@router.get("/{crop_name}")
def recommendation(crop_name: str):

    return get_crop_details(crop_name)


# ============================================================
# SOIL BASED RECOMMENDATION
# ============================================================

@router.post("/by-soil")
def recommendation_by_soil(
    data: CropRecommendationRequest
):

    crops = get_crops_by_soil(
        data.soil
    )

    return {
        "success": True,
        "district": data.district.strip(),
        "soil": data.soil.strip(),
        "count": len(crops),
        "recommended_crops": crops
    }


# ============================================================
# AUTO WEATHER + SOIL RECOMMENDATION
# ============================================================

@router.post("/by-context")
def recommendation_by_context(
    data: CropRecommendationRequest
):

    return get_crop_recommendation(
        district=data.district,
        soil_type=data.soil
    )