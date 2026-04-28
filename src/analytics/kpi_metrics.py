"""
KPI Metrics Analytics Module

This module provides functions for calculating Key Performance Indicators (KPIs)
for bike sharing analytics dashboards. KPIs include trip counts, duration metrics,
and station usage statistics.

Functions:
    calculate_kpis: Calculate comprehensive KPI metrics from bike sharing data
"""

from __future__ import annotations
from typing import Dict, Any
import pandas as pd


def calculate_kpis(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate Key Performance Indicators (KPIs) from bike sharing data.
    
    Computes essential metrics including trip counts, duration statistics,
    and top station information for dashboard displays.
    
    Args:
        data (pd.DataFrame): Cleaned bike sharing data with columns:
            - Trip Duration or Trip Duration  (seconds)
            - Start Station Name
            
    Returns:
        Dict[str, Any]: Dictionary containing:
            - total_trips (int): Total number of trips
            - median_duration (float): Median trip duration in minutes
            - top_station (str): Name of station with most trip starts
            - top_station_trips (int): Number of trips from top station
    
    Example:
        >>> data = pd.DataFrame({
        ...     'Trip Id': [1, 2, 3],
        ...     'Trip Duration ': [600, 1200, 900],  # seconds
        ...     'Start Station Name': ['Union Station', 'Queen St', 'Union Station']
        ... })
        >>> kpis = calculate_kpis(data)
        >>> print(f"Total trips: {kpis['total_trips']}")
        Total trips: 3
        >>> print(f"Median duration: {kpis['median_duration']:.1f} min")
        Median duration: 15.0 min
        >>> print(f"Top station: {kpis['top_station']}")
        Top station: Union Station
    
    Notes:
        - Returns zeros/N/A values if data is empty or missing required columns
        - Handles both 'Trip Duration' and 'Trip Duration ' column names
        - Converts duration from seconds to minutes for readability
        - Uses station_usage.get_top_stations() for top station calculation
    """
    # Import here to avoid circular dependency
    from analytics.station_usage import get_top_stations
    
    # Handle empty data
    if data.empty:
        return {
            'total_trips': 0,
            'median_duration': 0,
            'top_station': 'N/A',
            'top_station_trips': 0
        }
    
    # Calculate total trips
    total_trips = len(data)
    
    # Calculate median trip duration (convert seconds to minutes)
    median_duration = 0
    if 'Trip Duration ' in data.columns:
        median_duration = data['Trip Duration '].median() / 60  # Convert to minutes
    elif 'Trip Duration' in data.columns:
        median_duration = data['Trip Duration'].median() / 60  # Convert to minutes
    
    # Determine top start station
    top_station = 'N/A'
    top_station_trips = 0
    
    if 'Start Station Name' in data.columns:
        top_stations_df = get_top_stations(data, n=1)
        if not top_stations_df.empty:
            top_station = top_stations_df.iloc[0]['Station Name']
            top_station_trips = int(top_stations_df.iloc[0]['Trip Count'])
    
    return {
        'total_trips': total_trips,
        'median_duration': median_duration,
        'top_station': top_station,
        'top_station_trips': top_station_trips
    }
