from datetime import date

from pydantic import BaseModel, Field


# ============================================================
# CROP TIMELINE REQUEST
# ============================================================

class CropTimelineRequest(BaseModel):

    crop: str = Field(
        ...,
        min_length=2,
        description="Crop name"
    )

    planting_date: date = Field(
        ...,
        description="Crop planting date in YYYY-MM-DD format"
    )

    district: str = Field(
        ...,
        min_length=2,
        description="Tamil Nadu district name"
    )