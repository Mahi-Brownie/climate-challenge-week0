import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Climate Challenge Dashboard", layout="wide")
st.title("🌍 African Climate Vulnerability Dashboard (2015-2026)")

# Load Data
@st.cache_data
def load_data():
    data_path = "data/"
    files = [f for f in os.listdir(data_path) if f.endswith("_clean.csv")]
    df_list = [pd.read_csv(os.path.join(data_path, f)) for f in files]
    return pd.concat(df_list)

try:
    df = load_data()
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar Filters
    st.sidebar.header("Filters")
    countries = st.sidebar.multiselect("Select Countries", options=df['Country'].unique(), default=df['Country'].unique())
    year_range = st.sidebar.slider("Select Year Range", 2015, 2026, (2015, 2026))

    # Filtered Data
    filtered_df = df[(df['Country'].isin(countries)) & (df['Date'].dt.year >= year_range[0]) & (df['Date'].dt.year <= year_range[1])]

    # Visuals
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Temperature Trends")
        fig_temp = px.line(filtered_df, x='Date', y='T2M', color='Country')
        st.plotly_chart(fig_temp, use_container_width=True)

    with col2:
        st.subheader("Precipitation Distribution")
        fig_rain = px.box(filtered_df, x='Country', y='PRECTOTCORR', color='Country')
        st.plotly_chart(fig_rain, use_container_width=True)

except Exception as e:
    st.error(f"Please ensure cleaned CSV files are in the 'data/' folder. Error: {e}")
