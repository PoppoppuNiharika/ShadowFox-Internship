import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page settings
st.set_page_config(
    page_title="Delhi AQI Dashboard",
    layout="wide"
)

# Light Yellow + Purple Theme
st.markdown("""
<style>
body {
    background-color: #fffdf5;
}

.main {
    background: linear-gradient(to right, #fffdf5, #f8f0ff);
}

h1 {
    color: #6a0dad;
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

h2, h3 {
    color: #7b2cbf;
}

[data-testid="stMetricValue"] {
    color: #6a0dad;
}

div.block-container {
    padding-top: 2rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 18px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #fff3b0;
    border-radius: 12px;
    padding: 12px;
    color: #4b0082;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    background-color: #d8b4fe;
    color: #4b0082;
}

.stButton>button {
    background-color: #ffe066;
    color: #4b0082;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

.stDownloadButton>button {
    background-color: #ffe066;
    color: #4b0082;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
data = pd.read_csv("dataset.csv")
data["date"] = pd.to_datetime(data["date"])

# Title
st.title("🌸 Delhi Air Quality Analysis Dashboard")

st.write(
    "Analyze Delhi’s pollution trends, station-wise AQI, seasonal changes, and pollutant relationships."
)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Home",
    "📂 Dataset",
    "📊 Statistics",
    "📈 Trends",
    "🏢 Stations",
    "🌦 Seasons",
    "🔥 Heatmap"
])

# HOME
with tab1:
    st.subheader("Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average AQI", round(data["aqi"].mean(), 2))

    with col2:
        st.metric("Highest AQI", data["aqi"].max())

    with col3:
        st.metric("Lowest AQI", data["aqi"].min())

    with col4:
        st.metric("Total Stations", data["station"].nunique())

# DATASET
with tab2:
    st.subheader("Dataset Preview")
    st.write(data.head())

    st.download_button(
        "⬇ Download Dataset",
        data.to_csv(index=False),
        "delhi_aqi.csv"
    )

# STATISTICS
with tab3:
    st.subheader("AQI Statistics")
    st.write(data["aqi"].describe())

    st.subheader("Highest AQI Record")
    st.write(data.loc[data["aqi"].idxmax()])

    st.subheader("Lowest AQI Record")
    st.write(data.loc[data["aqi"].idxmin()])

# TRENDS
with tab4:
    st.subheader("Monthly AQI Trend")

    trend = data.groupby("date")["aqi"].mean().resample("ME").mean()

    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(trend.index, trend.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("AQI Category Distribution")

    category_count = data["aqi_category"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 2))
    ax.bar(category_count.index, category_count.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# STATIONS
with tab5:
    st.subheader("Station-wise Analysis")

    station = st.selectbox(
        "Select Station",
        data["station"].unique()
    )

    filtered_data = data[data["station"] == station]

    st.write(filtered_data.head())

    station_data = data.groupby("station")["aqi"].mean().sort_values(
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(6, 2))
    ax.bar(station_data.index, station_data.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# SEASONS
with tab6:
    st.subheader("Season-wise AQI")

    season_data = data.groupby("season")["aqi"].mean()

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.bar(season_data.index, season_data.values)
    st.pyplot(fig)

# HEATMAP
with tab7:
    st.subheader("Pollutant Correlation Heatmap")

    pollutants = data[["pm25", "pm10", "no2", "so2", "co", "o3"]]

    fig, ax = plt.subplots(figsize=(5, 2))
    sns.heatmap(
        pollutants.corr(),
        annot=True,
        cmap="coolwarm"
    )

    st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Built using Streamlit, Pandas, Matplotlib & Seaborn")