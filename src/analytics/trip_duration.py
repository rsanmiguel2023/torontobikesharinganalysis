"""
Trip Duration Analytics Module

This module provides functions for analyzing trip duration statistics including
descriptive statistics (mean, median, min, max) and histogram generation.

Functions:
    calculate_duration_stats: Calculate comprehensive duration statistics
    valid_durations: Extract valid (non-negative, non-null) durations
    empty_stats: Return empty stats dictionary for edge cases
"""

from __future__ import annotations
from typing import Any, Dict
import numpy as np
import pandas as pd


def valid_durations(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Extract a Series of valid (non-negative, non-null) trip durations.

    This helper function filters out invalid duration values and makes
    calculate_duration_stats easier to read. This is where we would extend
    validation rules in the future.
    
    Args:
        df (pd.DataFrame): DataFrame containing trip duration data
        column (str): Name of the column containing duration values
    
    Returns:
        pd.Series: Series of valid duration values (non-negative, non-null)
    
    Example:
        >>> data = pd.DataFrame({'duration': [100, -5, 200, None, 300]})
        >>> valid = valid_durations(data, 'duration')
        >>> list(valid)
        [100.0, 200.0, 300.0]
    
    Notes:
        - Returns empty Series if df is None or column doesn't exist
        - Coerces values to numeric, setting invalid values to NaN
        - Filters out negative values and NaN/null values
    """
    if df is None or column not in df.columns:
        return pd.Series(dtype="float64")

    durations = pd.to_numeric(df[column], errors="coerce")
    return durations[(durations >= 0) & durations.notna()]


def calculate_duration_stats(
    df: pd.DataFrame,
    column: str = "Trip Duration",
    bins: int = 10,
) -> Dict[str, Any]:
    """
    Calculate comprehensive trip duration statistics.
    
    Computes descriptive statistics (mean, median, min, max, count) and
    generates histogram data for duration distribution analysis.
    
    Args:
        df (pd.DataFrame): DataFrame with trip data
        column (str): Column name containing duration values. Defaults to "Trip Duration"
        bins (int): Number of bins for histogram. Defaults to 10
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - mean (float): Average duration
            - median (float): Median duration  
            - min (float): Minimum duration
            - max (float): Maximum duration
            - count (int): Number of valid duration values
            - hist (dict): Histogram data with 'counts' and 'bin_edges'
    
    Example:
        >>> data = pd.DataFrame({
        ...     'Trip Duration': [100, 200, 150, 300, 250]
        ... })
        >>> stats = calculate_duration_stats(data, bins=3)
        >>> print(f"Mean: {stats['mean']:.1f}")
        Mean: 200.0
        >>> print(f"Count: {stats['count']}")
        Count: 5
    
    Notes:
        - Returns empty_stats() if no valid durations found
        - Histogram edges span from minimum to maximum valid duration
        - All statistics based only on valid (non-negative, non-null) durations
    """
    valid = valid_durations(df, column)

    if valid.empty:
        return empty_stats()

    # Compute descriptive statistics
    mean_val = float(valid.mean())
    median_val = float(valid.median())
    min_val = float(valid.min())
    max_val = float(valid.max())

    # Generate histogram (counts + bin edges)
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
    This ensures consistent return structure even when no valid data exists.
    
    Returns:
        Dict[str, Any]: Dictionary with None values for statistics and empty arrays for histogram
    
    Example:
        >>> stats = empty_stats()
        >>> stats['mean'] is None
        True
        >>> stats['count']
        0
    
    Notes:
        - All descriptive statistics set to None
        - Histogram arrays are empty numpy arrays
        - Same structure as calculate_duration_stats() for consistency
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
