"""
Test suite for Dashboard KPI functionality (US08)

This file tests the KPI calculation and display logic for the Streamlit dashboard.

Tasks tested:
- Task 2: KPI cards implementation (total trips, median duration, top station)
- Task 3: Dynamic filtering and KPI updates
- Task 4: Correct values with sample dataset
"""

import os
import sys
import pandas as pd
import pytest
from datetime import datetime, timedelta

# Setup project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
DASHBOARD_PATH = PROJECT_ROOT

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)
if DASHBOARD_PATH not in sys.path:
    sys.path.append(DASHBOARD_PATH)

# Import dashboard functions
from data_processing.framework_dashboard import generate_sample_data
from analytics.kpi_metrics import calculate_kpis
from data_processing.cleaning import clean_data


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_data():
    """Fixture providing sample bike sharing data."""
    return pd.DataFrame({
        'Trip Id': [1, 2, 3, 4, 5],
        'Trip Duration ': [600, 900, 1200, 300, 1500],  # in seconds
        'Start Station Id': [100, 101, 100, 102, 100],
        'Start Time': [
            '2024-01-01 08:00:00',
            '2024-01-01 09:00:00',
            '2024-01-01 10:00:00',
            '2024-01-01 11:00:00',
            '2024-01-01 12:00:00'
        ],
        'Start Station Name': ['Station A', 'Station B', 'Station A', 'Station C', 'Station A'],
        'End Station Id': [101, 102, 101, 100, 102],
        'End Time': [
            '2024-01-01 08:10:00',
            '2024-01-01 09:15:00',
            '2024-01-01 10:20:00',
            '2024-01-01 11:05:00',
            '2024-01-01 12:25:00'
        ],
        'End Station Name': ['Station B', 'Station C', 'Station B', 'Station A', 'Station C'],
        'Bike Id': [1000, 1001, 1002, 1003, 1004],
        'User Type': ['Annual Member', 'Casual Member', 'Annual Member', 'Casual Member', 'Annual Member'],
        'Model': ['ICONIC', 'BOOST', 'ICONIC', 'ELECTRIC', 'ICONIC']
    })


@pytest.fixture
def cleaned_sample_data(sample_data):
    """Fixture providing cleaned sample data."""
    return clean_data(sample_data)


# ============================================================================
# Task 2: Test KPI Calculation
# ============================================================================

def test_calculate_kpis_total_trips(cleaned_sample_data):
    """
    Task 2: Test that total trips KPI is calculated correctly.
    
    Acceptance Criteria: KPI cards must display total trips.
    """
    kpis = calculate_kpis(cleaned_sample_data)
    
    assert 'total_trips' in kpis, "KPI dictionary must contain 'total_trips'"
    assert kpis['total_trips'] == 5, "Total trips should equal number of rows"
    assert isinstance(kpis['total_trips'], int), "Total trips must be an integer"


def test_calculate_kpis_median_duration(cleaned_sample_data):
    """
    Task 2: Test that median trip duration KPI is calculated correctly.
    
    Acceptance Criteria: KPI cards must display median trip duration.
    """
    kpis = calculate_kpis(cleaned_sample_data)
    
    assert 'median_duration' in kpis, "KPI dictionary must contain 'median_duration'"
    
    # Expected median: [300, 600, 900, 1200, 1500] -> 900 seconds = 15 minutes
    expected_median = 15.0  # minutes
    assert kpis['median_duration'] == expected_median, \
        f"Median duration should be {expected_median} minutes"
    assert isinstance(kpis['median_duration'], (int, float)), \
        "Median duration must be numeric"


def test_calculate_kpis_top_station(cleaned_sample_data):
    """
    Task 2: Test that top start station KPI is calculated correctly.
    
    Acceptance Criteria: KPI cards must display the top start station.
    """
    kpis = calculate_kpis(cleaned_sample_data)
    
    assert 'top_station' in kpis, "KPI dictionary must contain 'top_station'"
    assert 'top_station_trips' in kpis, "KPI dictionary must contain 'top_station_trips'"
    
    # Station A appears 3 times, others 1 time each
    assert kpis['top_station'] == 'Station A', "Top station should be 'Station A'"
    assert kpis['top_station_trips'] == 3, "Top station should have 3 trips"


def test_calculate_kpis_with_empty_data():
    """
    Task 2: Test that KPI calculation handles empty data gracefully.
    
    Acceptance Criteria: KPI cards must display valid values even with empty data.
    """
    empty_data = pd.DataFrame()
    kpis = calculate_kpis(empty_data)
    
    assert kpis['total_trips'] == 0, "Total trips should be 0 for empty data"
    assert kpis['median_duration'] == 0, "Median duration should be 0 for empty data"
    assert kpis['top_station'] == 'N/A', "Top station should be 'N/A' for empty data"
    assert kpis['top_station_trips'] == 0, "Top station trips should be 0 for empty data"


# ============================================================================
# Task 3: Test Dynamic Filtering
# ============================================================================

def test_kpis_update_with_filtered_data(cleaned_sample_data):
    """
    Task 3: Test that KPI values update when data is filtered.
    
    Acceptance Criteria: KPI values must update dynamically when filters are applied.
    """
    # Calculate KPIs for full dataset
    full_kpis = calculate_kpis(cleaned_sample_data)
    
    # Filter to only Station A trips
    filtered_data = cleaned_sample_data[
        cleaned_sample_data['Start Station Name'] == 'Station A'
    ]
    filtered_kpis = calculate_kpis(filtered_data)
    
    # Assert that KPIs changed
    assert filtered_kpis['total_trips'] < full_kpis['total_trips'], \
        "Filtered total trips should be less than full dataset"
    assert filtered_kpis['total_trips'] == 3, \
        "Filtered dataset should have 3 trips from Station A"
    assert filtered_kpis['top_station'] == 'Station A', \
        "Top station should be Station A when filtered to Station A only"


