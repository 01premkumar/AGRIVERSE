# ==========================================================
# AGRIVERSE CONFIGURATION
# ==========================================================

from pathlib import Path
import os


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ==========================================================
# DATASET FOLDERS
# ==========================================================

RAW_DATASET_PATH = (
    PROJECT_ROOT / "datasets" / "raw"
)

PROCESSED_DATASET_PATH = (
    PROJECT_ROOT / "datasets" / "processed"
)

EXTRACTED_DATASET_PATH = (
    PROJECT_ROOT / "datasets" / "extracted"
)


# ==========================================================
# MODELS
# ==========================================================

MODEL_PATH = (
    PROJECT_ROOT / "models"
)


# ==========================================================
# OUTPUTS
# ==========================================================

OUTPUT_PATH = (
    PROJECT_ROOT / "outputs"
)


# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================

RAW_DATASET_PATH.mkdir(
    parents=True,
    exist_ok=True
)

PROCESSED_DATASET_PATH.mkdir(
    parents=True,
    exist_ok=True
)

EXTRACTED_DATASET_PATH.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_PATH.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# WEATHER API CONFIGURATION
# ==========================================================

# IMPORTANT:
# Do NOT hardcode the API key here.
#
# Windows PowerShell:
#
# $env:AGRIVERSE_WEATHER_API_KEY="YOUR_NEW_API_KEY"
#
# Then start the backend from the same terminal.

WEATHER_API_KEY = os.getenv(
    "AGRIVERSE_WEATHER_API_KEY",
    ""
)


# ==========================================================
# CONFIG STATUS
# ==========================================================

print("🌾 AGRIVERSE CONFIG LOADED")

if WEATHER_API_KEY:
    print("🌦️ Weather API Key: Loaded")
else:
    print(
        "⚠️ Weather API Key: Not configured"
    )