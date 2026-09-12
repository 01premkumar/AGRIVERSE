from pydantic import BaseModel


# ============================================================
# EXISTING CROP ML REQUEST
# ============================================================

class CropRequest(BaseModel):

    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


# ============================================================
# SMART CROP RECOMMENDATION REQUEST
# ============================================================

class SmartCropRequest(BaseModel):

    district: str
    soil: str
    season: str

    temperature: float
    humidity: float
    rainfall: float