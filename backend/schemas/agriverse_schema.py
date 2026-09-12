from pydantic import BaseModel


class AgriverseRequest(BaseModel):

    district: str
    soil: str

    nitrogen: float
    phosphorus: float
    potassium: float

    temperature: float
    humidity: float
    ph: float
    rainfall: float