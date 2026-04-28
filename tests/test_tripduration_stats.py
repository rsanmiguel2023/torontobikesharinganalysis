# tests/test_analytics.py
import pandas as pd
import pytest


from analytics.trip_duration import calculate_duration_stats  


def sample_duration_df():
    """Simple DataFrame with valid trip durations for testing."""
    return pd.DataFrame(
        {
            "Trip Duration": [5, 10, 15, 20, 25], 
        }
    )


def test_calculate_duration_stats_returns_all_descriptive_values():
    """
    Function  calculate mean, median, min, max for trip length.
    """
    df = sample_duration_df()

    stats = calculate_duration_stats(df, column="Trip Duration")

    # All four keys exist
    assert "mean" in stats
    assert "median" in stats
    assert "min" in stats
    assert "max" in stats

    # All values are numeric (not None / NaN)
    for key in ["mean", "median", "min", "max"]:
        value = stats[key]
        assert value is not None
        assert isinstance(value, (int, float))


def test_calculate_duration_stats_respects_order_min_median_mean_max():
    """
    For an increasing list of durations we expect:
    min <= median <= mean <= max
    """
    df = sample_duration_df()

    stats = calculate_duration_stats(df, column="Trip Duration")

    assert stats["min"] <= stats["median"] <= stats["mean"] <= stats["max"]


def test_calculate_duration_stats_excludes_negative_and_missing():
    """
    Negative or missing trip lengths must is excluded from computation.
    Only the positive, non-null durations should be used.
    """
    df = pd.DataFrame(
        {
            "Trip Duration": [5, -10, None, 15],  # valid: 5 and 15
        }
    )

    stats = calculate_duration_stats(df, column="Trip Duration")

    # With valid values [5, 15]
    assert stats["min"] == 5
    assert stats["max"] == 15
    assert stats["median"] == 10
    assert stats["mean"] == 10


def test_calculate_duration_stats_returns_histogram_info():
    """
    Function must support histogram generation via bin edges and counts.
    """
    df = sample_duration_df()

    stats = calculate_duration_stats(df, column="Trip Duration")

    assert "hist" in stats
    hist = stats["hist"]
    assert "bin_edges" in hist
    assert "counts" in hist

    # At least 1 bin and counts sum to number of valid records
    assert len(hist["counts"]) >= 1
    assert sum(hist["counts"]) == len(df)


def test_calculate_duration_stats_handles_empty_input_gracefully():
    """
    Empty input or no valid durations should not raise an error.
    """
    df = pd.DataFrame({"Trip Duration": []})

    stats = calculate_duration_stats(df, column="Trip Duration")

    # Keys exist
    for key in ["mean", "median", "min", "max"]:
        assert key in stats

    # Values are None when there's no data
    assert stats["mean"] is None
    assert stats["median"] is None
    assert stats["min"] is None
    assert stats["max"] is None

    # Histogram structure exists but with zero-length arrays/lists
    hist = stats["hist"]
    assert "bin_edges" in hist
    assert "counts" in hist
    assert len(hist["counts"]) == 0
    assert len(hist["bin_edges"]) == 0
