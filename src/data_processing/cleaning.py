import pandas as pd

from utils.dataframe_utils import (
    positive_numeric_series,
    coerce_datetime_and_dropna,
)


def _normalize_trip_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert Trip Id to numeric and keep only positive values.

    This helper just makes clean_data easier to read.
    """
    df = df.copy()

    # Use shared numeric helper so the "positive numeric" rule lives in one place
    valid_ids = positive_numeric_series(df, "Trip Id", allow_zero=False)

    # Keep only rows whose Trip Id is valid (index alignment does the filtering)
    df = df.loc[valid_ids.index]

    return df


def clean_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the bike-share dataset so that trip records are consistent.
    """
    df = raw_df.copy()

    if "Trip Duration " in df.columns and "Trip Duration" not in df.columns:
        df = df.rename(columns={"Trip Duration ": "Trip Duration"})

    # Use the helper here
    df = _normalize_trip_ids(df)

    # Convert Start/End Time safely using shared datetime helper
    df = coerce_datetime_and_dropna(df, "Start Time")
    df = coerce_datetime_and_dropna(df, "End Time")

    for col in ["Start Station Name", "End Station Name"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df.reset_index(drop=True)