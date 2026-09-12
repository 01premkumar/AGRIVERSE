from fastapi import APIRouter, UploadFile, File

from backend.services.soil_service import soil_prediction


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/soil",
    tags=["Soil AI"]
)


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def soil_status():

    return {
        "status": "Soil AI is working"
    }


# ============================================================
# SOIL PREDICTION
# ============================================================

@router.post("/predict")
async def predict_soil(
    file: UploadFile = File(...)
):

    return await soil_prediction(file)