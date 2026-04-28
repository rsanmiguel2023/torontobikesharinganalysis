"""
Example Usage of Usage Summary Module

This script demonstrates how to use the production-ready usage_summary module
for analyzing bike sharing station traffic.
"""

import os
import sys
import pandas as pd

# Setup paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from data_processing.usage_summary import get_top_stations, StationUsageAnalyzer


def example_basic_usage():
    """Example: Using the basic function"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Function Usage")
    print("=" * 70)
    
    # Sample data
    data = pd.DataFrame({
        'Start Station Name': [
            'Union Station', 'Queen St', 'Union Station',
            'King St', 'Queen St', 'Union Station',
            'Yonge St', 'King St', 'Union Station',
            'Queen St', 'Bloor St', 'Yonge St'
        ],
        'Trip Id': range(1, 13)
    })
    
    # Get top 5 stations
    top_5 = get_top_stations(data, n=5)
    
    print("\nTop 5 Stations:")
    print(top_5.to_string(index=False))
    print()


def example_analyzer_class():
    """Example: Using the StationUsageAnalyzer class"""
    print("=" * 70)
    print("EXAMPLE 2: StationUsageAnalyzer Class")
    print("=" * 70)
    
    # Sample data with more variety
    data = pd.DataFrame({
        'Start Station Name': [
            'Union Station', 'Queen St', 'Union Station',
            'King St', 'Queen St', 'Union Station',
            'Yonge St', 'King St', 'Union Station',
            'Queen St', 'Bloor St', 'Yonge St',
            'Spadina', 'Dundas St', 'Bloor St'
        ] * 3,  # Repeat to have more data
        'Trip Id': range(1, 46)
    })
    
    # Create analyzer
    analyzer = StationUsageAnalyzer(data)
    
    # Get top stations
    print("\nTop 10 Stations:")
    top_10 = analyzer.get_top_stations(n=10)
    print(top_10.to_string(index=False))
    
    # Get statistics
    print("\nStation Statistics:")
    stats = analyzer.get_station_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
    print()


def example_visualization():
    """Example: Creating a visualization"""
    print("=" * 70)
    print("EXAMPLE 3: Creating Visualization")
    print("=" * 70)
    
    # Sample data
    data = pd.DataFrame({
        'Start Station Name': [
            'Union Station', 'Queen St', 'King St',
            'Yonge St', 'Bloor St', 'Spadina',
            'Dundas St', 'College St', 'Bay St',
            'Front St'
        ] * 10,  # Create 100 trips total
        'Trip Id': range(1, 101)
    })
    
    # Create analyzer
    analyzer = StationUsageAnalyzer(data)
    
    # Create and save chart
    output_dir = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "top_stations_chart.png")
    analyzer.create_top_stations_chart(n=10, output_path=output_path)
    
    print(f"\nChart saved to: {output_path}")
    print("The chart displays:")
    print("  - Top 10 stations by trip count")
    print("  - Clear bar chart with labels")
    print("  - Trip counts displayed on each bar")
    print("  - Professional styling with grid")
    print()


def example_tie_handling():
    """Example: Handling ties in trip counts"""
    print("=" * 70)
    print("EXAMPLE 4: Tie-Breaking Logic")
    print("=" * 70)
    
    # Data with intentional ties
    data = pd.DataFrame({
        'Start Station Name': [
            'Station Z', 'Station A', 'Station Z',
            'Station A', 'Station M', 'Station M',
            'Station B', 'Station B'
        ],
        'Trip Id': range(1, 9)
    })
    
    print("\nAll stations have 2 trips each.")
    print("Ties are broken alphabetically by station name:")
    
    result = get_top_stations(data, n=4)
    print(result.to_string(index=False))
    
    print("\nNote: Stations are ordered A, B, M, Z (alphabetically)")
    print("      despite all having the same trip count.")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("USAGE SUMMARY MODULE - EXAMPLE DEMONSTRATIONS")
    print("=" * 70)
    print()
    
    # Run all examples
    example_basic_usage()
    example_analyzer_class()
    example_visualization()
    example_tie_handling()
    
    print("=" * 70)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 70)
    print("\nProduction code location:")
    print("  src/data_processing/usage_summary.py")
    print("\nAvailable imports:")
    print("  from data_processing.usage_summary import get_top_stations")
    print("  from data_processing.usage_summary import StationUsageAnalyzer")
    print()
