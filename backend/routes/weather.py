from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.services.weather_service import weather_prediction


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class WeatherRequest(BaseModel):

    district: str = Field(
        ...,
        min_length=2,
        description="Tamil Nadu district name"
    )


# ============================================================
# CURRENT WEATHER
# ============================================================

@router.post("/")
def weather(data: WeatherRequest):

    district = data.district.strip()

    return weather_prediction(district)