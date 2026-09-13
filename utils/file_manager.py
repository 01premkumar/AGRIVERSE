# ==========================================================
# AGRIVERSE
# FILE MANAGER
# ==========================================================

import os
from pathlib import Path

from config.config import *

# ==========================================================
# DISPLAY PROJECT INFORMATION
# ==========================================================

def display_project_paths():

    print("=" * 60)

    print("🌾 AGRIVERSE PROJECT PATHS")

    print("=" * 60)

    print("PROJECT ROOT")
    print(PROJECT_ROOT)

    print()

    print("RAW DATASET")
    print(RAW_DATASET_PATH)

    print()

    print("PROCESSED DATASET")
    print(PROCESSED_DATASET_PATH)

    print()

    print("EXTRACTED DATASET")
    print(EXTRACTED_DATASET_PATH)

    print()

    print("MODEL PATH")
    print(MODEL_PATH)

    print()

    print("OUTPUT PATH")
    print(OUTPUT_PATH)

    print("=" * 60)

# ==========================================================
# DISPLAY FILES
# ==========================================================

def list_raw_datasets():

    print("=" * 60)

    print("📂 RAW DATASETS")

    print("=" * 60)

    FILES = os.listdir(RAW_DATASET_PATH)

    if len(FILES) == 0:

        print("❌ No Dataset Found")

    else:

        for FILE in FILES:

            print("✅", FILE)