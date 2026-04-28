"""
Test-Driven Development Cycle for Usage Summary Feature (US04)

User Story: As a planner, I want top stations so that I can identify high traffic areas.

This file demonstrates a complete TDD cycle:
1. RED: Write failing tests (2 tests)
2. GREEN: Implement minimal functionality (2 implementations)
3. REFACTOR: Clean up and improve code structure (1 refactoring)
"""

import pandas as pd
import pytest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt


# Import production code
from analytics.station_usage import get_top_stations, StationUsageAnalyzer


# ============================================================================
# RED PHASE: FAILING TESTS
# ============================================================================

def test_get_top_stations_basic():
    """
    RED - Task 1: Test for top N stations aggregation.
    
    Acceptance Criteria: The test must fail if the aggregation does not 
    correctly identify the top stations by trip count.
    
    This test will FAIL initially because the function doesn't exist yet.
    """
    # Arrange: Create sample data with various trip counts
    sample_data = pd.DataFrame({
        'Start Station Name': ['Station A', 'Station B', 'Station A', 
                               'Station C', 'Station B', 'Station A',
                               'Station D', 'Station B'],
        'Trip Id': [1, 2, 3, 4, 5, 6, 7, 8]
    })
    
    # Act: Call the function (will fail - function doesn't exist yet)
    result = get_top_stations(sample_data, n=3)
    
    # Assert: Verify correct stations and counts
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"
    assert len(result) == 3, "Should return top 3 stations"
    assert 'Station Name' in result.columns, "Should have 'Station Name' column"
    assert 'Trip Count' in result.columns, "Should have 'Trip Count' column"
    
    # Verify the top 3 stations are correct
    expected_top_3 = ['Station A', 'Station B', 'Station C']
    assert result['Station Name'].tolist() == expected_top_3, \
        "Should return stations in descending order by trip count"
    
    # Verify the counts are correct
    assert result['Trip Count'].tolist() == [3, 3, 1], \
        "Trip counts should be correct"


def test_get_top_stations_handles_ties():
    """
    RED - Task 4: Test for handling ties in trip counts.
    
    Acceptance Criteria: Unit tests must confirm that ties in trip counts 
    are resolved consistently according to a defined rule.
    
    This test will FAIL initially because tie-breaking logic doesn't exist yet.
    Rule: Ties should be broken alphabetically by station name.
    """
    # Arrange: Create data where stations have same trip counts
    sample_data = pd.DataFrame({
        'Start Station Name': ['Station Z', 'Station A', 'Station Z',
                               'Station A', 'Station M', 'Station M'],
        'Trip Id': [1, 2, 3, 4, 5, 6]
    })
    
    # Act: Call the function with ties present
    result = get_top_stations(sample_data, n=3)
    
    # Assert: Verify ties are broken alphabetically
    assert len(result) == 3, "Should return top 3 stations"
    
    # All stations have 2 trips, so alphabetical order should determine ranking
    expected_order = ['Station A', 'Station M', 'Station Z']
    assert result['Station Name'].tolist() == expected_order, \
        "Ties should be resolved alphabetically by station name"
    
    assert all(result['Trip Count'] == 2), \
        "All stations should have 2 trips in this test"


# ============================================================================
# GREEN PHASE: MINIMAL IMPLEMENTATION
# ============================================================================
# Production code has been moved to: src/data_processing/usage_summary.py
#
# GREEN 1: Basic aggregation function (get_top_stations)
#   - Aggregates trip counts by station
#   - Returns tidy DataFrame with station names and counts
#
# GREEN 2: Enhanced with tie-breaking logic
#   - Sorts by trip count (descending) then station name (ascending)
#   - Ensures consistent, predictable results
#
# ============================================================================
# REFACTOR PHASE: CLEANUP AND IMPROVEMENT
# ============================================================================
# Production code has been moved to: src/data_processing/usage_summary.py
#
# REFACTOR: StationUsageAnalyzer class
#   - Better code organization (class-based structure)
#   - Input data validation
#   - Visualization capability (create_top_stations_chart)
#   - Comprehensive documentation
#   - Additional utility methods (get_station_summary, get_station_statistics)


# ============================================================================
# TESTS FOR REFACTORED CODE
# ============================================================================

def test_station_usage_analyzer_initialization():
    """Test that the analyzer initializes correctly with valid data."""
    sample_data = pd.DataFrame({
        'Start Station Name': ['Station A', 'Station B', 'Station A'],
        'Trip Id': [1, 2, 3]
    })
    
    analyzer = StationUsageAnalyzer(sample_data)
    assert analyzer.data is not None
    assert len(analyzer.data) == 3


