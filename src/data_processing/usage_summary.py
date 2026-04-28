"""
Usage Summary Module for Toronto Bike Sharing Analytics Tool

This module provides functionality to analyze and visualize top bike sharing stations
by trip count. It supports identifying high traffic areas for planning purposes.

User Story: As a planner, I want top stations so that I can identify high traffic areas.

Classes:
    StationUsageAnalyzer: Main class for analyzing station usage and creating visualizations

Functions:
    get_top_stations: Standalone function for quick station analysis
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


def get_top_stations(data, n=10):
    """
    Get the top N stations by trip count.
    
    This is a standalone function for quick analysis. For more features,
    use the StationUsageAnalyzer class.
    
    Args:
        data (pd.DataFrame): DataFrame containing 'Start Station Name' column
        n (int): Number of top stations to return (default: 10)
    
    Returns:
        pd.DataFrame: Tidy DataFrame with 'Station Name' and 'Trip Count' columns,
                      sorted by trip count (descending), ties broken alphabetically
    
    Example:
        >>> data = pd.DataFrame({
        ...     'Start Station Name': ['Station A', 'Station B', 'Station A'],
        ...     'Trip Id': [1, 2, 3]
        ... })
        >>> result = get_top_stations(data, n=2)
        >>> print(result)
          Station Name  Trip Count
        0    Station A           2
        1    Station B           1
    """
    # Aggregate trip counts by station
    station_counts = data.groupby('Start Station Name').size().reset_index(
        name='Trip Count'
    )
    
    # Rename for clarity
    station_counts = station_counts.rename(
        columns={'Start Station Name': 'Station Name'}
    )
    
    # Sort by count (descending) then name (ascending) for consistent tie-breaking
    station_counts = station_counts.sort_values(
        by=['Trip Count', 'Station Name'],
        ascending=[False, True]
    )
    
    # Return top N stations
    return station_counts.head(n).reset_index(drop=True)


class StationUsageAnalyzer:
    """
    Analyzer for bike sharing station usage patterns.
    
    This class provides comprehensive analysis and visualization capabilities
    for identifying high-traffic bike sharing stations.
    
    Attributes:
        data (pd.DataFrame): The bike sharing trip data
    
    Example:
        >>> data = pd.DataFrame({
        ...     'Start Station Name': ['Union Station', 'Queen St', 'Union Station'],
        ...     'Trip Id': [1, 2, 3]
        ... })
        >>> analyzer = StationUsageAnalyzer(data)
        >>> top_stations = analyzer.get_top_stations(n=5)
        >>> analyzer.create_top_stations_chart(n=10, output_path='chart.png')
    """
    
    def __init__(self, data):
        """
        Initialize the analyzer with bike sharing data.
        
        Args:
            data (pd.DataFrame): DataFrame with bike trip data. Must contain
                                'Start Station Name' column.
        
        Raises:
            ValueError: If required columns are missing from the data
        """
        self.data = data
        self._validate_data()
    
    def _validate_data(self):
        """
        Validate that required columns exist in the data.
        
        Raises:
            ValueError: If required columns are missing
        """
        required_columns = ['Start Station Name']
        missing = [col for col in required_columns if col not in self.data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def get_top_stations(self, n=10):
        """
        Get the top N stations by trip count.
        
        Args:
            n (int): Number of top stations to return (default: 10)
        
        Returns:
            pd.DataFrame: Tidy DataFrame with columns:
                - Station Name: Name of the station
                - Trip Count: Number of trips starting from this station
                
                Sorted by trip count (descending), ties broken alphabetically.
        
        Example:
            >>> analyzer = StationUsageAnalyzer(data)
            >>> top_5 = analyzer.get_top_stations(n=5)
        """
        # Aggregate trip counts by station
        station_counts = self.data.groupby('Start Station Name').size().reset_index(
            name='Trip Count'
        )
        
        # Rename for clarity
        station_counts = station_counts.rename(
            columns={'Start Station Name': 'Station Name'}
        )
        
        # Sort by count (descending) then name (ascending) for consistent tie-breaking
        station_counts = station_counts.sort_values(
            by=['Trip Count', 'Station Name'],
            ascending=[False, True]
        )
        
        # Return top N
        return station_counts.head(n).reset_index(drop=True)
    
    def create_top_stations_chart(self, n=10, figsize=(12, 6), output_path=None):
        """
        Create a bar chart visualization of top N stations.
        
        Creates a professional bar chart displaying the top stations by trip count
        with clear labels, counts on bars, and proper formatting.
        
        Args:
            n (int): Number of top stations to display (default: 10)
            figsize (tuple): Figure size in inches as (width, height) (default: (12, 6))
            output_path (str, optional): Path to save the chart. If None, returns figure
                                        without saving. If provided, saves to file and
                                        closes the figure.
        
        Returns:
            matplotlib.figure.Figure: The created figure (only if output_path is None)
        
        Example:
            >>> analyzer = StationUsageAnalyzer(data)
            >>> # Save to file
            >>> analyzer.create_top_stations_chart(n=10, output_path='top_stations.png')
            >>> # Or get figure object
            >>> fig = analyzer.create_top_stations_chart(n=10)
            >>> plt.show()
        """
        # Get top stations data
        top_stations = self.get_top_stations(n)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create bar chart
        bars = ax.bar(
            range(len(top_stations)),
            top_stations['Trip Count'],
            color='steelblue',
            edgecolor='navy',
            alpha=0.8
        )
        
        # Customize the chart
        ax.set_xlabel('Station Name', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Trips', fontsize=12, fontweight='bold')
        ax.set_title(
            f'Top {n} Bike Sharing Stations by Trip Count',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        
        # Set x-axis labels
        ax.set_xticks(range(len(top_stations)))
        ax.set_xticklabels(
            top_stations['Station Name'],
            rotation=45,
            ha='right'
        )
        
        # Add value labels on top of bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='bold'
            )
        
        # Add grid for better readability
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save or return
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            return None
        else:
            return fig
    
    def get_station_summary(self):
        """
        Get a summary of all stations with their trip counts.
        
        Returns:
            pd.DataFrame: DataFrame with all stations and their trip counts,
                         sorted by trip count (descending)
        """
        return self.get_top_stations(n=len(self.data['Start Station Name'].unique()))
    
    def get_station_statistics(self):
        """
        Get statistical summary of station usage.
        
        Returns:
            dict: Dictionary containing:
                - total_stations: Total number of unique stations
                - total_trips: Total number of trips
                - avg_trips_per_station: Average trips per station
                - median_trips_per_station: Median trips per station
                - max_trips: Maximum trips for any station
                - min_trips: Minimum trips for any station
        """
        station_counts = self.get_station_summary()
        
        return {
            'total_stations': len(station_counts),
            'total_trips': station_counts['Trip Count'].sum(),
            'avg_trips_per_station': station_counts['Trip Count'].mean(),
            'median_trips_per_station': station_counts['Trip Count'].median(),
            'max_trips': station_counts['Trip Count'].max(),
            'min_trips': station_counts['Trip Count'].min()
        }
