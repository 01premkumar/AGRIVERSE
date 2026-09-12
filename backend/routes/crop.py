from fastapi import APIRouter

from backend.schemas.crop_schema import (
    CropRequest,
    SmartCropRequest
)

from backend.services.crop_service import crop_prediction
from backend.services.recommendation_service import (
    get_crops_by_soil_and_weather
)


router = APIRouter()


@router.post("/predict")
def predict(data: CropRequest):

    return crop_prediction(
        data.model_dump()
    )


@router.post("/smart-recommend")
def smart_recommend(data: SmartCropRequest):

    crops = get_crops_by_soil_and_weather(
        data.soil,
        data.season
    )

    return {
        "district": data.district,
        "soil": data.soil,
        "season": data.season,
        "weather": {
            "temperature": data.temperature,
            "humidity": data.humidity,
            "rainfall": data.rainfall
        },
        "recommended_crops": crops
    }