# Toronto BikeShare Analytics Dashboard

## Overview
Interactive Streamlit dashboard for analyzing Toronto bike sharing data with real-time KPI monitoring and dynamic filtering capabilities.

## US 08: Dashboard KPIs - Implementation Summary

### ✅ Task 1: Design Streamlit Layout
**Acceptance Criteria:** The dashboard layout must include a dedicated section for KPI cards.

**Implementation:**
- Clean, professional layout with header and sections
- KPI cards section immediately after the dashboard title
- Sidebar for filters and controls
- Additional analytics sections below KPIs
- Responsive design using Streamlit columns

### ✅ Task 2: Implement KPI Cards
**Acceptance Criteria:** KPI cards must display total trips, median trip duration, and the top start station.

**Implementation:**
Three KPI cards using `st.metric()`:
1. ** Total Trips** - Total number of bike trips
2. ** Median Trip Duration** - Median duration in minutes
3. ** Top Start Station** - Most popular starting station with trip count

### ✅ Task 3: Connect to Pipeline Outputs
**Acceptance Criteria:** KPI values must update dynamically when filters are applied.

**Implementation:**
Dynamic filtering system with real-time KPI updates:
- **Date Range Filter** - Filter by start/end dates
- **Station Filter** - Multi-select for specific stations
- **User Type Filter** - Filter by Annual/Casual members
- KPIs automatically recalculate when filters change

### ✅ Task 4: Test with Sample Dataset
**Acceptance Criteria:** KPI cards must display correct values when tested with a sample dataset.

**Implementation:**
- Built-in sample data generator for testing
- Comprehensive test suite (12 tests, all passing)
- Validated with multiple dataset sizes (100-5000 trips)
- All KPI calculations verified for accuracy

## Features

### KPI Cards
- **Total Trips**: Count of all bike trips in selected period
- **Median Trip Duration**: Median duration of trips (in minutes)
- **Top Start Station**: Most popular starting station with trip count

### Dynamic Filters
- **Date Range**: Select custom date ranges
- **Stations**: Multi-select specific stations
- **User Types**: Filter by member type
- Real-time KPI updates as filters change

### Additional Analytics
- Top 10 start stations table
- Trip duration statistics (mean, median, min, max)
- Data preview with first 100 rows

### Data Sources
1. **Sample Data**: Generated test data (100-5000 trips)
2. **Upload CSV**: Upload your own bike sharing data

## Installation

### Requirements
```bash
pip install streamlit pandas numpy matplotlib
```

### Project Structure
```
Toronto-Bike-Sharing-Analytics-Tool/
├── dashboard.py                    # Main Streamlit dashboard
├── src/
│   └── data_processing/
│       ├── loader.py              # Data loading utilities
│       ├── cleaning.py            # Data cleaning pipeline
│       ├── tripduration_stats.py  # Duration statistics
│       └── usage_summary.py  # Station usage analysis
└── tests/
    └── test_dashboard_kpi.py      # KPI tests (12 tests)
```

## Usage

### Launch Dashboard
```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Using Sample Data
1. Select "Sample Data" in the sidebar
2. Adjust the number of sample trips (100-5000)
3. View KPIs and apply filters

### Uploading Your Own Data
1. Select "Upload CSV" in the sidebar
2. Click "Choose a CSV file" and select your data
3. Data must include these columns:
   - Trip Id
   - Trip Duration (or "Trip Duration ")
   - Start Station Name
   - Start Time
   - End Time
   - Other bike sharing columns

### Applying Filters
1. Use the sidebar controls:
   - **Date Range**: Select start and end dates
   - **Stations**: Choose one or more stations
   - **User Type**: Select Annual/Casual members
2. KPIs update automatically
3. Filter summary shows filtered vs total trips

## Testing

### Run All Tests
```bash
pytest tests/test_dashboard_kpi.py -v
```

### Test Coverage
- ✅ Total trips calculation
- ✅ Median duration calculation
- ✅ Top station identification
- ✅ Empty data handling
- ✅ Dynamic filter updates
- ✅ User type filtering
- ✅ Date range filtering
- ✅ Sample data generation
- ✅ Multiple dataset sizes
- ✅ Full pipeline integration
- ✅ Data type validation

All 12 tests passing ✅

## KPI Calculation Logic

### Total Trips
```python
total_trips = len(filtered_data)
```

### Median Trip Duration
```python
median_duration = filtered_data['Trip Duration'].median() / 60  # Convert seconds to minutes
```

### Top Start Station
```python
top_stations = get_top_stations(filtered_data, n=1)
top_station = top_stations.iloc[0]['Station Name']
top_station_trips = top_stations.iloc[0]['Trip Count']
```

## Sample Data Format

The dashboard expects CSV data with these columns:
```
Trip Id, Trip Duration, Start Station Id, Start Time, Start Station Name,
End Station Id, End Time, End Station Name, Bike Id, User Type, Model
```

## API Functions

### `generate_sample_data(num_rows)`
Generate sample bike sharing data for testing.

**Parameters:**
- `num_rows` (int): Number of sample trips

**Returns:**
- pd.DataFrame: Sample data

### `calculate_kpis(data)`
Calculate KPI values from bike sharing data.

**Parameters:**
- `data` (pd.DataFrame): Cleaned bike sharing data

**Returns:**
- dict: KPI values (total_trips, median_duration, top_station, top_station_trips)

### `display_kpi_cards(kpis)`
Display KPI cards in the dashboard.

**Parameters:**
- `kpis` (dict): KPI values dictionary

### `apply_filters(data)`
Apply sidebar filters to the data.

**Parameters:**
- `data` (pd.DataFrame): Input data

**Returns:**
- pd.DataFrame: Filtered data

## Browser Compatibility
- Chrome/Edge (Recommended)
- Firefox
- Safari

## Performance
- Handles up to 5000 trips smoothly in sample mode
- Real-time filter updates (< 1 second)
- Efficient data processing pipeline

## Troubleshooting

### Dashboard won't start
```bash
# Ensure Streamlit is installed
pip install streamlit

# Run from project root
cd Toronto-Bike-Sharing-Analytics-Tool
streamlit run dashboard.py
```

### Import errors
Ensure you're running from the project root directory where `dashboard.py` is located.

### No data displaying
- Check that filters aren't too restrictive
- Verify uploaded CSV has required columns
- Try using sample data first

## Future Enhancements
- Additional KPIs (average speed, popular routes)
- Interactive maps for station locations
- Time series charts for trip trends
- Export filtered data functionality
- Custom date aggregations (daily, weekly, monthly)

## License
Part of Toronto Bike Sharing Analytics Tool project.

## Contact
For issues or questions, refer to the project README.
