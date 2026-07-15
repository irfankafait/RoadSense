import pandas as pd
import pytest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


from config import *

from roadsense_data_cleaning_v1 import (
    load_data,
    validate_columns,
    parse_dates,
)

from roadsense_kpi_engine_v1 import (
    calculate_total_accidents,
    calculate_severe_accidents,
    calculate_peak_hour,
    calculate_top_hotspot,
)

# ==========================================================
# Test Data Loading
# ==========================================================

def test_load_data():

    df = load_data(
        RAW_DATA_FILE
    )

    assert isinstance(
        df,
        pd.DataFrame
    )

    assert not df.empty


# ==========================================================
# Test Required Columns
# ==========================================================

def test_validate_columns():

    df = load_data(
        RAW_DATA_FILE
    )

    validated_df = validate_columns(df)

    required_columns = [

        "accident_id",
        "accident_date",
        "hour_of_day",
        "location_name",
        "zone",
        "road_type",
        "severity",
        "weather_condition"

    ]

    for column in required_columns:

        assert column in validated_df.columns    


# ==========================================================
# Test Date Parsing
# ==========================================================

def test_parse_dates():

    df = load_data(
        RAW_DATA_FILE
    )

    df = parse_dates(df)

    assert pd.api.types.is_datetime64_any_dtype(
        df["accident_date"]
    )        

# ==========================================================
# KPI Tests
# ==========================================================

def test_total_accidents():

    df = pd.read_csv(
        CLEANED_DATA_FILE
    )

    total = calculate_total_accidents(df)

    assert total == len(df)

def test_severe_accidents():

    df = pd.read_csv(
        CLEANED_DATA_FILE
    )

    severe = calculate_severe_accidents(df)

    expected = len(
        df[
            df["severity"].isin(
                [
                    "Major",
                    "Critical"
                ]
            )
        ]
    )

    assert severe == expected

    
def test_peak_hour():

    df = pd.read_csv(
        CLEANED_DATA_FILE
    )

    peak = calculate_peak_hour(df)

    assert peak in df["hour_of_day"].unique()     


def test_top_hotspot():

    df = pd.read_csv(
        CLEANED_DATA_FILE
    )

    hotspot = calculate_top_hotspot(df)

    assert hotspot in df["location_name"].unique()           