"""Home page for Toronto Bike Sharing Analytics Dashboard."""
from pathlib import Path
import sys
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from app.utils.load_data import load_dashboard_data, normalize_duration_column

st.set_page_config(page_title="Toronto Bike Sharing Analytics", page_icon="🚲", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.tip-title {display:flex;align-items:center;margin-bottom:.4rem}.tip-title h2{margin:0;font-size:1.5rem;font-weight:700}.tip-title h3{margin:0;font-size:1.35rem;font-weight:600}.tip{position:relative;display:inline-flex;cursor:help;margin-left:10px}.tip-icon{font-size:.9rem;color:#888}.tip-box{visibility:hidden;opacity:0;width:380px;background:rgba(28,28,44,.97);color:#e4e4f0;text-align:left;border-radius:8px;padding:14px 18px;font-size:.95rem;line-height:1.65;position:absolute;z-index:9999;bottom:calc(100% + 10px);left:50%;transform:translateX(-50%);transition:opacity .2s;box-shadow:0 6px 24px rgba(0,0,0,.45);pointer-events:none}.tip-box::after{content:"";position:absolute;top:100%;left:50%;margin-left:-6px;border:6px solid transparent;border-top-color:rgba(28,28,44,.97)}.tip:hover .tip-box{visibility:visible;opacity:1}.step-badge{background:#f0f4ff;border-radius:6px;padding:8px 14px;margin-bottom:8px;font-size:.75rem;font-weight:700;color:#2c5282;letter-spacing:.08em}
</style>
""", unsafe_allow_html=True)


def tip_header(label, text, level=3):
    html = text.replace("**", "")
    st.markdown(f'<div class="tip-title"><h{level}>{label}</h{level}><span class="tip"><span class="tip-icon">ℹ️</span><span class="tip-box">{html}</span></span></div>', unsafe_allow_html=True)


@st.cache_data
def get_data():
    return load_dashboard_data()


df = get_data()
duration_col = normalize_duration_column(df)
trips = len(df)
median_min = df[duration_col].median() / 60
avg_min = df[duration_col].mean() / 60
top_station = df["Start Station Name"].mode().iloc[0] if "Start Station Name" in df.columns else "N/A"
member_share = (df["User Type"].eq("Annual Member").mean() * 100) if "User Type" in df.columns else 0

st.title("Toronto Bike Sharing Analytics Dashboard")
st.markdown("""
This dashboard explores bike-sharing trip patterns, station demand, user type behavior, trip duration, and operational KPIs. It is structured as a portfolio-ready analytics project with reusable Python modules, tests, reports, and an interactive Streamlit interface.
""")

st.markdown("""
<div style="background: linear-gradient(135deg, #0f2440 0%, #1a3660 100%); border-left: 5px solid #4CAF50; border-radius: 10px; padding: 22px 28px; margin-bottom: 8px;">
<p style="color:#f0c040;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin:0 0 10px 0;">Executive Summary</p>
<p style="color:#e8eaf0;font-size:1rem;line-height:1.75;margin:0;">Bike-sharing demand is shaped by station location, rider type, trip duration, and time-based usage patterns. This dashboard translates trip-level records into operational KPIs that can support station planning, availability monitoring, and service improvement.</p>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Trips", f"{trips:,}")
c2.metric("Median Duration", f"{median_min:.1f} min")
c3.metric("Average Duration", f"{avg_min:.1f} min")
c4.metric("Annual Member Share", f"{member_share:.1f}%")

st.divider()

tab1, tab2, tab3 = st.tabs(["Project Scope", "Dashboard Preview", "Repository Structure"])
with tab1:
    tip_header("Business Problem", "Operators need to understand where and when bike demand occurs so they can improve station availability and rider experience.", 3)
    st.markdown("""
- Identify high-demand stations
- Compare annual and casual member behavior
- Monitor trip duration patterns
- Support rebalancing and operational planning
- Convert raw trip data into dashboard-ready KPIs
""")
    tip_header("Core Analytics Modules", "The repository includes modular Python functions for loading, cleaning, deriving features, calculating KPIs, and visualizing usage patterns.", 3)
    st.markdown("""
- `src/data_processing`: loading, cleaning, filtering, and dashboard preparation
- `src/analytics`: KPI, station usage, peak usage, trip duration, and user-type modules
- `src/visualization`: reusable chart generation
- `tests`: unit tests for reliability
""")
with tab2:
    left,right = st.columns(2)
    with left:
        if "User Type" in df.columns:
            user_counts = df["User Type"].value_counts().reset_index()
            user_counts.columns = ["User Type", "Trips"]
            fig = px.pie(user_counts, names="User Type", values="Trips", title="Trip Share by User Type")
            st.plotly_chart(fig, use_container_width=True)
    with right:
        if "Start Station Name" in df.columns:
            top = df["Start Station Name"].value_counts().head(10).reset_index()
            top.columns = ["Station", "Trips"]
            fig = px.bar(top, x="Trips", y="Station", orientation="h", title="Top Start Stations")
            fig.update_layout(yaxis={"categoryorder":"total ascending"})
            st.plotly_chart(fig, use_container_width=True)
with tab3:
    st.code("""toronto-bike-sharing-analytics/
├── app/
├── src/
├── data/
├── figures/
├── reports/
├── tests/
├── examples/
├── requirements.txt
└── README.md""", language="text")
