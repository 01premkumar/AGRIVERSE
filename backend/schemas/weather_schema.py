from pydantic import BaseModel, Field


class WeatherRequest(BaseModel):

    district: str = Field(
        ...,
        min_length=2,
        description="Tamil Nadu district name"
    )