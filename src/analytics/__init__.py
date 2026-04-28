"""
Analytics Module

This module provides comprehensive analytics functions for bike sharing data analysis.
All analytics logic is organized into dedicated submodules for better maintainability.

Available Modules:
    - peak_usage: Peak usage analysis (hourly/weekday patterns)
    - trip_duration: Trip duration statistics and histograms
    - station_usage: Station usage patterns and top stations
    - user_type_breakdown: User type distribution analysis
    - kpi_metrics: Key performance indicators for dashboards

Quick imports:
    from analytics.peak_usage import analyze_peak_usage
    from analytics.trip_duration import calculate_duration_stats
    from analytics.station_usage import get_top_stations, StationUsageAnalyzer
    from analytics.user_type_breakdown import user_type_breakdown
    from analytics.kpi_metrics import calculate_kpis
"""

# Export main analytics functions for convenient imports
from analytics.peak_usage import analyze_peak_usage
from analytics.trip_duration import calculate_duration_stats, valid_durations, empty_stats
from analytics.station_usage import get_top_stations, StationUsageAnalyzer
from analytics.user_type_breakdown import user_type_breakdown
from analytics.kpi_metrics import calculate_kpis

__all__ = [
    # Peak usage analysis
    'analyze_peak_usage',
    
    # Trip duration analysis
    'calculate_duration_stats',
    'valid_durations',
    'empty_stats',
    
    # Station usage analysis
    'get_top_stations',
    'StationUsageAnalyzer',
    
    # User type analysis
    'user_type_breakdown',
    
    # KPI metrics
    'calculate_kpis',
]
