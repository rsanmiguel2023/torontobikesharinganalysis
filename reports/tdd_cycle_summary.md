# US04 - Usage Summary: Test-Driven Development Cycle

## Overview
This document explains the TDD cycle implemented in `tests/US04-usage_summary.py` for the user story: **"As a planner, I want top stations so that I can identify high traffic areas."**

## TDD Cycle Structure

### 🔴 RED PHASE: Two Failing Tests

#### Test 1: `test_get_top_stations_basic()` (Task 1)
- **Purpose**: Test for top N stations aggregation
- **Acceptance Criteria**: Must fail if aggregation doesn't correctly identify top stations by trip count
- **What it tests**:
  - Function returns a DataFrame
  - Correct number of stations (top N)
  - Proper column names ('Station Name', 'Trip Count')
  - Stations sorted in descending order by trip count
  - Accurate trip counts

#### Test 2: `test_get_top_stations_handles_ties()` (Task 4)
- **Purpose**: Test for handling ties in trip counts
- **Acceptance Criteria**: Must confirm ties are resolved consistently (alphabetically)
- **What it tests**:
  - When multiple stations have same trip count
  - Stations are ordered alphabetically to break ties
  - All tied stations have correct counts

### 🟢 GREEN PHASE: Two Minimal Implementations

#### Implementation 1: Basic Aggregation (Task 2)
```python
def get_top_stations(data, n=10):
    # GREEN 1: Basic aggregation - count trips per station
    station_counts = data.groupby('Start Station Name').size().reset_index(name='Trip Count')
    station_counts = station_counts.rename(columns={'Start Station Name': 'Station Name'})
    ...
```
- **Acceptance Criteria**: Returns tidy DataFrame with stations and trip counts
- **Features**:
  - Groups by station name
  - Counts trips per station
  - Returns DataFrame with clear column names

#### Implementation 2: Tie-Breaking Logic (Task 2 & 4)
```python
    # GREEN 2: Sort by trip count (descending) and station name (ascending) for tie-breaking
    station_counts = station_counts.sort_values(
        by=['Trip Count', 'Station Name'],
        ascending=[False, True]
    )
```
- **Acceptance Criteria**: Ties resolved consistently (alphabetically)
- **Features**:
  - Primary sort: Trip count (descending)
  - Secondary sort: Station name (ascending/alphabetical)
  - Consistent, predictable results

### 🔵 REFACTOR PHASE: Cleanup and Enhancement (Task 3)

#### Refactoring: `StationUsageAnalyzer` Class
This is a **significant refactoring** that improves structure and adds visualization:

**Improvements:**
1. **Better Organization**: Class-based structure
2. **Validation**: Input data validation
3. **Separation of Concerns**: Analysis separate from visualization
4. **Documentation**: Comprehensive docstrings
5. **Extensibility**: Easy to add new methods

**New Features:**
- `get_top_stations()`: Same functionality, better structure
- `create_top_stations_chart()`: Bar chart visualization (Task 3)
  - **Acceptance Criteria**: Displays top 10 stations with clear labels and counts
  - Customizable figure size
  - Value labels on bars
  - Professional styling
  - Save to file or return figure

## Test Results

All 7 tests pass:
```
✓ test_get_top_stations_basic
✓ test_get_top_stations_handles_ties
✓ test_station_usage_analyzer_initialization
✓ test_station_usage_analyzer_validates_data
✓ test_analyzer_get_top_stations
✓ test_create_top_stations_chart
✓ test_chart_saves_to_file
```

## Usage Examples

### Using the Basic Function (Green Implementation)
```python
import pandas as pd

# Load data
data = pd.DataFrame({
    'Start Station Name': ['Union Station', 'Queen St', 'Union Station', ...],
    'Trip Id': [1, 2, 3, ...]
})

# Get top 5 stations
top_5 = get_top_stations(data, n=5)
print(top_5)
```

### Using the Refactored Class (Refactor Implementation)
```python
# Create analyzer
analyzer = StationUsageAnalyzer(data)

# Get top stations
top_10 = analyzer.get_top_stations(n=10)

# Create visualization
analyzer.create_top_stations_chart(n=10, output_path='top_stations.png')
```

## Key TDD Principles Demonstrated

1. **Red**: Write tests first - they fail because functionality doesn't exist
2. **Green**: Write minimal code to make tests pass
3. **Refactor**: Improve code structure while keeping tests green

## Tasks Completion Checklist

- ✅ Task 1: Failing test for top N stations (RED)
- ✅ Task 2: Aggregation function implementation (GREEN)
- ✅ Task 3: Bar chart visualization (REFACTOR)
- ✅ Task 4: Unit tests for ties (RED + GREEN)

## Running the Code

### Run Demonstration
```bash
python tests/US04-usage_summary.py
```

### Run Tests
```bash
pytest tests/US04-usage_summary.py -v
```

### Run Specific Test
```bash
pytest tests/US04-usage_summary.py::test_get_top_stations_basic -v
```

## Notes

- The file demonstrates a complete TDD cycle with clear separation between phases
- Tests are comprehensive and cover edge cases (ties, validation)
- Code is production-ready with proper documentation and error handling
- Visualization feature meets all acceptance criteria for Task 3
