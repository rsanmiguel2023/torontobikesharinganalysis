import pandas as pd


def _to_list(value):
    """
    Small helper to turn different kinds of input into a list.

    Examples:
    - None          -> None
    - [1, 2, 3]     -> [1, 2, 3]
    - "Monday"      -> ["Monday"]
    - 5             -> [5]

    This makes it easier to accept either a single value or a list of values.
    """
    if value is None:
        return None

    # If it's already a list/tuple/set, just turn it into a list
    if isinstance(value, (list, tuple, set)):
        return list(value)

    # Otherwise wrap a single value in a list
    return [value]


# ------------------------------
# DATE RANGE FILTER
# ------------------------------
def filter_by_date_range(df, start_date=None, end_date=None, time_column="Start Time"):
    """
    Keep only rows where the time_column is between start_date and end_date (inclusive).

    - df:           DataFrame with a datetime column (usually 'Start Time')
    - start_date:   Earliest date to keep (string or Timestamp) - can be None
    - end_date:     Latest date to keep (string or Timestamp) - can be None
    - time_column:  Name of the datetime column in df
    """
    # If no dates are provided, just return a copy of the original data
    if start_date is None and end_date is None:
        return df.copy()

    # If the time column does not exist, don't crash, just return a copy
    if time_column not in df.columns:
        return df.copy()

    result = df.copy()
    result[time_column] = pd.to_datetime(result[time_column], errors="coerce")

    if start_date is not None:
        start_ts = pd.to_datetime(start_date)
        result = result[result[time_column] >= start_ts]

    if end_date is not None:
        end_ts = pd.to_datetime(end_date)
        result = result[result[time_column] <= end_ts]

    return result


# ------------------------------
# HOUR FILTER
# ------------------------------
def filter_by_hour(df, hours=None, hour_column="Hour"):
    """
    Keep only rows where the Hour column is in the given list of hours.

    - hours can be a single number (e.g., 7) or a list (e.g., [7, 8, 9]).
    - If hours is None or empty, return the original data.
    """
    hour_list = _to_list(hours)
    if not hour_list:
        return df.copy()

    if hour_column not in df.columns:
        return df.copy()

    return df[df[hour_column].isin(hour_list)].copy()


# ------------------------------
# DAY OF WEEK FILTER
# ------------------------------
def filter_by_day_of_week(df, days=None, day_column="Day"):
    """
    Keep only rows where the Day column matches the given day names.

    - days can be "Monday" or ["Monday", "Tuesday"], etc.
    - Matching is case-insensitive ("monday" == "Monday").
    """
    day_list = _to_list(days)
    if not day_list:
        return df.copy()

    if day_column not in df.columns:
        return df.copy()

    # Normalize both the filter values and the column values to lowercase
    day_list_norm = [str(d).strip().lower() for d in day_list]

    result = df.copy()
    return result[result[day_column].str.strip().str.lower().isin(day_list_norm)]


# ------------------------------
# MONTH FILTER
# ------------------------------
def filter_by_month(df, months=None, month_column="Month"):
    """
    Keep only rows where the Month column matches the given month values.

    - months can be 6 or [6, 7, 8], or names depending on how Month is stored.
    """
    month_list = _to_list(months)
    if not month_list:
        return df.copy()

    if month_column not in df.columns:
        return df.copy()

    return df[df[month_column].isin(month_list)].copy()


# ------------------------------
# START STATION FILTER
# ------------------------------
def filter_by_start_station(df, stations=None, column="Start Station Name"):
    """
    Keep only trips that start from the given station(s).

    - stations can be "Union Station" or ["Union Station", "City Hall"]
    """
    station_list = _to_list(stations)
    if not station_list:
        return df.copy()

    if column not in df.columns:
        return df.copy()

    return df[df[column].isin(station_list)].copy()


# ------------------------------
# END STATION FILTER
# ------------------------------
def filter_by_end_station(df, stations=None, column="End Station Name"):
    """
    Keep only trips that end at the given station(s).
    """
    station_list = _to_list(stations)
    if not station_list:
        return df.copy()

    if column not in df.columns:
        return df.copy()

    return df[df[column].isin(station_list)].copy()


# ------------------------------
# STATION PAIR FILTER
# ------------------------------
def filter_by_station_pair(
    df,
    start_station=None,
    end_station=None,
    start_col="Start Station Name",
    end_col="End Station Name",
):
    """
    Keep only trips that match a specific origin–destination pair.

    - If both start_station and end_station are None, return the original data.
    """
    if start_station is None and end_station is None:
        return df.copy()

    if start_col not in df.columns or end_col not in df.columns:
        return df.copy()

    result = df.copy()

    if start_station is not None:
        result = result[result[start_col] == start_station]

    if end_station is not None:
        result = result[result[end_col] == end_station]

    return result


# ------------------------------
# USER TYPE FILTER
# ------------------------------
def filter_by_user_type(df, user_types=None, column="User Type"):
    """
    Keep only rows where the User Type column matches the given types.

    - user_types can be "Subscriber" or ["Subscriber", "Casual"].
    - Matching is case-insensitive.
    """
    type_list = _to_list(user_types)
    if not type_list:
        return df.copy()

    if column not in df.columns:
        return df.copy()

    type_list_norm = [str(t).strip().lower() for t in type_list]

    result = df.copy()
    return result[result[column].str.strip().str.lower().isin(type_list_norm)]


# ------------------------------
# DURATION RANGE FILTER
# ------------------------------
def filter_by_duration_range(df, min_duration=None, max_duration=None, column="Trip Duration"):
    """
    Keep only trips where Trip Duration is between min_duration and max_duration.

    - Negative values are removed automatically.
    - If both min_duration and max_duration are None, return original data.
    """
    if min_duration is None and max_duration is None:
        return df.copy()

    if column not in df.columns:
        return df.copy()

    result = df.copy()
    result[column] = pd.to_numeric(result[column], errors="coerce")
    result = result[result[column] >= 0]

    if min_duration is not None:
        result = result[result[column] >= min_duration]

    if max_duration is not None:
        result = result[result[column] <= max_duration]

    return result


# ------------------------------
# BIKE ID FILTER
# ------------------------------
def filter_by_bike_id(df, bike_ids=None, column="Bike Id"):
    """
    Keep only rows for the given Bike Id or list of Bike Ids.

    - bike_ids can be 101 or [101, 102, 103].
    """
    id_list = _to_list(bike_ids)
    if not id_list:
        return df.copy()

    if column not in df.columns:
        return df.copy()

    return df[df[column].isin(id_list)].copy()
