from pydantic import BaseModel
from typing import Optional


class AssistantContext(BaseModel):

    question: str

    district: Optional[str] = None

    soil: Optional[str] = None

    crop: Optional[str] = None

    disease: Optional[str] = None