
import pandas as pd
import pip
import pytest


from data_processing.derive import derivetime_columns 



def test_derived_columns_exist(tmp_path):
    # Create sample CSV
    test_file = tmp_path / "test.csv"
    pd.DataFrame({
        "Start Time": ["2025-05-20 10:00:00"]
    }).to_csv(test_file, index=False)

    df = derivetime_columns(str(test_file))

    assert "Hour" in df.columns
    assert "Day" in df.columns
    assert "Month" in df.columns


def test_hour_range(tmp_path):
    test_file = tmp_path / "test.csv"
    pd.DataFrame({
        "Start Time": ["2025-05-20 23:00:00"]
    }).to_csv(test_file, index=False)

    df = derivetime_columns(str(test_file))
    assert 0 <= df.loc[0, "Hour"] <= 23


def test_day_range(tmp_path):
    test_file = tmp_path / "test.csv"
    pd.DataFrame({
        "Start Time": ["2025-05-15 09:00:00"]
    }).to_csv(test_file, index=False)

    df = derivetime_columns(str(test_file))
    assert 1 <= df.loc[0, "Day"] <= 31


def test_month_range(tmp_path):
    test_file = tmp_path / "test.csv"
    pd.DataFrame({
        "Start Time": ["2025-12-15 09:00:00"]
    }).to_csv(test_file, index=False)

    df = derivetime_columns(str(test_file))
    assert 1 <= df.loc[0, "Month"] <= 12


def test_invalid_start_time(tmp_path):
    test_file = tmp_path / "test.csv"
    pd.DataFrame({
        "Start Time": ["invalid"]
    }).to_csv(test_file, index=False)

    df = derivetime_columns(str(test_file))

    assert pd.isna(df.loc[0, "Hour"])
    assert pd.isna(df.loc[0, "Day"])
    assert pd.isna(df.loc[0, "Month"])





