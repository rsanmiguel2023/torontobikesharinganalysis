import os
import sys
import pandas as pd

# --- make Python see the src/ folder ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from analytics.user_type_breakdown import user_type_breakdown
from visualization.us07_user_type_charts import plot_user_type_stacked_counts


def test_manual_us07_validation():
    """
    Manual validation test for US07.
    Not intended to assert anything automatically.
    Just loads data, runs functions, and prints results.
    """

    # 1. Load sample CSV
    csv_path = os.path.join(PROJECT_ROOT, "data", "sample_us07.csv")

    assert os.path.exists(csv_path), f"File not found: {csv_path}"

    df = pd.read_csv(csv_path)

    # 2. Run analytics
    result = user_type_breakdown(df)

    print("\n--- US07 Manual Validation Output ---")
    print("Counts:", result["counts"])
    print("Avg Duration:", result["avg_duration"])

    # 3. Generate chart
    plot_user_type_stacked_counts(result)

    print("Chart saved to output/us07_user_type_stacked.png\n")

    # 4. Always pass
    # This is NOT an automated unit test — it's a manual validation step.
    assert True
