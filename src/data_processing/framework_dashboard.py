"""
Toronto BikeShare Analytics Dashboard

US 08: Dashboard KPIs
This Streamlit dashboard displays key performance indicators (KPIs) for bike sharing data.

Tasks implemented:
- Task 1: Design Streamlit layout with KPI section
- Task 2: Implement KPI cards (total trips, median duration, top station)
- Task 3: Connect to pipeline outputs with dynamic filtering
- Task 4: Test with sample dataset
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Setup project paths
# Get the project root (two levels up from dashboard_kpi.py in src/data_processing/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Import analytics modules
from analytics.station_usage import get_top_stations
from analytics.kpi_metrics import calculate_kpis

# Import reusable filter functions
from utils.filters import (
    filter_by_date_range,
    filter_by_start_station,
    filter_by_user_type
)


def generate_sample_data(num_rows=1000):
    """
    Generate sample bike sharing data for testing.
    
    Args:
        num_rows (int): Number of sample trips to generate
        
    Returns:
        pd.DataFrame: Sample bike sharing data
    """
    np.random.seed(42)
    
    # Sample station names
    stations = [
        "Union Station", "Queen St", "King St", "Yonge St", "Bloor St",
        "Spadina", "Dundas St", "College St", "Bay St", "Front St",
        "Harbourfront", "City Hall", "Eaton Centre", "Rogers Centre", "CN Tower"
    ]
    
    # Generate dates over the past 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    dates = [start_date + timedelta(
        seconds=np.random.randint(0, int((end_date - start_date).total_seconds()))
    ) for _ in range(num_rows)]
    
    # Generate trip durations (in seconds) - mostly between 5 and 60 minutes
    durations = np.random.gamma(shape=2, scale=600, size=num_rows).astype(int)
    durations = np.clip(durations, 300, 7200)  # 5 min to 2 hours
    
    # Generate data
    data = pd.DataFrame({
        'Trip Id': range(1, num_rows + 1),
        'Trip Duration ': durations,
        'Start Station Id': np.random.randint(100, 200, num_rows),
        'Start Time': dates,
        'Start Station Name': np.random.choice(stations, num_rows, p=[0.15, 0.12, 0.10, 0.08, 0.08, 
                                                                        0.07, 0.07, 0.06, 0.06, 0.05,
                                                                        0.05, 0.04, 0.04, 0.02, 0.01]),
        'End Station Id': np.random.randint(100, 200, num_rows),
        'End Station Name': np.random.choice(stations, num_rows),
        'Bike Id': np.random.randint(1000, 2000, num_rows),
        'User Type': np.random.choice(['Annual Member', 'Casual Member'], num_rows, p=[0.7, 0.3]),
        'Model': np.random.choice(['ICONIC', 'BOOST', 'ELECTRIC'], num_rows, p=[0.5, 0.3, 0.2])
    })
    
    # Calculate end times
    data['End Time'] = data.apply(
        lambda row: row['Start Time'] + timedelta(seconds=row['Trip Duration ']),
        axis=1
    )
    
    return data


# calculate_kpis function moved to analytics.kpi_metrics module
# Import with: from analytics.kpi_metrics import calculate_kpis


def display_kpi_cards(kpis):
    """
    Display KPI cards in a row.
    
    Args:
        kpis (dict): Dictionary containing KPI values
    """
    # Task 2: Implement KPI cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=" Total Trips",
            value=f"{kpis['total_trips']:,}",
            help="Total number of bike trips in the selected period"
        )
    
    with col2:
        st.metric(
            label="⏱️ Median Trip Duration",
            value=f"{kpis['median_duration']:.1f} min",
            help="Median duration of all trips in minutes"
        )
    
    with col3:
        st.metric(
            label="🚴 Top Start Station",
            value=kpis['top_station'],
            delta=f"{kpis['top_station_trips']} trips",
            help="Station with the most trip starts"
        )


def create_visualizations(data):
    """
    Create line and bar chart visualizations based on filtered data.
    
    Args:
        data (pd.DataFrame): Filtered bike sharing data
    """
    if data.empty:
        st.warning("⚠️ No data available for visualization")
        return
    
    st.subheader(" Visualizations")
    
    # Line chart - Trips Over Time
    st.subheader(" Trips Over Time")
    
    # Aggregate trips by date
    if 'Start Time' in data.columns:
        # Group by date
        data['Date'] = data['Start Time'].dt.date
        trips_by_date = data.groupby('Date').size().reset_index(name='Trips')
        trips_by_date['Date'] = pd.to_datetime(trips_by_date['Date'])
        
        if len(trips_by_date) > 0:
            # Create line chart
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(trips_by_date['Date'], trips_by_date['Trips'], 
                   marker='o', linewidth=2, markersize=6, color='steelblue')
            ax.set_xlabel('Date', fontsize=11, fontweight='bold')
            ax.set_ylabel('Number of Trips', fontsize=11, fontweight='bold')
            ax.set_title('Daily Trip Count', fontsize=12, fontweight='bold', pad=15)
            ax.grid(True, alpha=0.3, linestyle='--')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
            
            # Show summary stats
            st.caption(f" Total days: {len(trips_by_date)} | "
                      f"Avg trips/day: {trips_by_date['Trips'].mean():.1f} | "
                      f"Peak: {trips_by_date['Trips'].max()} trips")
        else:
            st.info("Not enough data for time series visualization")
    else:
        st.info("Start Time column not available")
    
    st.markdown("---")
    
    # Bar chart - Top Stations
    st.subheader(" Top Stations")
    
    # Get top 10 stations
    if 'Start Station Name' in data.columns:
        top_stations = get_top_stations(data, n=10)
        
        if len(top_stations) > 0:
            # Create bar chart
            fig, ax = plt.subplots(figsize=(12, 5))
            bars = ax.barh(range(len(top_stations)), 
                          top_stations['Trip Count'][::-1],
                          color='coral', edgecolor='darkred', alpha=0.8)
            
            ax.set_yticks(range(len(top_stations)))
            ax.set_yticklabels(top_stations['Station Name'][::-1])
            ax.set_xlabel('Number of Trips', fontsize=11, fontweight='bold')
            ax.set_ylabel('Station Name', fontsize=11, fontweight='bold')
            ax.set_title('Top 10 Start Stations', fontsize=12, fontweight='bold', pad=15)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2., 
                       f'{int(width)}',
                       ha='left', va='center', fontsize=9, 
                       fontweight='bold', color='black', 
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='white', alpha=0.7))
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            
            st.caption(f" Showing top {len(top_stations)} of "
                      f"{data['Start Station Name'].nunique()} stations")
        else:
            st.info("Not enough station data for visualization")
    else:
        st.info("Station Name column not available")
    
    st.markdown("---")
    
    # Trip Duration Distribution
    st.subheader(" Trip Duration Distribution")
    
    if 'Trip Duration' in data.columns and len(data) > 0:
        # Convert to minutes for better readability
        durations_min = data['Trip Duration'] / 60
        durations_min = durations_min[durations_min <= 120]  # Filter outliers > 2 hours
        
        if len(durations_min) > 0:
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.hist(durations_min, bins=30, color='mediumseagreen', 
                   edgecolor='darkgreen', alpha=0.8)
            ax.set_xlabel('Trip Duration (minutes)', fontsize=11, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=11, fontweight='bold')
            ax.set_title('Trip Duration Distribution', fontsize=12, fontweight='bold', pad=15)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.axvline(durations_min.median(), color='red', linestyle='--', 
                      linewidth=2, label=f'Median: {durations_min.median():.1f} min')
            ax.legend()
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
            
            st.caption(f" Mean: {durations_min.mean():.1f} min | "
                      f"Median: {durations_min.median():.1f} min | "
                      f"Std: {durations_min.std():.1f} min")
        else:
            st.info("No valid duration data for visualization")
    else:
        st.info("Trip Duration column not available")
    
    st.markdown("---")
    
    # User Type Breakdown
    st.subheader(" User Type Breakdown")
    
    if 'User Type' in data.columns and len(data) > 0:
        user_type_counts = data['User Type'].value_counts()
        
        if len(user_type_counts) > 0:
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            explode = [0.05] * len(user_type_counts)
            
            wedges, texts, autotexts = ax.pie(user_type_counts.values, 
                                               labels=user_type_counts.index,
                                               autopct='%1.1f%%',
                                               colors=colors[:len(user_type_counts)],
                                               explode=explode,
                                               startangle=90,
                                               textprops={'fontsize': 10, 'fontweight': 'bold'})
            
            ax.set_title('User Type Distribution', fontsize=12, fontweight='bold', pad=15)
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close()
            
            # Show counts
            breakdown_text = " | ".join([f"{k}: {v:,}" for k, v in user_type_counts.items()])
            st.caption(f" {breakdown_text}")
        else:
            st.info("No user type data for visualization")
    else:
        st.info("User Type column not available")


def apply_filters(data):
    """
    Apply filters to the data based on sidebar selections.
    Uses reusable filter functions from utils.filters module.
    
    Args:
        data (pd.DataFrame): Input data
        
    Returns:
        pd.DataFrame: Filtered data
    """
    filtered_data = data.copy()
    
    # Date range filter using reusable function
    if 'Start Time' in filtered_data.columns:
        st.sidebar.subheader("📅 Date Range")
        min_date = filtered_data['Start Time'].min().date()
        max_date = filtered_data['Start Time'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select date range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            # Use reusable filter function
            filtered_data = filter_by_date_range(
                filtered_data,
                start_date=start_date,
                end_date=end_date,
                time_column='Start Time'
            )
    
    # Station filter using reusable function
    if 'Start Station Name' in filtered_data.columns:
        st.sidebar.subheader("🚉 Station Filter")
        all_stations = sorted(filtered_data['Start Station Name'].unique())
        selected_stations = st.sidebar.multiselect(
            "Select stations:",
            options=all_stations,
            default=all_stations,
            help="Filter trips by start station"
        )
        
        if selected_stations:
            # Use reusable filter function
            filtered_data = filter_by_start_station(
                filtered_data,
                stations=selected_stations,
                column='Start Station Name'
            )
    
    # User type filter using reusable function
    if 'User Type' in filtered_data.columns:
        st.sidebar.subheader("👤 User Type")
        user_types = filtered_data['User Type'].unique()
        selected_user_types = st.sidebar.multiselect(
            "Select user types:",
            options=user_types,
            default=list(user_types),
            help="Filter trips by user type"
        )
        
        if selected_user_types:
            # Use reusable filter function
            filtered_data = filter_by_user_type(
                filtered_data,
                user_types=selected_user_types,
                column='User Type'
            )
    
    return filtered_data


def main():
    """Main dashboard application."""
    
    # Task 1: Design Streamlit layout
    st.set_page_config(
        page_title="Toronto BikeShare Analytics",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Dashboard Title with Logo
    col1, col2 = st.columns([1, 6])
    with col1:
        logo_path = os.path.join(os.path.dirname(__file__), "Toronto Bike-share logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)
    with col2:
        st.title("Toronto Bike-Share Analytics Dashboard")
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title(" Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Data source selection
    st.sidebar.subheader("📂 Data Source")
    data_source = st.sidebar.radio(
        "Choose data source:",
        options=["Sample Data", "Upload CSV"],
        help="Select whether to use sample data or upload your own"
    )
    
    # Load data
    if data_source == "Sample Data":
        st.sidebar.info("Using generated sample data for testing")
        num_samples = st.sidebar.slider(
            "Number of sample trips:",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100
        )
        raw_data = generate_sample_data(num_samples)
    else:
        st.sidebar.info("Upload a CSV file with bike sharing data")
        uploaded_file = st.sidebar.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload bike sharing trip data"
        )
        
        if uploaded_file is not None:
            raw_data = pd.read_csv(uploaded_file)
        else:
            st.warning("⚠️ Please upload a CSV file or select 'Sample Data'")
            st.stop()
    
    # Clean data
    try:
        cleaned_data = clean_data(raw_data)
        
        if cleaned_data.empty:
            st.error("❌ No valid data after cleaning. Please check your data source.")
            st.stop()
            
    except Exception as e:
        st.error(f"❌ Error processing data: {str(e)}")
        st.stop()
    
    st.sidebar.markdown("---")
    
    # Task 3: Connect to pipeline outputs with dynamic filtering
    filtered_data = apply_filters(cleaned_data)
    
    # Show filter results
    if len(filtered_data) < len(cleaned_data):
        st.sidebar.success(
            f"✅ Filtered: {len(filtered_data):,} of {len(cleaned_data):,} trips"
        )
    else:
        st.sidebar.info(f" Total trips: {len(cleaned_data):,}")
    
    # Task 2 & 4: Calculate and display KPI cards
    st.subheader(" Key Performance Indicators")
    
    if filtered_data.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filters.")
    else:
        kpis = calculate_kpis(filtered_data)
        display_kpi_cards(kpis)
    
    st.markdown("---")
    
    # Create main layout with two columns
    left_pane, right_pane = st.columns([2, 1])
    
    with left_pane:
        # Add visualization section in left pane
        create_visualizations(filtered_data)
    
    with right_pane:
        # Additional Analytics in right pane
        st.subheader(" Additional Analytics")
        
        if not filtered_data.empty:
            st.subheader("Top 10 Start Stations")
            top_stations = get_top_stations(filtered_data, n=10)
            st.dataframe(
                top_stations,
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            st.subheader("Trip Duration Statistics")
            duration_stats = calculate_duration_stats(filtered_data, "Trip Duration")
            
            if duration_stats['count'] > 0:
                stats_df = pd.DataFrame({
                    'Metric': ['Mean', 'Median', 'Min', 'Max', 'Count'],
                    'Value': [
                        f"{duration_stats['mean']/60:.1f} min",
                        f"{duration_stats['median']/60:.1f} min",
                        f"{duration_stats['min']/60:.1f} min",
                        f"{duration_stats['max']/60:.1f} min",
                        f"{duration_stats['count']:,}"
                    ]
                })
                st.dataframe(
                    stats_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No duration data available")
        
        # Data preview
        st.markdown("---")
        st.subheader(" Data Preview")
        
        with st.expander("View filtered data", expanded=False):
            st.dataframe(
                filtered_data.head(100),
                use_container_width=True
            )
            st.caption(f"Showing first 100 of {len(filtered_data):,} trips")


if __name__ == "__main__":
    main()
