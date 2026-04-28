# Usage Summary Module

**Location:** `src/data_processing/usage_summary.py`

## Overview

Production-ready module for analyzing and visualizing top bike sharing stations by trip count. Developed using Test-Driven Development (TDD) methodology.

## Features

### 1. Quick Analysis Function
- `get_top_stations(data, n=10)` - Fast function for basic station analysis
- Returns tidy DataFrame with station names and trip counts
- Automatic tie-breaking (alphabetical by station name)

### 2. Full-Featured Analyzer Class
- `StationUsageAnalyzer` - Comprehensive analysis and visualization
- Input validation
- Multiple analysis methods
- Professional chart generation

## Installation

Required packages:
```bash
pip install pandas matplotlib
```

## Usage

### Basic Function

```python
from data_processing.usage_summary import get_top_stations
import pandas as pd

# Your bike sharing data
data = pd.DataFrame({
    'Start Station Name': ['Station A', 'Station B', 'Station A', ...],
    'Trip Id': [1, 2, 3, ...]
})

# Get top 10 stations
top_10 = get_top_stations(data, n=10)
print(top_10)
```

### Analyzer Class

```python
from data_processing.usage_summary import StationUsageAnalyzer

# Create analyzer
analyzer = StationUsageAnalyzer(data)

# Get top stations
top_stations = analyzer.get_top_stations(n=10)

# Get statistics
stats = analyzer.get_station_statistics()
print(f"Total stations: {stats['total_stations']}")
print(f"Average trips per station: {stats['avg_trips_per_station']:.2f}")

# Create visualization
analyzer.create_top_stations_chart(
    n=10, 
    output_path='top_stations.png'
)
```

## API Reference

### `get_top_stations(data, n=10)`

Quick function to get top N stations.

**Parameters:**
- `data` (pd.DataFrame): DataFrame with 'Start Station Name' column
- `n` (int): Number of top stations to return

**Returns:**
- pd.DataFrame: Tidy DataFrame with 'Station Name' and 'Trip Count'

### `StationUsageAnalyzer`

#### `__init__(data)`

Initialize analyzer with bike sharing data.

**Parameters:**
- `data` (pd.DataFrame): Must contain 'Start Station Name' column

**Raises:**
- ValueError: If required columns are missing

#### `get_top_stations(n=10)`

Get top N stations by trip count.

**Parameters:**
- `n` (int): Number of stations to return

**Returns:**
- pd.DataFrame: Sorted by trip count (descending), ties broken alphabetically

#### `create_top_stations_chart(n=10, figsize=(12, 6), output_path=None)`

Create bar chart visualization.

**Parameters:**
- `n` (int): Number of stations to display
- `figsize` (tuple): Figure size (width, height) in inches
- `output_path` (str, optional): Path to save chart

**Returns:**
- matplotlib.figure.Figure: Figure object (if output_path is None)

#### `get_station_summary()`

Get all stations with trip counts.

**Returns:**
- pd.DataFrame: All stations sorted by trip count

#### `get_station_statistics()`

Get statistical summary.

**Returns:**
- dict: Contains total_stations, total_trips, avg_trips_per_station, median_trips_per_station, max_trips, min_trips

## Examples

See `examples/usage_summary_examples.py` for complete working examples including:
- Basic function usage
- Analyzer class usage
- Visualization creation
- Tie-breaking demonstration

Run examples:
```bash
python examples/usage_summary_examples.py
```

## Tests

Comprehensive test suite following TDD methodology.

**Run tests:**
```bash
pytest tests/US04-usage_summary.py -v
```

**Test coverage:**
- Basic aggregation functionality
- Tie-breaking logic
- Input validation
- Visualization generation
- File saving

## TDD Cycle

This module was developed following strict TDD methodology:

1. **RED:** Two failing tests
   - `test_get_top_stations_basic()` - Basic aggregation
   - `test_get_top_stations_handles_ties()` - Tie-breaking

2. **GREEN:** Two minimal implementations
   - Basic aggregation function
   - Tie-breaking enhancement

3. **REFACTOR:** One major cleanup
   - `StationUsageAnalyzer` class with visualization

See `US04-TDD-CYCLE-SUMMARY.md` for detailed TDD cycle documentation.

## User Story

**As a planner, I want top stations so that I can identify high traffic areas.**

### Tasks Completed
✅ Task 1: Failing test for top N stations  
✅ Task 2: Aggregation function implementation  
✅ Task 3: Bar chart visualization  
✅ Task 4: Unit tests for ties  

All acceptance criteria met.

## Data Requirements

Input DataFrame must contain:
- `Start Station Name` (str): Name of the starting station

Additional columns are ignored.

## Tie-Breaking Rules

When stations have identical trip counts:
- Stations are sorted alphabetically by name
- Ensures consistent, predictable results
- No random ordering

## Output Formats

### DataFrame Output
```
  Station Name  Trip Count
0 Union Station          45
1      Queen St          32
2       King St          28
```

### Chart Output
- Professional bar chart
- Clear axis labels
- Value labels on bars
- Grid for readability
- High resolution (300 DPI)

## License

Part of Toronto Bike Sharing Analytics Tool project.
