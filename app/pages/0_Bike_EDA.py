from pathlib import Path
import sys
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path: sys.path.insert(0, str(ROOT / "src"))
from app.utils.load_data import load_dashboard_data, normalize_duration_column

st.set_page_config(page_title="Bike EDA", page_icon="🔎", layout="wide")

st.markdown("""
<style>.banner{background:linear-gradient(135deg,#0f2440 0%,#1a3660 100%);border-left:5px solid #7B1FA2;border-radius:10px;padding:22px 28px;margin-bottom:18px}.banner p{color:#e8eaf0;line-height:1.7;margin:0}.banner .label{color:#f0c040;font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px}</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data(): return load_dashboard_data()
df = get_data()
duration_col = normalize_duration_column(df)

st.title("Exploratory Data Analysis")
st.markdown("""<div class="banner"><p class="label">EDA Summary</p><p>This page explores trip volume, duration distribution, daily trends, station usage, and rider composition. These patterns help explain operational demand before deeper station and user-type analysis.</p></div>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Filters")
    if "User Type" in df.columns:
        selected_users = st.multiselect("User Type", sorted(df["User Type"].dropna().unique()), default=list(sorted(df["User Type"].dropna().unique())))
        df = df[df["User Type"].isin(selected_users)]
    if "Start Station Name" in df.columns:
        stations = sorted(df["Start Station Name"].dropna().unique())
        selected_station = st.selectbox("Station Focus", ["All"] + stations)
        if selected_station != "All": df = df[df["Start Station Name"] == selected_station]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Trips", f"{len(df):,}")
c2.metric("Median Duration", f"{df[duration_col].median()/60:.1f} min")
c3.metric("Unique Start Stations", f"{df['Start Station Name'].nunique() if 'Start Station Name' in df.columns else 0:,}")
c4.metric("Bike Models", f"{df['Model'].nunique() if 'Model' in df.columns else 0:,}")

tab1, tab2, tab3 = st.tabs(["Time Trends", "Duration", "Data Preview"])
with tab1:
    if "Start Time" in df.columns:
        temp = df.copy(); temp["date"] = temp["Start Time"].dt.date
        daily = temp.groupby("date").size().reset_index(name="trips")
        fig = px.line(daily, x="date", y="trips", markers=True, title="Daily Trip Count")
        st.plotly_chart(fig, use_container_width=True)
    if "Start Station Name" in df.columns:
        top = df["Start Station Name"].value_counts().head(12).reset_index()
        top.columns = ["station", "trips"]
        fig = px.bar(top, x="trips", y="station", orientation="h", title="Top Start Stations")
        fig.update_layout(yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(fig, use_container_width=True)
with tab2:
    plot_df = df.copy(); plot_df["duration_min"] = plot_df[duration_col] / 60
    fig = px.histogram(plot_df, x="duration_min", nbins=40, title="Trip Duration Distribution")
    st.plotly_chart(fig, use_container_width=True)
    if "User Type" in df.columns:
        fig = px.box(plot_df, x="User Type", y="duration_min", title="Trip Duration by User Type")
        st.plotly_chart(fig, use_container_width=True)
with tab3:
    st.dataframe(df.head(200), use_container_width=True)
