# US09: Interactive Charts Final Dashboard - User Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Using Sidebar Filters](#using-sidebar-filters)
4. [Understanding KPIs](#understanding-kpis)
5. [Interactive Charts Guide](#interactive-charts-guide)
6. [Peak Usage Analysis](#peak-usage-analysis)
7. [Data Transformations](#data-transformations)
8. [Limitations & Known Issues](#limitations--known-issues)
9. [Technical Requirements](#technical-requirements)

---

## 🎯 Overview

The **Toronto Bike-Share Interactive Analytics Dashboard** is a comprehensive data visualization tool that provides real-time insights into bike-sharing usage patterns. Built with Streamlit and integrated with reusable filter functions, this dashboard allows users to explore trip data through multiple interactive visualizations.

**Key Features:**
- 🔧 Dynamic filtering by date range, station, and user type
- 📊 Real-time KPI calculations
- 📈 Six different chart types for comprehensive analysis
- 🔥 Advanced peak usage heatmap with hourly/weekday breakdown
- ⚡ Performance-optimized with caching for faster interactions

---

## 🚀 Getting Started

### Running the Dashboard

1. **Navigate to the project directory:**
   ```bash
   cd "Toronto-Bike-Sharing-Analytics-Tool"
   ```

2. **Run the Streamlit application:**
   ```bash
   python -m streamlit run src/data_processing/interactive_dashboard.py
   ```

3. **Access the dashboard:**
   - The dashboard will automatically open in your default browser
   - Default URL: `http://localhost:8502`
   - If it doesn't open automatically, copy the URL from the terminal

### Choosing Your Data Source

On first launch, you'll see two data source options in the sidebar:

#### Option 1: Sample Data (Default)
- **Best for:** Testing, demonstrations, or learning how the dashboard works
- **How it works:** Generates synthetic bike trip data with realistic patterns
- **Customization:** Use the slider to select between 100-5000 sample trips
- **Advantages:** No file needed, instant setup, consistent results

#### Option 2: Upload CSV
- **Best for:** Analyzing your own Toronto BikeShare datasets
- **Format requirements:**
  - CSV file format
  - Must contain these columns:
    - `Start Time` (datetime)
    - `Start Station Name` (text)
    - `Trip Duration` or `Trip Duration ` (numeric, in seconds)
    - `User Type` (text: "Annual Member" or "Casual Member")
- **How to upload:**
  1. Select "Upload CSV" radio button
  2. Click "Browse files"
  3. Select your CSV file
  4. Dashboard will automatically load and validate the data

---

## 🔧 Using Sidebar Filters

The sidebar contains powerful filtering tools that instantly update all visualizations. All filters work together (combined filtering).

### 1. Date Range Filter

**Purpose:** Filter trips that occurred within a specific time period.

**How to use:**
1. Click on the **"Start Date"** calendar picker
2. Select your desired start date
3. Click on the **"End Date"** calendar picker
4. Select your desired end date

**How it responds:**
- All charts and KPIs update immediately
- Only trips between start and end dates (inclusive) are shown
- Default range: Full dataset span

**Example use cases:**
- Compare summer vs. winter usage: Filter June-August vs. December-February
- Analyze specific events: Filter around holidays or special events
- Monthly analysis: Set both dates within the same month

---

### 2. Station Filter

**Purpose:** Focus analysis on specific bike stations.

**How to use:**
1. Locate the **"Filter by Start Station"** multiselect box
2. Click to open the dropdown menu
3. Search by typing station names
4. Select one or multiple stations
5. Selected stations appear as tags

**How it responds:**
- Shows only trips that started from selected stations
- If no stations selected, all stations are included
- KPIs recalculate based on filtered trips
- "Top 10 Stations" chart adjusts to show ranking among filtered data

**Example use cases:**
- Compare high-traffic vs. low-traffic stations
- Analyze specific neighborhoods or districts
- Study commuter hub usage patterns

**Tip:** Use Ctrl+Click (Windows) or Cmd+Click (Mac) to select multiple stations quickly.

---

### 3. User Type Filter

**Purpose:** Analyze behavior differences between user types.

**How to use:**
1. Locate the **"Filter by User Type"** multiselect box
2. Click to see available user types:
   - Annual Member (regular subscribers)
   - Casual Member (pay-per-use riders)
3. Select one or both types

**How it responds:**
- All visualizations filter to show only selected user types
- User Type Distribution pie chart updates percentages
- KPIs reflect filtered user behavior
- If no selection, all users are included

**Example use cases:**
- Compare subscriber vs. casual rider patterns
- Analyze different usage behaviors (commuters vs. tourists)
- Calculate membership conversion opportunities

---

### Filter Summary

At the bottom of the sidebar, you'll see:
- **Filtered Trips:** Number of trips after applying all filters
- **Total Trips:** Original dataset size
- **Filter Rate:** Percentage of data currently displayed

**Understanding Filter Rate:**
- 100% = No active filters (showing all data)
- 50% = Half of trips match your filter criteria
- 0% = No trips match (try adjusting filters)

---

## 📊 Understanding KPIs

### Key Performance Indicators appear at the top of the dashboard in three cards:

### 🚴 Total Trips
**What it shows:** Total number of bike trips in the filtered dataset.

**How to interpret:**
- Higher numbers indicate more activity
- Compare across different filters to identify trends
- Seasonal variations are normal (higher in summer)

**Example insights:**
- "Annual Members made 7,200 trips vs. 3,800 casual trips"
- "Union Station generated 1,500 trips in July"

---

### ⏱️ Median Trip Duration
**What it shows:** The middle value of all trip durations (in minutes).

**Why median, not average?**
- Median is less affected by extreme values (very long or very short trips)
- Better represents typical user behavior
- More stable metric for comparison

**How to interpret:**
- 10-20 minutes: Short commuter trips
- 20-40 minutes: Leisure or intermediate trips
- 40+ minutes: Long recreational rides

**Example insights:**
- "Casual members ride 35% longer than annual members"
- "Weekend trips average 12 minutes longer"

---

### 📍 Top Start Station
**What it shows:** The station with the most trip starts and its trip count.

**How to interpret:**
- Identifies highest-demand locations
- Delta value shows exact trip count
- Useful for capacity planning
- May vary significantly with filters

**Example insights:**
- "Union Station is the busiest with 450 trips"
- "Top station changes from Union Station (weekdays) to Harbourfront (weekends)"

---

## 📈 Interactive Charts Guide

### 1. 📈 Trips Over Time (Line Chart)

**Location:** Top-left quadrant

**What it shows:** Daily trip counts over the filtered time period.

**Visual elements:**
- **Red line:** Daily trip trend
- **Circle markers:** Each data point represents one day
- **Yellow annotation:** Peak day with exact trip count

**How to interpret:**
- **Upward trends:** Growing usage over time
- **Downward trends:** Declining usage
- **Spikes:** High-activity days (weekends, events, good weather)
- **Dips:** Low-activity days (poor weather, holidays)

**Interactions:**
- Hover to see exact values (if interactive mode enabled)
- Rotated x-axis labels for readability

**Example insights:**
- "Usage peaks on Friday with 350 trips"
- "Weather event caused 60% drop on March 15"
- "Consistent growth of 5% per week"

---

### 2. 🏆 Top 10 Stations (Horizontal Bar Chart)

**Location:** Top-right quadrant

**What it shows:** The 10 busiest start stations ranked by trip count.

**Visual elements:**
- **Orange bars:** Trip count for each station
- **Inverted Y-axis:** #1 station at top
- **Grid lines:** Help read exact values

**How to interpret:**
- Longer bars = more trips
- Compare relative popularity between stations
- Identify high-demand locations
- Note: Ranking may change dramatically with filters

**Example insights:**
- "Top 3 stations account for 45% of all trips"
- "Union Station has 3x more trips than average"
- "Tourist areas dominate weekend rankings"

---

### 3. 📊 Trip Duration Distribution (Histogram)

**Location:** Bottom-left of first section

**What it shows:** Frequency distribution of trip lengths (converted to minutes).

**Visual elements:**
- **Green bars:** Number of trips in each duration bucket
- **30 bins:** Duration range divided into 30 equal intervals
- **Semi-transparent:** Alpha = 0.7 for better visibility

**How to interpret:**
- **Peak position:** Most common trip duration
- **Shape:** Normal (bell-shaped), right-skewed, or multi-modal
- **Spread:** Variation in riding behavior
- **Long tail:** Presence of outlier trips

**Example insights:**
- "Most trips last 10-15 minutes"
- "Casual members show bimodal distribution (short + long trips)"
- "Very few trips exceed 60 minutes"

---

### 4. 👥 User Type Distribution (Pie Chart)

**Location:** Bottom-right of first section

**What it shows:** Percentage breakdown of trips by user type.

**Visual elements:**
- **Orange slice:** Annual Member trips
- **Green slice:** Casual Member trips
- **Percentages:** Auto-calculated proportions
- **Matched sizing:** Same dimensions as Trip Duration chart (10x5)

**How to interpret:**
- Larger slice = more trips from that user type
- Percentages always sum to 100%
- Changes dynamically with filters

**Example insights:**
- "70% Annual Members, 30% Casual Members"
- "Weekend usage shifts to 55% casual members"
- "Harbourfront station: 80% casual members (tourist area)"

---

### 5. 📊 Hourly Distribution (Bar Chart with Trend Line)

**Location:** Left side of distribution section

**What it shows:** Trip counts aggregated by hour of day (0-23).

**Visual elements:**
- **Blue bars (alpha=0.7):** Trip count for each hour
- **Red dashed line:** 3rd-degree polynomial trend line
- **Deep blue labels:** Exact trip count on each bar
- **Legend:** Identifies trend line

**How to interpret:**
- **Peak hours:** Identify rush hours or high-activity periods
- **Trend line:** Shows overall daily pattern (smooth curve)
- **Dual peaks:** Typical commuter pattern (8am & 5pm)
- **Single peak:** Leisure pattern (midday)

**Example insights:**
- "Morning rush: 7-9am, Evening rush: 4-6pm"
- "Casual members peak at 2pm (lunch/leisure)"
- "Annual members show clear commute pattern"

---

### 6. 📅 Weekday Distribution (Bar Chart)

**Location:** Right side of distribution section

**What it shows:** Trip counts aggregated by day of week (Monday-Sunday).

**Visual elements:**
- **Coral bars:** Trip count for each day
- **Deep blue labels:** Exact trip count on each bar
- **Rotated labels:** 45-degree angle for readability

**How to interpret:**
- **Weekday vs. weekend:** Compare work days vs. leisure days
- **Monday effect:** Often lower after weekend
- **Friday peak:** Often highest weekday usage
- **Weekend patterns:** Saturday may differ from Sunday

**Example insights:**
- "Wednesday is busiest weekday (commuter pattern)"
- "Saturday has 40% more trips than Monday"
- "Sunday shows gradual decline (return-to-work anticipation)"

---

## 🔥 Peak Usage Analysis

### Location: Bottom of dashboard (after Additional Statistics)

### Heatmap Visualization

**What it shows:** Trip density across weekdays (rows) and hours (columns).

**Visual elements:**
- **Coolwarm colormap:**
  - Blue shades = Low activity
  - Red shades = High activity
- **7 rows:** Mon, Tue, Wed, Thu, Fri, Sat, Sun
- **24 columns:** Hours 00-23
- **Color bar:** Trip count legend on the right

**How to interpret:**
- **Dark red cells:** Peak usage times (most trips)
- **Dark blue cells:** Low usage times (few trips)
- **Pattern recognition:**
  - Commuter pattern: Red at 8am & 5pm on weekdays
  - Leisure pattern: Red during midday on weekends
  - Night pattern: Blue across all days (low usage)

**Example insights:**
- "Tuesday 5pm: 450 trips (peak hour)"
- "Sunday 3am: 5 trips (lowest usage)"
- "Weekend pattern shifts 2 hours later than weekdays"

---

### Peak Metrics (3 KPI Cards)

Located above the heatmap:

#### 🕐 Peak Hour
- **Format:** HH:00 (24-hour format)
- **Meaning:** Hour with highest trip count across all days
- **Example:** "17:00" = 5pm rush hour

#### 📅 Peak Day
- **Format:** Day name (Monday-Sunday)
- **Meaning:** Day of week with highest trip count
- **Example:** "Wednesday" = Mid-week commuter surge

#### 📊 Total Analyzed Trips
- **Format:** Comma-separated number
- **Meaning:** Sum of all trips in the heatmap
- **Use:** Verify data completeness

---

## 🔄 Data Transformations

### Understanding How Data is Processed

#### 1. Date/Time Conversions
- **Input:** `Start Time` column (string or datetime)
- **Process:** Converted to pandas datetime using `pd.to_datetime()`
- **Derived fields:**
  - `Start Time.dt.date` → Used for daily aggregation
  - `Start Time.dt.hour` → Used for hourly analysis (0-23)
  - `Start Time.dt.dayofweek` → Used for weekday analysis (0=Monday)

#### 2. Duration Calculations
- **Input:** `Trip Duration` or `Trip Duration ` (in seconds)
- **Process:** Divided by 60 to convert to minutes
- **Used for:** Median duration KPI, histogram distribution
- **Clipping:** Sample data clips durations between 5 min - 2 hours

#### 3. Aggregations

**Daily Aggregation:**
```python
trips_by_date = data.groupby(data['Start Time'].dt.date).size()
```
- Groups all trips by date
- Counts trips per day
- Used in "Trips Over Time" chart

**Station Aggregation:**
```python
top_stations = data['Start Station Name'].value_counts().nlargest(10)
```
- Counts trips per station
- Selects top 10 by count
- Used in "Top 10 Stations" chart

**Hourly/Weekday Matrix:**
- Creates 7×24 matrix (weekday × hour)
- Each cell = trip count for that day-hour combination
- Used in heatmap visualization

#### 4. Filter Applications

Filters are applied sequentially using reusable functions:

1. **Date Range Filter:**
   ```python
   data = data[(data['Start Time'] >= start_date) & (data['Start Time'] <= end_date)]
   ```

2. **Station Filter:**
   ```python
   data = data[data['Start Station Name'].isin(selected_stations)]
   ```

3. **User Type Filter:**
   ```python
   data = data[data['User Type'].isin(selected_types)]
   ```

All visualizations use the **filtered dataset** after all transformations.

---

## ⚠️ Limitations & Known Issues

### Data Limitations

#### 1. Sample Data Constraints
- **Synthetic data:** Generated patterns may not reflect real-world complexity
- **Fixed seed:** Same random seed produces identical results
- **Station probabilities:** Weighted distribution may not match actual Toronto BikeShare
- **30-day span:** Limited to past 30 days from current date
- **No weather data:** Cannot correlate with actual weather events

#### 2. CSV Upload Requirements
- **Required columns:** Must contain all mandatory columns
- **Date format:** `Start Time` must be parseable by pandas
- **Encoding:** UTF-8 recommended for special characters
- **File size:** Large files (>50MB) may cause performance issues
- **Memory:** Dashboard loads entire file into memory

#### 3. Performance Considerations
- **Large datasets:** 100,000+ trips may cause slow rendering
- **Complex filters:** Multiple filters increase processing time
- **Chart rendering:** Matplotlib plots take 1-2 seconds each
- **Browser limits:** Some older browsers may struggle with large datasets

### Visualization Limitations

#### 1. Line Chart (Trips Over Time)
- **Peak annotation:** Only shows single highest peak
- **Multiple peaks:** Secondary peaks not labeled
- **Date gaps:** Missing dates appear as gaps in line
- **X-axis crowding:** Many data points cause label overlap

#### 2. Histogram (Trip Duration)
- **Bin count:** Fixed at 30 bins (not adjustable)
- **Outliers:** Very long trips may compress main distribution
- **Resolution:** May miss subtle patterns in specific duration ranges

#### 3. Heatmap
- **Color scale:** Fixed colormap (coolwarm) may not suit all preferences
- **Cell annotations:** No value labels on cells (by design for clarity)
- **Empty cells:** Zero-trip cells may not be visually distinct

#### 4. All Charts
- **Static images:** Charts are matplotlib figures, not fully interactive
- **No zoom:** Cannot zoom into specific regions
- **No tooltips:** Hover interactions limited
- **Export:** No built-in export to PDF/PNG (use browser print)

### Known Issues

#### 1. Date Filter Edge Cases
- **Timezone handling:** Assumes local timezone, may cause 1-day offset
- **Midnight trips:** Trips at exactly 00:00:00 may be excluded
- **Date range validation:** No error if end date < start date (returns empty data)

#### 2. Station Filter
- **Case sensitivity:** Station names must match exactly
- **Whitespace:** Leading/trailing spaces may cause mismatches
- **Special characters:** Some station names with accents may not display correctly

#### 3. User Type Filter
- **Naming variations:** Only recognizes "Annual Member" and "Casual Member"
- **Custom types:** Other user types appear as "gray" in pie chart
- **Empty selection:** Selecting zero types shows all types (may be confusing)

#### 4. KPI Calculations
- **Median duration:** Returns 0 if duration column missing (should show N/A)
- **Top station:** May show "N/A" with valid data if station names are null
- **Division by zero:** Filter rate calculation fails if total trips = 0

#### 5. Caching Issues
- **Stale cache:** Cached data persists even if source file changes
- **Clear cache:** Must manually clear Streamlit cache (C key in browser)
- **Parameter sensitivity:** Cache may not invalidate when filter order changes

### Workarounds

**For large datasets:**
- Pre-filter data before uploading (e.g., specific date range in Excel)
- Use sample data slider to test with smaller datasets first
- Close other browser tabs to free memory

**For missing data:**
- Check CSV column names match exactly
- Remove or replace null values before uploading
- Ensure date format is consistent (YYYY-MM-DD HH:MM:SS)

**For performance:**
- Start with "Sample Data" to verify dashboard works
- Gradually increase sample size to find optimal performance
- Use fewer filters simultaneously
- Refresh browser if dashboard becomes unresponsive

---

## 🛠️ Technical Requirements

### System Requirements
- **Python Version:** 3.8 or higher
- **RAM:** Minimum 4GB (8GB recommended for large datasets)
- **Browser:** Modern browser (Chrome, Firefox, Edge, Safari)
- **Internet:** Required for initial package downloads

### Required Python Packages
```
streamlit >= 1.28.0
pandas >= 2.0.0
numpy >= 1.24.0
matplotlib >= 3.7.0
seaborn >= 0.12.0
```

### Optional Dependencies
- `openpyxl` - For Excel file uploads (future feature)
- `plotly` - For interactive charts (future enhancement)

### Installation

1. **Install dependencies:**
   ```bash
   pip install streamlit pandas numpy matplotlib seaborn
   ```

2. **Verify installation:**
   ```bash
   python -m streamlit --version
   ```

3. **Run dashboard:**
```bash
streamlit run src/data_processing/interactive_dashboard.py
```---

## 📞 Support & Contact

**Development Team:**
- Wilson Bli
- Iyanuoluwa Bolaji
- Olusola Adegbenga Ipoade
- Roberto San Miguel

**Institution:** University of Niagara Falls, Canada  
**Program:** MSc. Data Analytics  
**Year:** 2025

**Repository:** [Toronto-Bike-Sharing-Analytics-Tool](https://github.com/Iyanu0612/Toronto-Bike-Sharing-Analytics-Tool)

---

## 📝 Version History

- **v1.0** - Initial release with 6 charts and 3 KPIs
- **v1.1** - Added peak usage heatmap analysis
- **v1.2** - Implemented performance caching
- **v1.3** - Enhanced chart customizations (colors, labels, trend lines)

*Last Updated: December 4, 2025*