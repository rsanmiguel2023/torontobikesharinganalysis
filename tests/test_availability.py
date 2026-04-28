import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from analytics.peak_usage import analyze_peak_usage

def sample_data():
    """
    Sample dataset:
    - Hour 8 has 3 trips
    - Day 2 (Wednesday) has most trips (4)
    """
    data = {
        "start_time": [
            "2023-09-18 08:15",  # Monday - 8
            "2023-09-18 08:45",
            "2023-09-19 09:15",  # Tuesday - 9
            "2023-09-20 08:05",  # Wednesday - 8
            "2023-09-20 08:55",
            "2023-09-20 10:30",
            "2023-09-20 12:00"
        ]
    }
    return pd.DataFrame(data)




def test_hourly_aggregation():
    df = sample_data()
    result = analyze_peak_usage(df)

    assert result["hourly_counts"][8] == 4
    assert result["hourly_counts"][9] == 1
    assert result["hourly_counts"][10] == 1
    assert result["hourly_counts"][12] == 1


def test_weekday_aggregation():
    df = sample_data()
    result = analyze_peak_usage(df)

    # Monday = 0 (2 trips)
    assert result["weekday_counts"][0] == 2
    # Tuesday = 1 (1 trip)
    assert result["weekday_counts"][1] == 1
    # Wednesday = 2 (4 trips)
    assert result["weekday_counts"][2] == 4


def test_heatmap_shape():
    df = sample_data()
    result = analyze_peak_usage(df)

    assert isinstance(result["heatmap_matrix"], np.ndarray)
    assert result["heatmap_matrix"].shape == (7, 24)


def test_peak_detection():
    df = sample_data()
    result = analyze_peak_usage(df)

    # Peak hour = 8
    assert result["peak_hour"] == 8

    # Peak weekday = 2 (Wednesday)
    assert result["peak_day"] == 2


def test_empty_dataframe():
    df = pd.DataFrame(columns=["start_time"])
    result = analyze_peak_usage(df)

    assert result["peak_hour"] is None
    assert result["peak_day"] is None
    assert result["heatmap_matrix"].shape == (7, 24)
    assert result["hourly_counts"].empty
