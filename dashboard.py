
# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import plotly.express as px
import pandas as pd

from config import *
from roadsense_kpi_engine_v1 import *
from roadsense_chart_engine_v1 import *


# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(
    page_title='Traffic Accident Hotspot Reporter',
    page_icon='🚗',
    layout='wide'
)

st.title(
    'Traffic Accident Hotspot Reporter'
)


# ==========================================================
# Load Data (Cached)
# ==========================================================

@st.cache_data
def load_cleaned_data():
    return pd.read_csv(CLEANED_DATA_FILE)



@st.cache_data
def load_summary_metrics():
    return pd.read_csv(SUMMARY_METRICS_FILE)



@st.cache_data
def load_hotspot_ranking():
    return pd.read_csv(HOTSPOT_RANKING_FILE)



# ==========================================================
# Sidebar Filters
# ==========================================================

def create_sidebar_filters(df):
    st.sidebar.header('Filters')

# ==========================================================
# Apply Filters
# ==========================================================


    df['accident_date'] = pd.to_datetime(df['accident_date'])

    date_range = st.sidebar.date_input('Date Range',
        value=(
            df['accident_date'].min(),
            df['accident_date'].max()
        )
    )

    selected_severity = st.sidebar.multiselect(
            'Severity',
            options=df['severity'].dropna().unique(),
            default=df['severity'].dropna().unique()
    )

    selected_road_type = st.sidebar.multiselect(
            'Road Type',
            options=df['road_type'].dropna().unique(),
            default=df['road_type'].dropna().unique()
    )

    selected_weather = st.sidebar.multiselect(
            'Weather Condition',
            options=df['weather_condition'].dropna().unique(),
            default=df['weather_condition'].dropna().unique()
    )


    selected_zone = st.sidebar.multiselect(
            'Zone',
            options=df['zone'].dropna().unique(),
            default=df['zone'].dropna().unique()
    )

    return (
        date_range,
        selected_severity,
        selected_road_type,
        selected_weather,
        selected_zone
    )


def apply_filters(
        df,
        date_range,
    selected_severity,
    selected_road_type,
    selected_weather,
    selected_zone
):

    if isinstance(date_range, tuple):

        if len(date_range) == 2:
            start_date, end_date = date_range

        else:
            start_date = end_date = date_range[0]

    else:
        start_date = end_date = date_range

    filtered_df =df[
        (df['severity'].isin(selected_severity))
        &
        (df['road_type'].isin(selected_road_type))
        &
        (df['weather_condition'].isin(selected_weather))
        &
        (df['zone'].isin(selected_zone))
        &
        (
        df['accident_date'].dt.date.between(
            start_date,
            end_date
        )
    )
    ]
    return filtered_df

# ==========================================================
# KPI Cards
# ==========================================================

def display_kpi_cards(filtered_df):
    """
    Display KPI cards.
    """

    total_accidents = calculate_total_accidents(filtered_df)

    severe_accidents = calculate_severe_accidents(filtered_df)

    peak_hour = calculate_peak_hour(filtered_df)

    top_hotspot = calculate_top_hotspot(filtered_df)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:

        st.metric(
            label='Total Accidents',
            value=total_accidents
        )


    with col2:
        st.metric(
            'Severe Accidents',
            value=severe_accidents
        )        

    with col3:
        st.metric(
            label='Peak Hour',
            value=peak_hour
        )

    with col4:
        st.metric(
            label='Top Hotspot',
            value=top_hotspot
        )

# ==========================================================
# Charts
# ==========================================================

def display_charts(filtered_df):
    """
    Display all dashboard charts.
    """

    # Hourly Chart
    hourly_df = get_hourly_frequency(filtered_df)

    fig_hourly = px.bar(
        hourly_df,
        x='hour_of_day',
        y='accident_count',
        title='Accident Frequency by Hour'
    )

    # Severity Chart
    severity_df = (
        filtered_df
        .groupby(
            ['road_type', 'severity']
        )
        .size()
        .reset_index(
            name='accident_count'
        )
    )

    fig_severity = px.bar(
        severity_df,
        x='road_type',
        y='accident_count',
        color='severity',
        color_discrete_map={
            'Minor': '#0068c9',
            'Major': '#569bdb',
            'Critical' : "#f84141"
        },

        barmode='group',
        title='Severity by Road Type'
    )

    # Monthly Trend
    monthly_df = get_monthly_trend(filtered_df)

    fig_monthly = px.line(
        monthly_df,
        x='month',
        y='accident_count',
        markers=True,
        title='Monthly Accident Trend'
    )

    # Weather Chart
    weather_df = get_weather_summary(filtered_df)

    fig_weather = px.bar(
        weather_df,
        x='weather_condition',
        y='accident_count',
        title='Accident Count by Weather Condition'
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig_hourly,
            use_container_width=True,
            key='dashboard_chart_hourly'
        )

    with col2:
        st.plotly_chart(
            fig_severity,
            use_container_width=True,
            key='dashboard_chart_severity'
        )

    with col1:
        st.plotly_chart(
            fig_monthly,
            use_container_width=True,
            key='dashboard_chart_monthly'
        )

    with col2:
        st.plotly_chart(
            fig_weather,
            use_container_width=True,
            key='dashboard_chart_weather'
        )


# ==========================================================
# Hotspot Ranking Table
# ==========================================================


def display_hotspot_table(filtered_df):
    """
    Display hotspot ranking table.
    """

    st.subheader(
        "Hotspot Ranking"
    )

    hotspot_df = generate_hotspot_ranking(
        filtered_df
    )

    st.dataframe(
        hotspot_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# Download Reports
# ==========================================================


def display_download_buttons():
    """
    Display download buttons.
    """

    st.divider()

    st.header("Download Reports")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.download_button(
            label="📄 Download Cleaned Records",
            data=load_cleaned_data().to_csv(index=False),
            file_name="roadsense_cleaned_records_v1.csv",
            mime="text/csv"
        )

    with col2:

        st.download_button(
            label="📊 Download Summary Metrics",
            data=load_summary_metrics().to_csv(index=False),
            file_name="roadsense_summary_metrics_v1.csv",
            mime="text/csv"
        )

    with col3:

        st.download_button(
            label="📍 Download Hotspot Ranking",
            data=load_hotspot_ranking().to_csv(index=False),
            file_name="roadsense_hotspot_ranking_v1.csv",
            mime="text/csv"
        )     


def main():
    """
    Main Streamlit application.
    """

    try:
        df = load_cleaned_data()
    
    except FileNotFoundError:

        st.error(
            '❌ Cleaned data file not found.'
        )

        st.stop()

    (
        date_range,
        selected_severity,
        selected_road_type,
        selected_weather,
        selected_zone
    ) = create_sidebar_filters(df)

    filtered_df = apply_filters(
        df,
        date_range,
        selected_severity,
        selected_road_type,
        selected_weather,
        selected_zone
    )

    if filtered_df.empty:
        st.warning("No records found.")
        return

    display_kpi_cards(filtered_df)
    display_charts(filtered_df)
    display_hotspot_table(filtered_df)
    display_download_buttons()


if __name__ == "__main__":
    main()