def test_kpis_with_user_type_filter(cleaned_sample_data):
    """
    Task 3: Test that KPIs update correctly with user type filtering.
    
    Acceptance Criteria: KPI values must reflect filtered data.
    """
    # Filter to only Annual Members
    filtered_data = cleaned_sample_data[
        cleaned_sample_data['User Type'] == 'Annual Member'
    ]
    kpis = calculate_kpis(filtered_data)
    
    # Should have 3 Annual Member trips
    assert kpis['total_trips'] == 3, "Should have 3 Annual Member trips"


def test_kpis_with_date_filter(cleaned_sample_data):
    """
    Task 3: Test that KPIs update correctly with date filtering.
    
    Acceptance Criteria: KPI values must reflect filtered date range.
    """
    # Filter to specific date range (first 2 trips)
    filtered_data = cleaned_sample_data[
        cleaned_sample_data['Start Time'] < pd.Timestamp('2024-01-01 10:00:00')
    ]
    kpis = calculate_kpis(filtered_data)
    
    assert kpis['total_trips'] == 2, "Should have 2 trips before 10:00"


# ============================================================================
# Task 4: Test with Sample Dataset
# ============================================================================

def test_generate_sample_data_structure():
    """
    Task 4: Test that generated sample data has correct structure.
    
    Acceptance Criteria: Sample dataset must have all required columns.
    """
    sample_data = generate_sample_data(100)
    
    required_columns = [
        'Trip Id', 'Trip Duration ', 'Start Station Id', 'Start Time',
        'Start Station Name', 'End Station Id', 'End Time', 'End Station Name',
        'Bike Id', 'User Type', 'Model'
    ]
    
    for col in required_columns:
        assert col in sample_data.columns, f"Sample data must contain '{col}' column"
    
    assert len(sample_data) == 100, "Sample data should have requested number of rows"


def test_kpis_with_generated_sample_data():
    """
    Task 4: Test that KPI cards display correct values with generated sample data.
    
    Acceptance Criteria: KPI cards must display correct values when tested with sample dataset.
    """
    # Generate sample data
    sample_data = generate_sample_data(500)
    
    # Clean the data
    cleaned_data = clean_data(sample_data)
    
    # Calculate KPIs
    kpis = calculate_kpis(cleaned_data)
    
    # Verify all KPI values are valid
    assert kpis['total_trips'] > 0, "Total trips should be greater than 0"
    assert kpis['total_trips'] <= 500, "Total trips should not exceed sample size"
    
    assert kpis['median_duration'] > 0, "Median duration should be greater than 0"
    assert kpis['median_duration'] < 200, "Median duration should be reasonable (< 200 min)"
    
    assert kpis['top_station'] != 'N/A', "Top station should be identified"
    assert kpis['top_station_trips'] > 0, "Top station should have at least 1 trip"


def test_kpis_consistency_across_sample_sizes():
    """
    Task 4: Test that KPI calculation is consistent across different sample sizes.
    
    Acceptance Criteria: KPIs must be calculated correctly regardless of dataset size.
    """
    for sample_size in [50, 100, 500]:
        sample_data = generate_sample_data(sample_size)
        cleaned_data = clean_data(sample_data)
        kpis = calculate_kpis(cleaned_data)
        
        # All KPIs should be present and valid
        assert kpis['total_trips'] > 0, \
            f"Total trips should be > 0 for sample size {sample_size}"
        assert kpis['median_duration'] > 0, \
            f"Median duration should be > 0 for sample size {sample_size}"
        assert kpis['top_station'] != 'N/A', \
            f"Top station should be identified for sample size {sample_size}"


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_pipeline_with_sample_data():
    """
    Integration test: Full pipeline from sample generation to KPI display.
    
    Tests all tasks together:
    - Generate sample data (Task 4)
    - Clean data (pipeline)
    - Calculate KPIs (Task 2)
    - Verify dynamic updates work (Task 3)
    """
    # Generate and clean data
    raw_data = generate_sample_data(200)
    cleaned_data = clean_data(raw_data)
    
    # Calculate KPIs for full dataset
    full_kpis = calculate_kpis(cleaned_data)
    
    # Apply filter (simulate user interaction)
    stations = cleaned_data['Start Station Name'].unique()
    if len(stations) > 1:
        filtered_data = cleaned_data[
            cleaned_data['Start Station Name'] == stations[0]
        ]
        filtered_kpis = calculate_kpis(filtered_data)
        
        # Verify KPIs changed appropriately
        assert filtered_kpis['total_trips'] <= full_kpis['total_trips'], \
            "Filtered trips should not exceed full dataset trips"
        
        if filtered_data['Start Station Name'].nunique() == 1:
            assert filtered_kpis['top_station'] == stations[0], \
                "Top station should match the filtered station"


def test_kpi_data_types():
    """Test that all KPI values have correct data types."""
    sample_data = generate_sample_data(100)
    cleaned_data = clean_data(sample_data)
    kpis = calculate_kpis(cleaned_data)
    
    assert isinstance(kpis['total_trips'], int), "Total trips must be integer"
    assert isinstance(kpis['median_duration'], (int, float)), \
        "Median duration must be numeric"
    assert isinstance(kpis['top_station'], str), "Top station must be string"
    assert isinstance(kpis['top_station_trips'], int), \
        "Top station trips must be integer"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
