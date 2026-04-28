"""
Peak Usage Analytics Module

This module provides functions for analyzing peak usage patterns in bike sharing data,
including hourly and weekday aggregations, heatmap generation, and peak identification.

Functions:
    analyze_peak_usage: Identifies peak usage hours and days with heatmap data
"""

import numpy as np
import pandas as pd


def analyze_peak_usage(df: pd.DataFrame, datetime_col: str = "start_time") -> dict:
    """
    Analyzes peak usage time for bike trips.
    
    Performs hourly and weekday aggregations to identify when bike usage is highest.
    Returns data suitable for heatmap visualization and peak time identification.

    Args:
        df (pd.DataFrame): Cleaned bike trip data
        datetime_col (str): Column containing trip start time. Defaults to "start_time"

    Returns:
        dict: Dictionary containing:
            - hourly_counts (pd.Series): Trip counts by hour (0-23)
            - weekday_counts (pd.Series): Trip counts by weekday (0=Monday, 6=Sunday)
            - heatmap_matrix (np.ndarray): 7x24 matrix (weekday x hour) of trip counts
            - peak_hour (int or None): Hour with maximum trips (0-23)
            - peak_day (int or None): Weekday with maximum trips (0-6)
    
    Example:
        >>> data = pd.DataFrame({
        ...     'start_time': pd.date_range('2024-01-01', periods=100, freq='H')
        ... })
        >>> result = analyze_peak_usage(data, 'start_time')
        >>> print(f"Peak hour: {result['peak_hour']}")
        >>> print(f"Peak day: {result['peak_day']}")
    
    Notes:
        - Returns empty/zero data if DataFrame is empty or datetime column is missing
        - Drops rows with null datetime values before analysis
        - Weekday encoding: 0=Monday, 1=Tuesday, ..., 6=Sunday (pandas default)
    """
    # Handle empty dataframe or missing column
    if df.empty or datetime_col not in df.columns:
        return {
            "hourly_counts": pd.Series(dtype=int),
            "weekday_counts": pd.Series(dtype=int),
            "heatmap_matrix": np.zeros((7, 24)),
            "peak_hour": None,
            "peak_day": None
        }

    # Ensure datetime format and remove nulls
    df = df.copy()
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    df = df.dropna(subset=[datetime_col])

    if df.empty:
        return {
            "hourly_counts": pd.Series(dtype=int),
            "weekday_counts": pd.Series(dtype=int),
            "heatmap_matrix": np.zeros((7, 24)),
            "peak_hour": None,
            "peak_day": None
        }

    # Extract hour and weekday components
    df["hour"] = df[datetime_col].dt.hour
    df["weekday"] = df[datetime_col].dt.weekday  # Monday=0, Sunday=6

    # 1. Hourly aggregation - count trips by hour
    hourly_counts = df["hour"].value_counts().sort_index()
    hourly_counts = hourly_counts.reindex(range(24), fill_value=0)

    # 2. Weekday aggregation - count trips by day of week
    weekday_counts = df["weekday"].value_counts().sort_index()
    weekday_counts = weekday_counts.reindex(range(7), fill_value=0)

    # 3. Create heatmap matrix (7 days x 24 hours)
    heatmap_matrix = np.zeros((7, 24))
    for _, row in df.iterrows():
        heatmap_matrix[int(row["weekday"])][int(row["hour"])] += 1

    # 4. Identify peak hour and day
    peak_hour = hourly_counts.idxmax() if hourly_counts.sum() > 0 else None
    peak_day = weekday_counts.idxmax() if weekday_counts.sum() > 0 else None

    return {
        "hourly_counts": hourly_counts,
        "weekday_counts": weekday_counts,
        "heatmap_matrix": heatmap_matrix,
        "peak_hour": peak_hour,
        "peak_day": peak_day
    }
