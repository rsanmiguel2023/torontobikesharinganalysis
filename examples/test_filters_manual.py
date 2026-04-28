import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from utils.filters import (
    filter_by_date_range,
    filter_by_hour,
    filter_by_day_of_week,
    filter_by_month,
    filter_by_start_station,
    filter_by_end_station,
    filter_by_station_pair,
    filter_by_user_type,
    filter_by_duration_range,
    filter_by_bike_id,
)



# ------------------------------
# Create a tiny sample DataFrame
# ------------------------------
data = {
    "Start Time": ["2023-06-01 08:30", "2023-06-02 14:00", "2023-07-01 09:15"],
    "Hour": [8, 14, 9],
    "Day": ["Thursday", "Friday", "Saturday"],
    "Month": [6, 6, 7],
    "Start Station Name": ["Union Station", "City Hall", "Union Station"],
    "End Station Name": ["City Hall", "Union Station", "Harbourfront"],
    "User Type": ["Subscriber", "Casual", "Subscriber"],
    "Trip Duration": [12, 30, 8],
    "Bike Id": [101, 102, 101],
}

df = pd.DataFrame(data)

print("---------- ORIGINAL DATA ----------")
print(df)
print("\n")


# ------------------------------
# Test each filter
# ------------------------------

print("Date Range Filter (June only):")
print(filter_by_date_range(df, "2023-06-01", "2023-06-30"))
print("\n")

print("Hour Filter (8 AM only):")
print(filter_by_hour(df, 8))
print("\n")

print("Day Filter (Saturday only):")
print(filter_by_day_of_week(df, "Saturday"))
print("\n")

print("Month Filter (July only):")
print(filter_by_month(df, 7))
print("\n")

print("Start Station Filter (Union Station):")
print(filter_by_start_station(df, "Union Station"))
print("\n")

print("End Station Filter (City Hall):")
print(filter_by_end_station(df, "City Hall"))
print("\n")

print("Station Pair Filter (Union -> City Hall):")
print(filter_by_station_pair(df, "Union Station", "City Hall"))
print("\n")

print("User Type Filter (Subscriber):")
print(filter_by_user_type(df, "Subscriber"))
print("\n")

print("Duration Filter (10–20 minutes):")
print(filter_by_duration_range(df, 10, 20))
print("\n")

print("Bike ID Filter (101):")
print(filter_by_bike_id(df, 101))
print("\n")
