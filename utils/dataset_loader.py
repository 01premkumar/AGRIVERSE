# ==========================================================
# AGRIVERSE
# DATASET LOADER
# ==========================================================

import pandas as pd
from pathlib import Path
from config.config import *

# ==========================================================
# LOAD CSV DATASET
# ==========================================================

def load_csv_dataset(file_name):

    dataset_path = RAW_DATASET_PATH / file_name

    if not dataset_path.exists():
        raise FileNotFoundError(f"{file_name} not found")

    dataframe = pd.read_csv(dataset_path)

    print("=" * 60)
    print(f"✅ {file_name} Loaded Successfully")
    print("=" * 60)

    print("Rows    :", dataframe.shape[0])
    print("Columns :", dataframe.shape[1])

    return dataframe