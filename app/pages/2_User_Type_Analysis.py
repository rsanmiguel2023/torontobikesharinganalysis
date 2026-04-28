from pathlib import Path
import sys
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path: sys.path.insert(0, str(ROOT / "src"))
from app.utils.load_data import load_dashboard_data, normalize_duration_column

st.set_page_config(page_title="User Type Analysis", page_icon="👥", layout="wide")

@st.cache_data
def get_data(): return load_dashboard_data()
df = get_data(); duration_col = normalize_duration_column(df)

st.title("User Type Analysis")
st.markdown("This page compares annual and casual member behavior to identify differences in trip volume, trip duration, station preferences, and operational usage patterns.")
st.divider()

if "User Type" not in df.columns:
    st.warning("User Type column not available.")
    st.stop()

summary = df.groupby("User Type").agg(
    trips=("User Type", "count"),
    median_duration_min=(duration_col, lambda s: s.median()/60),
    avg_duration_min=(duration_col, lambda s: s.mean()/60),
).reset_index()
summary["trip_share_pct"] = summary["trips"] / summary["trips"].sum() * 100

c1,c2,c3 = st.columns(3)
c1.metric("User Types", f"{summary.shape[0]}")
c2.metric("Largest Segment", summary.sort_values("trips", ascending=False).iloc[0]["User Type"])
c3.metric("Largest Segment Share", f"{summary['trip_share_pct'].max():.1f}%")

left,right = st.columns(2)
with left:
    fig = px.pie(summary, names="User Type", values="trips", title="Trip Share by User Type")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.bar(summary, x="User Type", y="median_duration_min", title="Median Trip Duration by User Type")
    st.plotly_chart(fig, use_container_width=True)

plot_df = df.copy(); plot_df["duration_min"] = plot_df[duration_col]/60
fig = px.box(plot_df, x="User Type", y="duration_min", points=False, title="Trip Duration Distribution by User Type")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(summary, use_container_width=True, hide_index=True)