def test_station_usage_analyzer_validates_data():
    """Test that the analyzer raises error for invalid data."""
    invalid_data = pd.DataFrame({
        'Wrong Column': [1, 2, 3]
    })
    
    with pytest.raises(ValueError, match="Missing required columns"):
        StationUsageAnalyzer(invalid_data)


def test_analyzer_get_top_stations():
    """Test that the analyzer's get_top_stations method works correctly."""
    sample_data = pd.DataFrame({
        'Start Station Name': ['Station A', 'Station B', 'Station A', 
                               'Station C', 'Station B', 'Station A'],
        'Trip Id': [1, 2, 3, 4, 5, 6]
    })
    
    analyzer = StationUsageAnalyzer(sample_data)
    result = analyzer.get_top_stations(n=2)
    
    assert len(result) == 2
    assert result['Station Name'].tolist() == ['Station A', 'Station B']
    assert result['Trip Count'].tolist() == [3, 2]


def test_create_top_stations_chart():
    """Test that the visualization function creates a chart without errors."""
    sample_data = pd.DataFrame({
        'Start Station Name': ['Station A', 'Station B', 'Station C'] * 10,
        'Trip Id': range(30)
    })
    
    analyzer = StationUsageAnalyzer(sample_data)
    
    # Create chart without saving
    fig = analyzer.create_top_stations_chart(n=3)
    
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    
    # Clean up
    plt.close(fig)


def test_chart_saves_to_file(tmp_path):
    """Test that the chart can be saved to a file."""
    sample_data = pd.DataFrame({
        'Start Station Name': ['Station A', 'Station B', 'Station C'] * 10,
        'Trip Id': range(30)
    })
    
    analyzer = StationUsageAnalyzer(sample_data)
    
    # Save chart to temporary file
    output_file = tmp_path / "test_chart.png"
    analyzer.create_top_stations_chart(n=3, output_path=str(output_file))
    
    assert output_file.exists()
    assert output_file.stat().st_size > 0


# ============================================================================
# DEMONSTRATION FUNCTION
# ============================================================================

def demonstrate_tdd_cycle():
    """
    Demonstrate the complete TDD cycle with sample data.
    
    This function shows:
    1. RED: Tests fail initially (would fail if functions didn't exist)
    2. GREEN: Minimal implementation makes tests pass
    3. REFACTOR: Improved code structure with same functionality
    """
    print("=" * 70)
    print("TDD CYCLE DEMONSTRATION - US04: Top Stations Usage Summary")
    print("=" * 70)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'Start Station Name': [
            'Union Station', 'Queen St', 'Union Station',
            'King St', 'Queen St', 'Union Station',
            'Yonge St', 'King St', 'Union Station',
            'Queen St', 'Bloor St', 'Yonge St'
        ],
        'Trip Id': range(1, 13)
    })
    
    print("\n1. RED PHASE: Tests would fail without implementation")
    print("   - test_get_top_stations_basic")
    print("   - test_get_top_stations_handles_ties")
    
    print("\n2. GREEN PHASE: Minimal implementation")
    print("\n   GREEN 1: Basic function implementation")
    result = get_top_stations(sample_data, n=3)
    print("\n   Top 3 Stations:")
    print(result.to_string(index=False))
    
    print("\n   GREEN 2: Enhanced with tie-breaking logic")
    tie_data = pd.DataFrame({
        'Start Station Name': ['Station Z', 'Station A', 'Station Z',
                               'Station A', 'Station M', 'Station M'],
        'Trip Id': [1, 2, 3, 4, 5, 6]
    })
    tie_result = get_top_stations(tie_data, n=3)
    print("\n   Tie-breaking example (all have 2 trips, sorted alphabetically):")
    print(tie_result.to_string(index=False))
    
    print("\n3. REFACTOR PHASE: Improved structure and added visualization")
    analyzer = StationUsageAnalyzer(sample_data)
    refactored_result = analyzer.get_top_stations(n=5)
    print("\n   Top 5 Stations (using refactored analyzer):")
    print(refactored_result.to_string(index=False))
    
    print("\n   Visualization capability added:")
    print("   - create_top_stations_chart() method")
    print("   - Creates bar chart with clear labels and counts")
    print("   - Supports saving to file or returning figure object")
    
    print("\n" + "=" * 70)
    print("TDD CYCLE COMPLETE")
    print("=" * 70)
    print("\nAll tasks completed:")
    print("✓ Task 1: Failing test for top N stations (RED)")
    print("✓ Task 2: Aggregation function implementation (GREEN)")
    print("✓ Task 3: Bar chart visualization (REFACTOR)")
    print("✓ Task 4: Unit tests for ties (RED + GREEN)")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_tdd_cycle()
    
    print("\n" + "=" * 70)
    print("To run the tests, use: pytest tests/US04-usage_summary.py -v")
    print("=" * 70)
