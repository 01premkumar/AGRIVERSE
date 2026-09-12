from fastapi import APIRouter, UploadFile, File, Form

from backend.services.soil_service import soil_prediction
from backend.services.crop_service import crop_prediction


router = APIRouter(
    prefix="/agriverse",
    tags=["AGRIVERSE"]
)


@router.post("/recommend-with-soil")
async def recommend_with_soil(
    file: UploadFile = File(...),

    district: str = Form(...),

    nitrogen: float = Form(...),
    phosphorus: float = Form(...),
    potassium: float = Form(...),

    temperature: float = Form(...),
    humidity: float = Form(...),
    ph: float = Form(...),
    rainfall: float = Form(...)
):

    # 1. Predict soil from image
    soil_result = await soil_prediction(file)

    # 2. Prepare crop data
    crop_data = {
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }

    # 3. Predict suitable crop
    crop_result = crop_prediction(crop_data)

    # 4. Final AGRIVERSE result
    return {
        "district": district,

        "soil_analysis": soil_result,

        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        },

        "crop_recommendation": crop_result
    }