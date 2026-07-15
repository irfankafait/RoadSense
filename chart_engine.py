from config import *
import pandas as pd

df = pd.read_csv(CLEANED_DATA_FILE)

# =====================================
# Chart 1: Accident Frequency by Hour
# =====================================

def get_hourly_frequency(df):
    """
    Accident count by hour.
    """

    hourly_df = (
        df.groupby('hour_of_day')
        .size()
        .reset_index(
            name='accident_count'
        )
        .sort_values(
            by='hour_of_day'
        )
    )

    return hourly_df
hourly_df = get_hourly_frequency(df)
print(hourly_df)


# =====================================
# Chart 2: Severity by Road Type
# =====================================


def get_severity_by_road_type(df):

    severity_df = (
        pd.crosstab(
            df['road_type'],
            df['severity']
        )
        .reset_index()
    )

    return severity_df

severity_df = get_severity_by_road_type(df)

print(severity_df)


# =====================================
# Chart 3: Monthly Trend
# =====================================

def get_monthly_trend(df):

    monthly_df = (
        df.groupby('month')
        .size()
        .reset_index(
            name='accident_count'
        )
        .sort_values(
            by='month'
        )
    )

    return monthly_df

monthly_df = get_monthly_trend(df)
print(monthly_df)

# =====================================
# Chart 4: Weather Analysis
# =====================================

def get_weather_summary(df):

    weather_df = (
        df.groupby(
            'weather_condition'
        )
        .size()
        .reset_index(
            name='accident_count'
        )
        .sort_values(
            by='accident_count',
            ascending=False
        )
    )

    return weather_df

weather_df = get_weather_summary(df)

print(weather_df)