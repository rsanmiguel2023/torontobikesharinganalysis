# src/utils/dataframe_utils.py

from typing import Iterable

import pandas as pd
import numpy as np  # if you are using np here already


def positive_numeric_series(
    df: pd.DataFrame,
    column: str,
    *,
    allow_zero: bool = True,
) -> pd.Series:
    """
    Convert a column to numeric and return only non-null, non-negative values.

    If the DataFrame is None or the column is missing, an empty Series is
    returned so callers can handle the "no data" case safely.
    """
    if df is None or column not in df.columns:
        return pd.Series(dtype="float64")

    values = pd.to_numeric(df[column], errors="coerce")

    if allow_zero:
        mask = (values >= 0) & values.notna()
    else:
        mask = (values > 0) & values.notna()

    return values[mask]


def coerce_datetime(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Convert a column to datetime (errors='coerce') but DO NOT drop rows.

    Invalid values become NaT. This matches the original behaviour in
    derivetime_columns, where tests expect Hour/Day/Month to be NaN
    instead of the entire row being removed.
    """
    if df is None:
        return pd.DataFrame()

    if column not in df.columns:
        return df.copy()

    result = df.copy()
    result[column] = pd.to_datetime(result[column], errors="coerce")
    return result


def coerce_datetime_and_dropna(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Convert a column to datetime (errors='coerce') and drop rows where it is NaT.

    Returns a *new* DataFrame. The original input is not modified.
    """
    if df is None:
        return pd.DataFrame()

    if column not in df.columns:
        # Nothing to convert – return a copy so callers don't get surprises.
        return df.copy()

    result = df.copy()
    result[column] = pd.to_datetime(result[column], errors="coerce")
    result = result.dropna(subset=[column])
    return result


def add_hour_day_month(df: pd.DataFrame, datetime_col: str = "Start Time") -> pd.DataFrame:
    """
    Add Hour, Day, and Month columns derived from a datetime column.

    Assumes the datetime column is already of a datetime64 dtype.
    """
    result = df.copy()
    series = result[datetime_col]

    result["Hour"] = series.dt.hour
    result["Day"] = series.dt.day
    result["Month"] = series.dt.month
    return result


def add_hour_and_weekday(df: pd.DataFrame, datetime_col: str) -> pd.DataFrame:
    """
    Add hour and weekday columns derived from a datetime column.

    Assumes the datetime column is already of a datetime64 dtype.
    """
    result = df.copy()
    series = result[datetime_col]

    result["hour"] = series.dt.hour
    result["weekday"] = series.dt.weekday  # Monday=0, Sunday=6
    return result


def counts_over_range(series: pd.Series, values: Iterable[int]) -> pd.Series:
    """
    Compute value counts for a Series and reindex over a full range of values.

    Any missing values in the range are filled with 0. This is handy for
    time-of-day or weekday counts where we always want, for example, 0–23.
    """
    counts = series.value_counts().sort_index()
    return counts.reindex(list(values), fill_value=0)
