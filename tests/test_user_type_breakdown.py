import os
import sys
import pandas as pd
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from analytics.user_type_breakdown import user_type_breakdown  # will fail at first


def test_user_type_breakdown_counts_and_averages():
    # Arrange: small sample data
    df = pd.DataFrame(
        {
            "User Type": ["Subscriber", "Customer", "Subscriber", None],
            "Trip Duration": [10, 20, 30, 40],
        }
    )

    # Act
    result = user_type_breakdown(df)

    # Assert: basic structure
    assert "counts" in result
    assert "avg_duration" in result

    counts = result["counts"]
    avg = result["avg_duration"]

    # We expect:
    # Subscriber: 2 trips, durations 10 and 30 -> avg 20
    # Customer:   1 trip, duration 20        -> avg 20
    # Unknown:    1 trip, duration 40        -> avg 40
    assert counts["Subscriber"] == 2
    assert counts["Customer"] == 1
    assert counts["Unknown"] == 1

    assert avg["Subscriber"] == 20
    assert avg["Customer"] == 20
    assert avg["Unknown"] == 40
