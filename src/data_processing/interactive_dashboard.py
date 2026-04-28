"""
US09: Interactive Charts Final Dashboard

This Streamlit dashboard provides interactive visualizations for Toronto BikeShare data
with integrated reusable filter functions.

Features:
- Interactive date range, station, and user type filters
- Real-time KPI updates
- Multiple chart visualizations (line, bar, histogram, pie)
- Integration with reusable filter functions from utils.filters
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Setup project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Import reusable filter functions
from utils.filters import (
    filter_by_date_range,
    filter_by_start_station,
    filter_by_user_type
)

# Import analytics modules
from analytics.peak_usage import analyze_peak_usage
from analytics.station_usage import get_top_stations
from analytics.kpi_metrics import calculate_kpis


@st.cache_data
def generate_sample_data(num_rows=1000):
    """
    Generate sample bike sharing data for testing.
    Cached to avoid regenerating data on every interaction.
    
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
    
    # Generate dates over the past 30 days (vectorized)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    total_seconds = int((end_date - start_date).total_seconds())
    
    # Vectorized date generation
    random_seconds = np.random.randint(0, total_seconds, num_rows)
    dates = pd.to_datetime(start_date) + pd.to_timedelta(random_seconds, unit='s')
    
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
    
    # Calculate end times (vectorized)
    data['End Time'] = data['Start Time'] + pd.to_timedelta(data['Trip Duration '], unit='s')
    
    return data


# calculate_kpis function moved to analytics.kpi_metrics module
# Import with: from analytics.kpi_metrics import calculate_kpis

@st.cache_data(ttl=300)  # Cache for 5 minutes
def calculate_kpis_cached(data_hash, data):
    """Cached wrapper for calculate_kpis to improve performance."""
    return calculate_kpis(data)


