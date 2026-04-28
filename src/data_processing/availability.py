# src/data_processing/availability.py
import numpy as np
import pandas as pd

from utils.dataframe_utils import (
    coerce_datetime_and_dropna,
    add_hour_and_weekday,
    counts_over_range,
)


def _empty_peak_usage_result() -> dict:
    """
    Shared structure for the 'no data' case so we don't repeat the same
    dictionary in multiple places.
    """
    return {
        "hourly_counts": pd.Series(dtype=int),
        "weekday_counts": pd.Series(dtype=int),
        "heatmap_matrix": np.zeros((7, 24)),
        "peak_hour": None,
        "peak_day": None,
    }


def analyze_peak_usage(df: pd.DataFrame, datetime_col: str = "start_time") -> dict:
    """
    Analyzes peak usage time for bike trips.

    Args:
        df (pd.DataFrame): Cleaned bike trip data
        datetime_col (str): Column containing trip start time

    Returns:
        dict:
        {
            "hourly_counts": pd.Series,
            "weekday_counts": pd.Series,
            "heatmap_matrix": np.ndarray (7x24),
            "peak_hour": int,
            "peak_day": int
        }
    """
    # Handle empty dataframe
    if df.empty or datetime_col not in df.columns:
        return _empty_peak_usage_result()

    # Ensure datetime format (shared helper: coerce + drop NaT)
    df = coerce_datetime_and_dropna(df, datetime_col)

    if df.empty:
        return _empty_peak_usage_result()

    # Add hour and weekday columns via shared helper
    df = add_hour_and_weekday(df, datetime_col)

    # 1. Hourly aggregation
    hourly_counts = counts_over_range(df["hour"], range(24))
    df_unique = df.drop_duplicates(subset=["weekday", "hour"])
    # hourly_counts = df["hour"].value_counts().sort_index()

    # 2. Weekday aggregation
    weekday_counts = counts_over_range(df["weekday"], range(7))
    # weekday_counts = df["weekday"].value_counts().sort_index()

    # 3. Heatmap matrix (7x24)
    heatmap_matrix = np.zeros((7, 24))

    for _, row in df.iterrows():
        heatmap_matrix[int(row["weekday"])][int(row["hour"])] += 1

    # 4. Identify peak hour & day
    peak_hour = hourly_counts.idxmax() if hourly_counts.sum() > 0 else None
    peak_day = weekday_counts.idxmax() if weekday_counts.sum() > 0 else None

    return {
        "hourly_counts": hourly_counts,
        "weekday_counts": weekday_counts,
        "heatmap_matrix": heatmap_matrix,
        "peak_hour": peak_hour,
        "peak_day": peak_day,
    }
