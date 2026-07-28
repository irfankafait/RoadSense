import pandas as pd
import pytest
from src.etl import ETLoader
from collections import namedtuple


class FakeDatabase:
       pass

def test_validate_columns_success():

    df = pd.DataFrame({

        'accident_date': [],
        'hour_of_day': [],
        'location': [],
        'zone': [],
        'weather': [],
        'severity': [],
        'road_type': [],
        'latitude': [],
        'longitude': [], # Why Empty Lists? This method only checks whether the columns exist.
    })

    etl = ETLoader(db=FakeDatabase())

    etl.validate_columns(df)


def test_validate_columns_missing_columns():

        df = pd.DataFrame({
              
              'location': [],
              'weather': []
        })

        etl = ETLoader(db=FakeDatabase())

        with pytest.raises(ValueError, match='Missing required columns'):
              etl.validate_columns(df)


def test_transform_row():
    
        etl = ETLoader(db=FakeDatabase())

        etl.locations = {
            "Lahore": 1
        }


        etl.zones = {
               "Central": 2
                }
        
        etl.weather = {
            "Rain": 3
        }


        etl.severity = {
            "High": 4
        }

        etl.road_types = {
            "Urban": 5
        }

        Row = namedtuple(
       'Row',
       [
              'accident_date',
              'hour_of_day',
              'location',
              'zone',
              'weather',
              'severity',
              'road_type',
              'latitude',
              'longitude'
       ]
)

        row = Row(
            accident_date="2025-01-01",
            hour_of_day=14,
            location="Lahore",
            zone="Central",
            weather="Rain",
            severity="High",
            road_type="Urban",
            latitude=31.5204,
            longitude=74.3587
        )


        result = etl.transform_row(row)

        assert result == (
            "2025-01-01",
            14,
            1,
            2,
            3,
            4,
            5,
            31.5204,
            74.3587
        )