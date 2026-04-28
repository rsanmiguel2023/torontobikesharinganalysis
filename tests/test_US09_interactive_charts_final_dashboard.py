"""
Test suite for US09: Interactive Charts Final Dashboard

Tests the integration of reusable filter functions into the dashboard.
Verifies that sidebar widgets correctly pass filter selections into the data pipeline.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Setup project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Import reusable filter functions
from utils.filters import (
    filter_by_date_range,
    filter_by_start_station,
    filter_by_user_type
)

# Import dashboard functions
from data_processing.framework_dashboard import generate_sample_data
from analytics.kpi_metrics import calculate_kpis


class TestFilterIntegration:
    """Test the integration of reusable filter functions in the dashboard"""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing"""
        return generate_sample_data(num_rows=200)
    
    def test_filter_by_date_range_integration(self, sample_data):
        """Test date range filter integration"""
        # Get date range
        min_date = sample_data['Start Time'].min()
        max_date = sample_data['Start Time'].max()
        mid_date = min_date + (max_date - min_date) / 2
        
        # Apply date filter
        filtered = filter_by_date_range(
            sample_data,
            start_date=min_date,
            end_date=mid_date,
            time_column='Start Time'
        )
        
        assert len(filtered) > 0
        assert len(filtered) < len(sample_data)
        assert all(filtered['Start Time'] <= mid_date)
        
    def test_filter_by_station_integration(self, sample_data):
        """Test station filter integration"""
        # Get available stations
        stations = sample_data['Start Station Name'].unique()
        test_stations = list(stations[:3])  # Select first 3 stations as list
        
        # Apply station filter
        filtered = filter_by_start_station(
            sample_data,
            stations=test_stations,
            column='Start Station Name'
        )
        
        assert len(filtered) > 0
        assert all(filtered['Start Station Name'].isin(test_stations))
        
    def test_filter_by_user_type_integration(self, sample_data):
        """Test user type filter integration"""
        # Filter for Annual Members only
        filtered = filter_by_user_type(
            sample_data,
            user_types=['Annual Member'],
            column='User Type'
        )
        
        assert len(filtered) > 0
        assert all(filtered['User Type'].str.lower() == 'annual member')
        
    def test_multiple_filters_chained(self, sample_data):
        """Test that multiple filters can be chained together"""
        # Get parameters
        min_date = sample_data['Start Time'].min()
        max_date = sample_data['Start Time'].max()
        mid_date = min_date + (max_date - min_date) / 2
        test_station = sample_data['Start Station Name'].iloc[0]
        
        # Chain multiple filters
        filtered = sample_data.copy()
        filtered = filter_by_date_range(filtered, start_date=min_date, end_date=mid_date, time_column='Start Time')
        filtered = filter_by_start_station(filtered, stations=[test_station], column='Start Station Name')
        filtered = filter_by_user_type(filtered, user_types=['Annual Member'], column='User Type')
        
        # Verify all filters were applied
        assert len(filtered) <= len(sample_data)
        if len(filtered) > 0:
            assert all(filtered['Start Time'] <= mid_date)
            assert all(filtered['Start Station Name'] == test_station)
            assert all(filtered['User Type'].str.lower() == 'annual member')
    
    def test_kpis_update_with_filters(self, sample_data):
        """Test that KPIs update correctly when filters are applied"""
        # Calculate KPIs for full dataset
        kpis_full = calculate_kpis(sample_data)
        
        # Apply a filter
        filtered = filter_by_user_type(
            sample_data,
            user_types=['Annual Member'],
            column='User Type'
        )
        
        # Calculate KPIs for filtered data
        kpis_filtered = calculate_kpis(filtered)
        
        # Filtered should have fewer or equal trips
        assert kpis_filtered['total_trips'] <= kpis_full['total_trips']
        assert kpis_filtered['total_trips'] == len(filtered)


class TestDashboardKPI:
    """Test cases for dashboard KPI functionality"""
    
    def test_generate_sample_data(self):
        """Test sample data generation"""
        data = generate_sample_data(num_rows=100)
        
        assert len(data) == 100
        assert 'Trip Id' in data.columns
        assert 'Trip Duration ' in data.columns
        assert 'Start Station Name' in data.columns
        assert 'User Type' in data.columns
        
    def test_calculate_kpis_basic(self):
        """Test basic KPI calculations"""
        data = generate_sample_data(num_rows=50)
        kpis = calculate_kpis(data)
        
        assert 'total_trips' in kpis
        assert 'median_duration' in kpis
        assert 'top_station' in kpis
        assert 'top_station_trips' in kpis
        
        assert kpis['total_trips'] == 50
        assert kpis['median_duration'] > 0
        assert isinstance(kpis['top_station'], str)
        assert kpis['top_station_trips'] > 0
        
    def test_filter_with_kpis(self):
        """Test filtering and KPI calculation together"""
        data = generate_sample_data(num_rows=100)
        
        # Filter by user type using reusable filter function
        filtered = filter_by_user_type(
            data,
            user_types=['Annual Member'],
            column='User Type'
        )
        
        # Calculate KPIs on filtered data
        kpis = calculate_kpis(filtered)
        
        assert kpis['total_trips'] == len(filtered)
        assert kpis['total_trips'] <= 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
