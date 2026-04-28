import pandas as pd


def user_type_breakdown(df: pd.DataFrame) -> dict:
    """
    Analyze user types in the given DataFrame.
    Input:
        df - a pandas DataFrame with at least:
            - "User Type" column
            - "Trip Duration" column

    Output:
        A dictionary with:
        {
            "counts": {
                "Subscriber": X,
                "Customer": Y,
                "Unknown": Z
            },
            "avg_duration": {
                "Subscriber": A,
                "Customer": B,
                "Unknown": C
            }
        }
    """

    # If the DataFrame is empty, just return zeros.
    if df.empty:
        return {
            "counts": {
                "Subscriber": 0,
                "Customer": 0,
                "Unknown": 0,
            },
            "avg_duration": {
                "Subscriber": 0,
                "Customer": 0,
                "Unknown": 0,
            },
        }

    # Make a copy so we do not change the original data.
    temp = df.copy()

    # 🔁 Change these names if your real columns are different.
    user_col = "User Type"
    duration_col = "Trip Duration"

    # Basic safety checks: make sure columns exist.
    if user_col not in temp.columns:
        raise KeyError(f"Expected column '{user_col}' in DataFrame")
    if duration_col not in temp.columns:
        raise KeyError(f"Expected column '{duration_col}' in DataFrame")

    # Step 1: Fill missing values in User Type with "Unknown".
    temp[user_col] = temp[user_col].fillna("Unknown")

    # Step 2: Normalize user type text so we only have:
    #   - "Subscriber"
    #   - "Customer"
    #   - "Unknown"
    normalized_values = []

    for value in temp[user_col]:
        # Convert to lowercase string for easier comparison.
        text = str(value).strip().lower()

        # If it contains "sub", treat as Subscriber.
        if "sub" in text:
            normalized_values.append("Subscriber")
        # If it contains "cust" or "casual", treat as Customer.
        elif "cust" in text or "casual" in text:
            normalized_values.append("Customer")
        # If it literally says "unknown", keep as Unknown.
        elif text == "unknown":
            normalized_values.append("Unknown")
        # Anything else, also treat as Unknown.
        else:
            normalized_values.append("Unknown")

    # Replace the original user type column with our normalized labels.
    temp[user_col] = normalized_values

    # Step 3: Group by user type and calculate:
    #   - count of trips
    #   - average trip duration
    grouped = temp.groupby(user_col)[duration_col]

    counts_dict = grouped.size().to_dict()
    avg_dict = grouped.mean().to_dict()

    # Step 4: Make sure all three keys always exist.
    # If a type is missing, set its value to 0.
    expected_keys = ["Subscriber", "Customer", "Unknown"]

    for key in expected_keys:
        if key not in counts_dict:
            counts_dict[key] = 0
        if key not in avg_dict:
            avg_dict[key] = 0

    # Step 5: Build the final result dictionary.
    result = {
        "counts": counts_dict,
        "avg_duration": avg_dict,
    }

    return result
