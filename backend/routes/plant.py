from fastapi import APIRouter, UploadFile, File

from backend.services.plant_service import plant_prediction

router = APIRouter(
    prefix="/plant",
    tags=["Plant AI"]
)


@router.get("/status")
def status():
    return {
        "status": "Plant AI is working"
    }


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    return await plant_prediction(file)