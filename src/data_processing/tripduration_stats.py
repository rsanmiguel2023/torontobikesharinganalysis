# src/data_processing/tripduration_stats.py
from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd

from utils.dataframe_utils import positive_numeric_series


def valid_durations(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Extract a Series of valid (non-negative, non-null) trip durations.

    This helper keeps calculate_duration_stats easier to read
    and is also where we would extend rules in the future.
    """
    # Delegate to the shared numeric helper so the rules for "valid numeric
    # values" (coerce to numeric, drop NaNs, keep >= 0) live in one place.
    return positive_numeric_series(df, column, allow_zero=True)


def calculate_duration_stats(
    df: pd.DataFrame,
    column: str = "Trip Duration",
    bins: int = 10,
) -> Dict[str, Any]:
    valid = valid_durations(df, column)

    if valid.empty:
        return empty_stats()

    # 2) Compute descriptive stats
    mean_val = float(valid.mean())
    median_val = float(valid.median())
    min_val = float(valid.min())
    max_val = float(valid.max())

    # 3) Histogram (counts + bin edges)
    counts, bin_edges = np.histogram(valid, bins=bins)

    stats: Dict[str, Any] = {
        "mean": mean_val,
        "median": median_val,
        "min": min_val,
        "max": max_val,
        "count": int(valid.count()),
        "hist": {
            "counts": counts,
            "bin_edges": bin_edges,
        },
    }
    return stats


def empty_stats() -> Dict[str, Any]:
    """
    Return a consistent stats dictionary for the 'no valid data' case.

    Used so the function handles empty inputs gracefully without raising errors.
    """
    return {
        "mean": None,
        "median": None,
        "min": None,
        "max": None,
        "count": 0,
        "hist": {
            "counts": np.array([]),
            "bin_edges": np.array([]),
        },
    }
