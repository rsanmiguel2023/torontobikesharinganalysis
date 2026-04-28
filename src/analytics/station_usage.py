"""
Station Usage Analytics Module

This module provides functionality to analyze and visualize bike sharing station
usage patterns, identifying high-traffic locations and providing comprehensive
station statistics.

Functions:
    get_top_stations: Standalone function for quick top-N station analysis

Classes:
    StationUsageAnalyzer: Comprehensive analyzer with visualization capabilities
"""

from __future__ import annotations
from typing import Optional, Tuple, Dict, Any
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


def get_top_stations(data: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get the top N stations by trip count.
    
    This is a standalone function for quick analysis. For more features,
    use the StationUsageAnalyzer class which provides visualization and
    additional statistical methods.
    
    Args:
        data (pd.DataFrame): DataFrame containing 'Start Station Name' column
        n (int): Number of top stations to return (default: 10)
    
    Returns:
        pd.DataFrame: Tidy DataFrame with columns:
            - Station Name: Name of the station
            - Trip Count: Number of trips starting from this station
            
            Sorted by trip count (descending), ties broken alphabetically
    
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
    
    Notes:
        - Aggregates by 'Start Station Name' column
        - Returns consistent ordering (count desc, name asc)
        - Resets index for clean output
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
    for identifying high-traffic bike sharing stations and understanding
    usage distribution patterns.
    
    Attributes:
        data (pd.DataFrame): The bike sharing trip data
    
    Methods:
        get_top_stations: Get top N stations by trip count
        create_top_stations_chart: Create bar chart visualization
        get_station_summary: Get summary of all stations
        get_station_statistics: Get statistical summary of usage
    
    Example:
        >>> data = pd.DataFrame({
        ...     'Start Station Name': ['Union Station', 'Queen St', 'Union Station'],
        ...     'Trip Id': [1, 2, 3]
        ... })
        >>> analyzer = StationUsageAnalyzer(data)
        >>> top_stations = analyzer.get_top_stations(n=5)
        >>> analyzer.create_top_stations_chart(n=10, output_path='chart.png')
        >>> stats = analyzer.get_station_statistics()
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the analyzer with bike sharing data.
        
        Args:
            data (pd.DataFrame): DataFrame with bike trip data. Must contain
                                'Start Station Name' column.
        
        Raises:
            ValueError: If required columns are missing from the data
        
        Example:
            >>> analyzer = StationUsageAnalyzer(trip_data)
        """
        self.data = data
        self._validate_data()
    
    def _validate_data(self) -> None:
        """
        Validate that required columns exist in the data.
        
        Raises:
            ValueError: If required columns are missing
        
        Notes:
            - Called automatically during initialization
            - Ensures data integrity before analysis
        """
        required_columns = ['Start Station Name']
        missing = [col for col in required_columns if col not in self.data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    
    def get_top_stations(self, n: int = 10) -> pd.DataFrame:
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
            >>> print(top_5.head())
        
        Notes:
            - Delegates to standalone get_top_stations() function
            - Provides consistent interface within analyzer class
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
    
    def create_top_stations_chart(
        self,
        n: int = 10,
        figsize: Tuple[int, int] = (12, 6),
        output_path: Optional[str] = None
    ) -> Optional[matplotlib.figure.Figure]:
        """
        Create a bar chart visualization of top N stations.
        
        Creates a professional bar chart displaying the top stations by trip count
        with clear labels, counts on bars, and proper formatting.
        
        Args:
            n (int): Number of top stations to display (default: 10)
            figsize (Tuple[int, int]): Figure size in inches as (width, height) (default: (12, 6))
            output_path (Optional[str]): Path to save the chart. If None, returns figure
                                         without saving. If provided, saves to file and
                                         closes the figure.
        
        Returns:
            Optional[matplotlib.figure.Figure]: The created figure (only if output_path is None),
                                               otherwise None after saving
        
        Example:
            >>> analyzer = StationUsageAnalyzer(data)
            >>> # Save to file
            >>> analyzer.create_top_stations_chart(n=10, output_path='top_stations.png')
            >>> # Or get figure object for further customization
            >>> fig = analyzer.create_top_stations_chart(n=10)
            >>> plt.show()
        
        Notes:
            - Uses non-interactive Agg backend for server environments
            - Includes value labels on bars for clarity
            - Automatically handles layout to prevent label cutoff
            - Closes figure after saving to free memory
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
    
    def get_station_summary(self) -> pd.DataFrame:
        """
        Get a summary of all stations with their trip counts.
        
        Returns all stations in the dataset with their corresponding trip counts,
        sorted by trip count in descending order.
        
        Returns:
            pd.DataFrame: DataFrame with all stations and their trip counts,
                         sorted by trip count (descending)
        
        Example:
            >>> analyzer = StationUsageAnalyzer(data)
            >>> summary = analyzer.get_station_summary()
            >>> print(f"Total stations: {len(summary)}")
        
        Notes:
            - Includes all unique stations in the dataset
            - Useful for comprehensive analysis beyond top N
        """
        return self.get_top_stations(n=len(self.data['Start Station Name'].unique()))
    
    def get_station_statistics(self) -> Dict[str, Any]:
        """
        Get statistical summary of station usage.
        
        Provides comprehensive statistics about station usage patterns including
        counts, averages, and distribution metrics.
        
        Returns:
            Dict[str, Any]: Dictionary containing:
                - total_stations (int): Total number of unique stations
                - total_trips (int): Total number of trips
                - avg_trips_per_station (float): Average trips per station
                - median_trips_per_station (float): Median trips per station
                - max_trips (int): Maximum trips for any station
                - min_trips (int): Minimum trips for any station
        
        Example:
            >>> analyzer = StationUsageAnalyzer(data)
            >>> stats = analyzer.get_station_statistics()
            >>> print(f"Total stations: {stats['total_stations']}")
            >>> print(f"Average trips per station: {stats['avg_trips_per_station']:.2f}")
        
        Notes:
            - Useful for understanding overall usage distribution
            - Helps identify concentration of activity
            - All metrics based on trip counts per station
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
