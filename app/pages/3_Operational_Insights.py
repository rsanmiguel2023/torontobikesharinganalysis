from pathlib import Path
import sys
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path: sys.path.insert(0, str(ROOT / "src"))
from app.utils.load_data import load_dashboard_data, normalize_duration_column

st.set_page_config(page_title="Operational Insights", page_icon="🧭", layout="wide")

@st.cache_data
def get_data(): return load_dashboard_data()
df = get_data(); duration_col = normalize_duration_column(df)

st.title("Operational Insights and Recommendations")
st.markdown("This page translates analytical outputs into practical recommendations for bike-share operations, station monitoring, and customer experience improvement.")
st.divider()

if "Start Time" in df.columns:
    temp = df.copy(); temp["hour"] = temp["Start Time"].dt.hour
    hourly = temp.groupby("hour").size().reset_index(name="trips")
    peak_hour = int(hourly.loc[hourly["trips"].idxmax(), "hour"])
else:
    hourly = None; peak_hour = None

top_station = df["Start Station Name"].value_counts().idxmax() if "Start Station Name" in df.columns else "N/A"

c1,c2,c3 = st.columns(3)
c1.metric("Peak Hour", f"{peak_hour}:00" if peak_hour is not None else "N/A")
c2.metric("Highest Demand Station", top_station)
c3.metric("Median Trip", f"{df[duration_col].median()/60:.1f} min")

if hourly is not None:
    fig = px.bar(hourly, x="hour", y="trips", title="Trips by Hour of Day")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Recommendations")
st.markdown("""
1. Prioritize bike rebalancing around high-volume start stations.  
2. Monitor peak-hour demand to reduce empty or full station issues.  
3. Segment communications and pricing by annual vs casual member behavior.  
4. Use trip duration outliers to flag possible operational or data-quality issues.  
5. Track KPI trends regularly using the dashboard to support service planning.  
""")

st.markdown("### Portfolio Interpretation")
st.markdown("This project demonstrates how a city mobility dataset can be converted into a reusable analytics product. The final structure supports maintainable code, automated tests, interactive reporting, and business-focused recommendations.")
