# src/data_processing/derive.py
import pandas as pd
from pathlib import Path

from utils.dataframe_utils import (
    coerce_datetime,           # <-- new helper
    add_hour_day_month,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_ROOT / "data"


def derivetime_columns(file_path: str) -> pd.DataFrame:
    # Read input
    df = pd.read_csv(file_path)

    # Ensure Start Time exists
    if "Start Time" not in df.columns:
        raise KeyError("Start Time column is missing from DataFrame")

    # Convert safely (keep rows; invalid values become NaT)
    df = coerce_datetime(df, "Start Time")

    # Use shared helper to add Hour / Day / Month
    df = add_hour_day_month(df, "Start Time")

    # Prepare processed directory
    processed_dir = DATA_FOLDER / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Output path
    file_path = Path(file_path)
    output_path = processed_dir / file_path.name

    # Save CSV
    df.to_csv(output_path, index=False)

    return df
