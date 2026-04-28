from pathlib import Path
import sys
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path: sys.path.insert(0, str(ROOT / "src"))
from app.utils.load_data import load_dashboard_data, normalize_duration_column

st.set_page_config(page_title="Station Usage", page_icon="📍", layout="wide")

@st.cache_data
def get_data(): return load_dashboard_data()
df = get_data(); duration_col = normalize_duration_column(df)

st.title("Station Usage Analysis")
st.markdown("This page identifies the stations with the highest trip volume and compares station-level demand intensity. This supports rebalancing, bike availability planning, and station performance monitoring.")
st.divider()

if "Start Station Name" not in df.columns:
    st.warning("Start Station Name column not available.")
    st.stop()

station = df.groupby("Start Station Name").agg(
    trips=("Start Station Name", "count"),
    median_duration=(duration_col, lambda s: s.median()/60),
    avg_duration=(duration_col, lambda s: s.mean()/60),
).reset_index().sort_values("trips", ascending=False)

total = station["trips"].sum()
station["trip_share_pct"] = station["trips"] / total * 100

c1,c2,c3 = st.columns(3)
c1.metric("Stations", f"{len(station):,}")
c2.metric("Top Station", station.iloc[0]["Start Station Name"])
c3.metric("Top Station Share", f"{station.iloc[0]['trip_share_pct']:.1f}%")

left,right = st.columns([2,1])
with left:
    fig = px.bar(station.head(15), x="trips", y="Start Station Name", orientation="h", title="Top 15 Start Stations by Trips", hover_data=["trip_share_pct", "median_duration"])
    fig.update_layout(yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.markdown("### Station Ranking")
    st.dataframe(station.head(15), use_container_width=True, hide_index=True)

fig = px.scatter(station, x="trips", y="median_duration", size="trip_share_pct", hover_name="Start Station Name", title="Station Volume vs Median Trip Duration")
st.plotly_chart(fig, use_container_width=True)
