from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.crop import router as crop_router
from backend.routes.weather import router as weather_router
from backend.routes.recommendation import router as recommendation_router
from backend.routes.guidance import router as guidance_router
from backend.routes.plant import router as plant_router
from backend.routes.soil import router as soil_router
from backend.routes.assistant import router as assistant_router
from backend.routes.agriverse import router as agriverse_router
from backend.routes.crop_timeline import router as crop_timeline_router
from backend.routes.irrigation import (
    router as irrigation_router
)

# NEW
from backend.routes.seed import router as seed_router
from backend.routes.land_preparation import (
    router as land_preparation_router
)
from backend.routes.fertilizer import (
    router as fertilizer_router
)
from backend.routes.weed import (
    router as weed_router
)
from backend.routes.harvest import (
    router as harvest_router
)
from backend.routes.tree import (
    router as tree_router
)

# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="AGRIVERSE API",
    description="AI Personal Farming Assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AGRIVERSE Backend Running Successfully"
    }


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    crop_router,
    prefix="/crop",
    tags=["Crop AI"]
)

app.include_router(weather_router)

app.include_router(recommendation_router)

app.include_router(guidance_router)

app.include_router(plant_router)

app.include_router(soil_router)

app.include_router(assistant_router)

app.include_router(agriverse_router)

app.include_router(crop_timeline_router)


# ============================================================
# SEED / SEEDLING / SAPLING GUIDANCE
# ============================================================

app.include_router(seed_router)
app.include_router(
    land_preparation_router
)
app.include_router(
    fertilizer_router
)
app.include_router(
    irrigation_router
)
app.include_router(
    weed_router
)
app.include_router(
    harvest_router
)
app.include_router(
    tree_router
)