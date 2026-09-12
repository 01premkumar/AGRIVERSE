from fastapi import APIRouter

from backend.schemas.assistant_schema import (
    AssistantContext
)

from backend.services.assistant_service import (
    farmer_assistant,
    assistant_with_context
)


router = APIRouter(
    prefix="/assistant",
    tags=["AI Farmer Assistant"]
)


# ============================================================
# BASIC ASK
# ============================================================

class FarmerQuestion(AssistantContext):
    pass


@router.post("/ask")
def ask_farmer(data: FarmerQuestion):

    return farmer_assistant(
        data.question
    )


# ============================================================
# CONTEXT-AWARE ASSISTANT
# ============================================================

@router.post("/context")
def context_assistant(
    data: AssistantContext
):

    return assistant_with_context(
        data
    )


# ============================================================
# STATUS
# ============================================================

@router.get("/status")
def assistant_status():

    return {
        "status": "AGRIVERSE Farmer Assistant is working"
    }