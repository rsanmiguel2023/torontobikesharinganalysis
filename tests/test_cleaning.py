# tests/test_cleaning.py
import pandas as pd
import pytest

from data_processing.cleaning import clean_data  

def sample_base_df():
    """
    Base valid row that simulates what load_data() would return.
    """
    return pd.DataFrame(
        {
            "Trip Id": [1],
            "Trip Duration ": [600],  
            "Start Station Id": [100],
            "Start Time": ["2024-08-01 00:00"],
            "Start Station Name": ["Station A"],
            "End Station Id": [101],
            "End Time": ["2024-08-01 00:10"],
            "End Station Name": ["Station B"],
            "Bike Id": [1000],
            "User Type": ["Casual Member"],
            "Model": ["ICONIC"],
        }
    )

def test_clean_data_renames_trip_duration_and_parses_times():
    """
    'Trip Duration ' must be renamed to 'Trip Duration'
    and Start/End Time must be converted to datetime.
    """
    raw_data = sample_base_df()

    cleaned = clean_data(raw_data)

    # Column renamed
    assert "Trip Duration " not in cleaned.columns
    assert "Trip Duration" in cleaned.columns
    # Value preserved
    assert cleaned["Trip Duration"].iloc[0] == 600

    # Start/End Time converted to datetime
    assert str(cleaned["Start Time"].dtype).startswith("datetime64")
    assert str(cleaned["End Time"].dtype).startswith("datetime64")


def test_clean_data_drops_rows_with_invalid_times():
    """
    Rows where Start Time or End Time cannot be parsed
    should be removed from the cleaned data.
    """
    raw_data = pd.DataFrame(
        {
            "Trip Id": [1, 2],
            "Trip Duration ": [600, 600],
            "Start Station Id": [100, 200],
            "Start Time": ["2024-08-01 00:00", "NOT_A_TIME"],
            "Start Station Name": ["S1", "S2"],
            "End Station Id": [101, 201],
            "End Time": ["2024-08-01 00:10", "ALSO_BAD"],
            "End Station Name": ["E1", "E2"],
            "Bike Id": [111, 222],
            "User Type": ["Casual Member", "Annual Member"],
            "Model": ["ICONIC", "SMART"],
        }
    )

    cleaned = clean_data(raw_data)

    # Only the valid first row should survive
    assert len(cleaned) == 1
    assert cleaned["Trip Id"].iloc[0] == 1
    
def test_clean_data_replaces_missing_station_names_with_unknown():
    """
    Missing Start/End station names must be replaced with 'Unknown'.
    """
    raw_data = sample_base_df()
    raw_data.loc[0, "Start Station Name"] = None
    raw_data.loc[0, "End Station Name"] = None

    cleaned = clean_data(raw_data)

    assert cleaned["Start Station Name"].iloc[0] == "Unknown"
    assert cleaned["End Station Name"].iloc[0] == "Unknown"

def test_clean_data_drops_rows_with_missing_or_invalid_trip_id():
    """
    Rows with missing or non-numeric Trip Id should be dropped.
    We keep only rows with a valid positive Trip Id.
    """
    raw_data = pd.DataFrame(
        {
            "Trip Id": [1, None, "abc"],
            "Trip Duration ": [600, 700, 800],
            "Start Station Id": [100, 200, 300],
            "Start Time": ["2024-08-01 00:00"] * 3,
            "Start Station Name": ["S1", "S2", "S3"],
            "End Station Id": [101, 201, 301],
            "End Time": ["2024-08-01 00:10"] * 3,
            "End Station Name": ["E1", "E2", "E3"],
            "Bike Id": [111, 222, 333],
            "User Type": ["Casual Member"] * 3,
            "Model": ["ICONIC"] * 3,
        }
    )

    cleaned = clean_data(raw_data)

    # Only the row with Trip Id == 1 should remain
    assert len(cleaned) == 1
    assert cleaned["Trip Id"].iloc[0] == 1
