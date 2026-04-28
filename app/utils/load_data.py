from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def generate_sample_bike_data(num_rows: int = 2500) -> pd.DataFrame:
    """Generate realistic sample Bike Share Toronto trip data for the dashboard."""
    rng = np.random.default_rng(42)
    stations = [
        "Union Station", "Queen St W / Spadina Ave", "King St W / Bay St",
        "Yonge St / Bloor St", "College St / University Ave", "Dundas St W / Bathurst St",
        "Harbourfront Centre", "Nathan Phillips Square", "Front St / Blue Jays Way",
        "Liberty Village", "Kensington Market", "St Lawrence Market"
    ]
    end = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    start = end - timedelta(days=60)
    seconds = rng.integers(0, int((end - start).total_seconds()), size=num_rows)
    start_times = pd.to_datetime(start) + pd.to_timedelta(seconds, unit="s")
    duration = rng.gamma(shape=2.2, scale=520, size=num_rows).astype(int)
    duration = np.clip(duration, 180, 7200)
    df = pd.DataFrame({
        "Trip Id": np.arange(1, num_rows + 1),
        "Trip Duration ": duration,
        "Start Time": start_times,
        "Start Station Name": rng.choice(stations, size=num_rows, p=[.16,.12,.11,.10,.09,.08,.08,.07,.06,.05,.04,.04]),
        "End Station Name": rng.choice(stations, size=num_rows),
        "User Type": rng.choice(["Annual Member", "Casual Member"], size=num_rows, p=[.72,.28]),
        "Model": rng.choice(["ICONIC", "BOOST", "ELECTRIC"], size=num_rows, p=[.55,.30,.15]),
    })
    df["End Time"] = df["Start Time"] + pd.to_timedelta(df["Trip Duration "], unit="s")
    return df


def load_dashboard_data() -> pd.DataFrame:
    """Load project data if available; otherwise generate sample dashboard data."""
    candidates = [
        ROOT / "data" / "processed" / "bike_trips_processed.csv",
        ROOT / "data" / "raw" / "bike_trips.csv",
    ]
    for path in candidates:
        if path.exists():
            df = pd.read_csv(path)
            for col in ["Start Time", "End Time"]:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
            return df
    return generate_sample_bike_data()


def normalize_duration_column(df: pd.DataFrame) -> str:
    for col in ["Trip Duration ", "Trip Duration", "duration", "trip_duration"]:
        if col in df.columns:
            return col
    raise KeyError("No trip duration column found")
