from config import *
import pandas as pd

df = pd.read_csv(CLEANED_DATA_FILE)

print(df.shape)

df.head()

# KPI 1: Total Accidents

def calculate_total_accidents(df):
    """
    Return total accident records.
    """

    return len(df)

total_accidents = calculate_total_accidents(df)

print(
    f'Total Accidents: {total_accidents}'
)

# KPI 2: Severe Accidents

def calculate_severe_accidents(df):
    """
    Count Major and Critical accidents.
    """

    severe_df = df[
        df['severity']
        .isin(
            ['Major', 'Critical']
        )
    ]

    return len(severe_df)

severe_accidents = (
    calculate_severe_accidents(df)
)

print(
    f'Severe Accidents: '
    f'{severe_accidents}'
)


# KIP 3: Peak Hour

def calculate_peak_hour(df):
    """
    Return the hour with the highest accident count.
    """

    peak_hour = (
        df['hour_of_day']
        .mode()[0]
    )
    return peak_hour

peak_hour = calculate_peak_hour(df)


print(
    f'Accident in Peak Hours: '
    f'{peak_hour}'
)


# KPI 4: Top Hotspot

def calculate_top_hotspot(df):
    """
    Return Location with highest accident count.
    """
    top_hotspot = (
        df['location_name']
        .value_counts()
        .idxmax()
        )
    return top_hotspot
top_hotspot = calculate_top_hotspot(df)

print(
    f'Top Hotspot: '
    f'{top_hotspot}'
)

# KPI 5: Top Road Type

def calculate_top_road_type(df):
    """
    Return road type with the highest count. 
    """
    top_road_type = (
        df['road_type']
        .value_counts()
        .idxmax()
        )
    return top_road_type
top_road_type = calculate_top_road_type(df)

print(
    f'Top Road Type: '
    f'{top_road_type}'
)

# KPI 6: Top Weather Conditions

def calculate_top_weather_conditions(df):
    """
    Weather condition highest count
    """
    top_weather_condition = (
        df['weather_condition']
        .value_counts()
        .idxmax()
        )
    return top_weather_condition
top_weather_condition = calculate_top_weather_conditions(df)

print(
    f'Top Weather Condition: '
    f'{top_weather_condition}'
)


def generate_summary_metrics(df):

    summary_df = pd.DataFrame({
        'metric': [
            'Total Accidents',
            'Severe Accidents',
            'Peak Hour',
            'Top Hotspot',
            'Top Road Type',
            'Top Weather Condition'
        ],
        'value': [
            calculate_total_accidents(df),
            calculate_severe_accidents(df),
            calculate_peak_hour(df),
            calculate_top_hotspot(df),
            calculate_top_road_type(df),
            calculate_top_weather_conditions(df)
        ]
    })

    return summary_df

def export_summary_metrics(summary_df):

    summary_df.to_csv(
        SUMMARY_METRICS_FILE,
        index=False
    )

    print(
        f'Summary metrics exported:\n'
        f'{SUMMARY_METRICS_FILE}'
    )


def generate_hotspot_ranking(df):
    """
    Generate hotspot ranking with
    total accidents and severe accidents.
    """

    hotspot_df = (
        df.groupby(
            ["location_name", "zone"]
        )
        .agg(
            accident_count=(
                "accident_id",
                "count"
            ),
            severe_accident_count=(
                "severity",
                lambda x: x.isin(
                    ["Major", "Critical"]
                ).sum()
            )
        )
        .reset_index()
        .sort_values(
            by=[
                "accident_count",
                "severe_accident_count"
            ],
            ascending=False
        )
    )

    return hotspot_df
    

def export_hotspot_ranking(
        hotspot_df
    ):
        
    hotspot_df.to_csv(
        HOTSPOT_RANKING_FILE,
        index=False
    )

    print(
        f'Hotspot ranking exported:\n'
        f'{HOTSPOT_RANKING_FILE}'
        )

def run_kpi_engine():
    """
    Generate all KPI reports.
    """

    df = pd.read_csv(
        CLEANED_DATA_FILE
    )

    summary_df = generate_summary_metrics(df)

    export_summary_metrics(summary_df)

    hotspot_df = generate_hotspot_ranking(df)

    export_hotspot_ranking(hotspot_df)

    return (
        summary_df,
        hotspot_df
    )


if __name__ == "__main__":

    run_kpi_engine()