def display_kpi_cards(kpis):
    """
    Display KPI cards in a row.
    
    Args:
        kpis (dict): Dictionary containing KPI values
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🚴 Total Trips",
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
            label="📍 Top Start Station",
            value=kpis['top_station'],
            delta=f"{kpis['top_station_trips']} trips",
            help="Station with the most trip starts"
        )


def create_visualizations(data):
    """
    Create interactive visualizations from the data.
    
    Args:
        data (pd.DataFrame): Filtered bike sharing data
    """
    if data.empty:
        st.warning("No data available for visualization")
        return
    
    st.subheader("📊 Interactive Visualizations")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Trips over time (Line chart)
        st.markdown("### 📈 Trips Over Time")
        if 'Start Time' in data.columns:
            # Use resample for better performance with large datasets
            trips_by_date = data.set_index('Start Time').resample('D').size()
            trips_by_date.index = trips_by_date.index.date
            fig, ax = plt.subplots(figsize=(10, 5))
            trips_by_date.plot(kind='line', ax=ax, color='red', linewidth=2, marker='o', markersize=6)
            
            # Find and label peak points
            peak_idx = trips_by_date.idxmax()
            peak_value = trips_by_date.max()
            ax.annotate(f'Peak: {peak_value}', 
                       xy=(peak_idx, peak_value),
                       xytext=(10, 10), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='black'))
            
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Number of Trips', fontsize=12)
            ax.set_title('Daily Trip Count', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        # Trip duration distribution (Histogram)
        st.markdown("### 📊 Trip Duration Distribution")
        duration_col = 'Trip Duration ' if 'Trip Duration ' in data.columns else 'Trip Duration'
        if duration_col in data.columns:
            fig, ax = plt.subplots(figsize=(10, 5.5))
            durations_min = data[duration_col].values / 60  # Convert to minutes with .values for speed
            # Use computed bins for better performance
            bin_count = min(30, len(data) // 10) if len(data) > 300 else 20
            ax.hist(durations_min, bins=bin_count, color='#2ca02c', alpha=0.7, edgecolor='black')
            ax.set_xlabel('Trip Duration (minutes)', fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.set_title('Distribution of Trip Durations', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
    
    with col2:
        # Top stations (Bar chart)
        st.markdown("### 🏆 Top 10 Stations")
        if 'Start Station Name' in data.columns:
            top_stations = get_top_stations(data, n=10)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(top_stations['Station Name'], top_stations['Trip Count'], color='#ff7f0e')
            ax.set_xlabel('Number of Trips', fontsize=12)
            ax.set_ylabel('Station', fontsize=12)
            ax.set_title('Top 10 Start Stations', fontsize=12, fontweight='bold')
            ax.invert_yaxis()
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
        
        # User type distribution (Pie chart)
        st.markdown("### 👥 User Type Distribution")
        if 'User Type' in data.columns:
            user_counts = data['User Type'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 5))
            
            # Assign colors based on user type
            color_map = {}
            for user_type in user_counts.index:
                if 'annual' in user_type.lower():
                    color_map[user_type] = 'orange'
                elif 'casual' in user_type.lower():
                    color_map[user_type] = 'green'
                else:
                    color_map[user_type] = 'gray'
            
            colors = [color_map[user_type] for user_type in user_counts.index]
            
            ax.pie(user_counts.values, labels=user_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90, textprops={'fontsize': 12})
            ax.set_title('Distribution by User Type', fontsize=14, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)


def create_distribution_charts(data):
    """
    Create hourly and weekday distribution charts.
    
    Args:
        data (pd.DataFrame): Filtered bike sharing data with Start Time column
    """
    if data.empty or 'Start Time' not in data.columns:
        st.warning("No data available for distribution charts")
        return
    
    # Analyze peak usage using the availability module (cached)
    @st.cache_data(ttl=300)
    def get_peak_analysis(data_hash):
        return analyze_peak_usage(data, datetime_col='Start Time')
    
    peak_analysis = get_peak_analysis(hash(str(len(data))))
    
    # Display hourly and weekday distribution charts
    col1, col2 = st.columns(2)
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    with col1:
        st.markdown("### 📊 Hourly Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plot bar chart
        hours_range = range(24)
        bars = ax.bar(hours_range, peak_analysis['hourly_counts'].values, color='steelblue', alpha=0.7)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=8, color='darkblue')
        
        # Add trend line (only if reasonable amount of data)
        if len(peak_analysis['hourly_counts']) >= 10:
            y_values = peak_analysis['hourly_counts'].values
            x_values = np.arange(len(y_values))
            z = np.polyfit(x_values, y_values, 3)  # 3rd degree polynomial
            p = np.poly1d(z)
            ax.plot(x_values, p(x_values), "r--", linewidth=2, label='Trend Line', alpha=0.8)
        
        ax.set_xlabel('Hour of Day', fontsize=11)
        ax.set_ylabel('Number of Trips', fontsize=11)
        ax.set_title('Trips by Hour', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    with col2:
        st.markdown("### 📅 Weekday Distribution")
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(range(7), peak_analysis['weekday_counts'].values, color='coral')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9, color='darkblue')
        
        ax.set_xlabel('Day of Week', fontsize=11)
        ax.set_ylabel('Number of Trips', fontsize=11)
        ax.set_title('Trips by Day', fontsize=12, fontweight='bold')
        ax.set_xticks(range(7))
        ax.set_xticklabels(days, rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


def create_heatmap_visualization(data):
    """
    Create heatmap visualization showing weekday versus hour usage.
    
    Args:
        data (pd.DataFrame): Filtered bike sharing data with Start Time column
    """
    if data.empty or 'Start Time' not in data.columns:
        st.warning("No data available for heatmap visualization")
        return
    
    st.subheader("🔥 Peak Usage Analysis - Heatmap")
    
    # Analyze peak usage using the availability module (cached)
    @st.cache_data(ttl=300)
    def get_heatmap_analysis(data_hash):
        return analyze_peak_usage(data, datetime_col='Start Time')
    
    peak_analysis = get_heatmap_analysis(hash(str(len(data))))
    
    # Display peak metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if peak_analysis['peak_hour'] is not None:
            st.metric(
                label="🕐 Peak Hour",
                value=f"{peak_analysis['peak_hour']:02d}:00",
                help="Hour with the highest trip count"
            )
        else:
            st.metric(label="🕐 Peak Hour", value="N/A")
    
    with col2:
        if peak_analysis['peak_day'] is not None:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            st.metric(
                label="📅 Peak Day",
                value=days[peak_analysis['peak_day']],
                help="Day of week with the highest trip count"
            )
        else:
            st.metric(label="📅 Peak Day", value="N/A")
    
    with col3:
        total_trips = int(peak_analysis['heatmap_matrix'].sum())
        st.metric(
            label="📊 Total Analyzed Trips",
            value=f"{total_trips:,}",
            help="Total trips in the heatmap"
        )
    
    # Create heatmap visualization
    import seaborn as sns
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Create heatmap
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = [f'{h:02d}' for h in range(24)]
    
    # Optimize heatmap rendering
    sns.heatmap(
        peak_analysis['heatmap_matrix'],
        annot=False,
        fmt='g',
        cmap='coolwarm',
        cbar_kws={'label': 'Trip Count'},
        xticklabels=hours,
        yticklabels=days,
        ax=ax,
        square=False,
        linewidths=0  # Remove gridlines for better performance
    )
    
    ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax.set_ylabel('Day of Week', fontsize=12, fontweight='bold')
    ax.set_title('Bike Usage Heatmap: Weekday vs Hour', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def apply_sidebar_filters(data):
    """
    Apply filters from sidebar using reusable filter functions.
    
    Args:
        data (pd.DataFrame): Input data
        
    Returns:
        pd.DataFrame: Filtered data
    """
    st.sidebar.title("🔧 Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Use view instead of copy for initial assignment (more memory efficient)
    filtered_data = data
    
    # Date range filter
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
    
    # Station filter
    if 'Start Station Name' in filtered_data.columns:
        st.sidebar.subheader("🚉 Station Filter")
        # Cache unique stations for performance
        @st.cache_data
        def get_unique_stations(data_hash):
            return sorted(data['Start Station Name'].unique())
        all_stations = get_unique_stations(hash(str(len(data))))
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
    
    # User type filter
    if 'User Type' in filtered_data.columns:
        st.sidebar.subheader("👤 User Type")
        user_types = list(data['User Type'].unique())  # Use original data for options
        selected_user_types = st.sidebar.multiselect(
            "Select user types:",
            options=user_types,
            default=user_types,
            help="Filter trips by user type"
        )
        
        if selected_user_types:
            # Use reusable filter function
            filtered_data = filter_by_user_type(
                filtered_data,
                user_types=selected_user_types,
                column='User Type'
            )
    
    # Display filter summary
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Filter Summary")
    st.sidebar.write(f"**Filtered Trips:** {len(filtered_data):,}")
    st.sidebar.write(f"**Total Trips:** {len(data):,}")
    st.sidebar.write(f"**Filter Rate:** {len(filtered_data)/len(data)*100:.1f}%")
    
    return filtered_data


def main():
    """Main dashboard application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Toronto BikeShare Analytics - US09",
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
        st.title("🚴 Toronto Bike-Share Interactive Analytics Dashboard")
    
    st.markdown("---")
    
    # Data source selection
    st.sidebar.subheader("📂 Data Source")
    data_source = st.sidebar.radio(
        "Choose data source:",
        options=["Sample Data", "Upload CSV"],
        help="Select whether to use generated sample data or upload your own CSV file"
    )
    
    # Load data
    if data_source == "Sample Data":
        st.sidebar.info("Using generated sample data for demonstration")
        num_samples = st.sidebar.slider(
            "Number of sample trips:",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100
        )
        data = generate_sample_data(num_rows=num_samples)
        st.success(f"✅ Generated {num_samples} sample trips")
    else:
        st.sidebar.info("Upload a CSV file with bike sharing data")
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
                data['Start Time'] = pd.to_datetime(data['Start Time'])
                st.success(f"✅ Loaded {len(data)} trips from uploaded file")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
                return
        else:
            st.info("Please upload a CSV file to continue")
            return
    
    st.markdown("---")
    
    # Apply filters using reusable filter functions
    filtered_data = apply_sidebar_filters(data)
    
    # Calculate KPIs on filtered data (with caching)
    data_hash = hash(str(len(filtered_data)) + str(filtered_data.columns.tolist()))
    kpis = calculate_kpis_cached(data_hash, filtered_data)
    
    # Display KPI cards
    st.subheader("📊 Key Performance Indicators")
    display_kpi_cards(kpis)
    
    st.markdown("---")
    
    # Display visualizations
    create_visualizations(filtered_data)
    
    st.markdown("---")
    
    # Additional statistics
    with st.expander("📈 Additional Statistics"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Trips per Day", f"{len(filtered_data)/30:.1f}")
        
        with col2:
            if 'User Type' in filtered_data.columns:
                annual_pct = (filtered_data['User Type'].str.contains('Annual', case=False).sum() / len(filtered_data) * 100)
                st.metric("Annual Member %", f"{annual_pct:.1f}%")
        
        with col3:
            if 'Start Station Name' in filtered_data.columns:
                unique_stations = filtered_data['Start Station Name'].nunique()
                st.metric("Unique Stations Used", f"{unique_stations}")
    
    st.markdown("---")
    
    # Display hourly and weekday distribution charts
    create_distribution_charts(filtered_data)
    
    st.markdown("---")
    
    # Display hourly peak usage heatmap
    create_heatmap_visualization(filtered_data)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Toronto BikeShare Analytics Dashboard | Powered By: Team 13 | "
        "Wilson Bli, Iyanuoluwa Bolaji, Olusola Adegbenga Ipoade, Roberto San Miguel | "
        "Msc. Data Analytics - University of Niagara Falls, Canada 2025"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    main()
