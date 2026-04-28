# **US10 – Reusable Data Filters Module (`utils.filters`)**

## **1. Overview**

This module contains **simple, reusable filtering functions** used across the Toronto Bike-Sharing Analytics Tool.
The goal is to avoid repeating the same filtering code in multiple user stories and keep the analytics scripts clean and consistent.

These filters allow any team member to easily apply:

* Date range filtering
* Hour / weekday / month filtering
* User type filtering
* Start/end station filtering
* Trip duration filtering
* Bike ID filtering
* Station-to-station pair filtering

The filters benefit several user stories:

| User Story                     | How This Module Helps            |
| ------------------------------ | -------------------------------- |
| **US06 – Peak Hours**          | Filter by hour, weekday, month   |
| **US07 – User Type Breakdown** | Filter by subscriber / casual    |
| **US08 – Dashboard Skeleton**  | Used behind Streamlit widgets    |
| **US09 – Interactive Charts**  | Dynamic filtering for charts     |
| **US10 – Reusable Filters**    | Centralizing all filtering logic |

---

## **2. How to Import the Filters**

Any script inside the project may import the filters like this:

```python
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
```

If your script is outside `src/`, add this (beginners will copy-paste):

```python
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
```

---

## **3. Example: Complete Workflow with Filters**

This example shows how the filters plug directly into the existing loading + cleaning pipeline (**US01 + US02 + US10**):

```python
from data_processing.loader import load_data
from data_processing.cleaning import clean_data
from utils.filters import (
    filter_by_date_range,
    filter_by_user_type,
    filter_by_hour,
)

# Step 1: Load and clean
df_raw = load_data("data/bike_trips.csv")
df = clean_data(df_raw)

# Step 2: Apply filters
df = filter_by_date_range(df, start_date="2025-01-01", end_date="2025-01-31")
df = filter_by_user_type(df, user_types=["Subscriber"])
df = filter_by_hour(df, hours=[7, 8, 9])  # morning peak

# Step 3: Use the filtered df for charts/analytics
print(df.head())
```

---

## **4. Filter Function Reference (Beginner-Friendly)**

Each filter returns a new filtered DataFrame.
If you pass nothing (e.g., `None`), the filter simply returns the original DataFrame.

---

### **4.1 `filter_by_date_range(df, start_date=None, end_date=None, time_column="Start Time")`**

**What it does:**
Keeps only rows between the given dates.

**Examples:**

```python
df = filter_by_date_range(df, "2025-01-01", "2025-01-31")
```

---

### **4.2 `filter_by_hour(df, hours=None, hour_column="Hour")`**

**What it does:**
Filters by hour (0–23). Accepts one value or a list.

**Example:**

```python
df = filter_by_hour(df, hours=[7, 8, 9])   # Morning peak
```

---

### **4.3 `filter_by_day_of_week(df, days=None, day_column="Day")`**

**What it does:**
Filters by weekday name.

**Example:**

```python
df = filter_by_day_of_week(df, ["Saturday", "Sunday"])
```

---

### **4.4 `filter_by_month(df, months=None, month_column="Month")`**

**Example:**

```python
df = filter_by_month(df, [6, 7, 8])  # Summer months
```

---

### **4.5 `filter_by_start_station(df, stations=None, column="Start Station Name")`**

**Example:**

```python
df = filter_by_start_station(df, ["Union Station", "Bay St"])
```

---

### **4.6 `filter_by_end_station(df, stations=None, column="End Station Name")`**

```python
df = filter_by_end_station(df, ["Queen St W"])
```

---

### **4.7 `filter_by_station_pair(df, start_station=None, end_station=None, ...)`**

**What it does:**
Filters for a specific origin → destination pair.

```python
df = filter_by_station_pair(df, "Union Station", "Harbourfront")
```

---

### **4.8 `filter_by_user_type(df, user_types=None, column="User Type")`**

**Example:**

```python
df = filter_by_user_type(df, ["Subscriber"])
```

---

### **4.9 `filter_by_duration_range(df, min_duration=None, max_duration=None, column="Trip Duration")`**

**Example:**

```python
df = filter_by_duration_range(df, min_duration=60, max_duration=1200)
```

---

### **4.10 `filter_by_bike_id(df, bike_ids=None, column="Bike Id")`**

**Example:**

```python
df = filter_by_bike_id(df, [12345, 99999])
```

---

## **5. Manual Testing (Task #61)**

A simple script in:

```
examples/test_filters_manual.py
```

was used to verify:

* Each filter runs without errors
* Output rows match expected logic
* Edge cases (None, empty lists, invalid values) are handled
* No filter ever mutates the original DataFrame

A screenshot of the test output was attached to Task #61.

---

## **6. How These Filters Support Other User Stories**

| User Story                    | How Filters Will Be Used              |
| ----------------------------- | ------------------------------------- |
| **US06 – Peak hours**         | Hour filter, day filter               |
| **US07 – User types**         | `filter_by_user_type`                 |
| **US08 – Dashboard skeleton** | All filters behind Streamlit widgets  |
| **US09 – Interactive charts** | Filters applied dynamically to charts |
| **Future stations analytics** | Start/End station filters             |
| **Future advanced charts**    | Month, weekday, bike ID filters       |

---

