from config import *
from logger import logger
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    'accident_id',
    'accident_date',
    'hour_of_day',
    'location',
    'zone',
    'road_type',
    'severity',
    'weather'
]


def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load accident CSV file.
    """

    try:
        df = pd.read_csv(file_path)

        logger.info('Dataset loaded successfully.')

        return df
    except Exception as e:

        raise Exception(
            f'Error loading file: {e}'
        )


def validate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate required columns.
    """

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f'Missing columns: {missing_columns}'
        )
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert accident_date
    to datetime.
    """

    df['accident_date'] = pd.to_datetime(
        df['accident_date'],
        errors='coerce'
    )

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate accident IDs.
    """
    before_rows = len(df)

    df = df.drop_duplicates(
        subset = 'accident_id'
    )

    after_rows = len(df)

    duplicated_removed = before_rows - after_rows

    logger.info(
        f'Removed {duplicated_removed} duplicate rows.'
    )

    return df


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values.
    """

    object_cols = df.select_dtypes(
        include='object'
    ).columns

    df[object_cols] = (
        df[object_cols].fillna('Unknown')
    )

    required_columns = [

        'accident_date',
        'hour_of_day'
    ]

    before = df[required_columns].isna().sum().sum()

    df[required_columns] = (

        df[required_columns].ffill().bfill()
    )

    after = df[required_columns].isna().sum().sum()

    logger.info(f'Filled {before - after} missing values in required columns.')

    return df



def clean_data(file_path: Path) -> pd.DataFrame:

    df = load_data(file_path)

    df = validate_columns(df)

    df = parse_dates(df)

    df = remove_duplicates(df)

    df = impute_missing_values(df)

    return df


def export_cleaned_data(df: pd.DataFrame) -> None:

    df.to_csv(
    CLEANED_DATA_FILE,
    index = False
    )

    logger.info(
        f'Cleaned data exported to {CLEANED_DATA_FILE}'
        )

def run_data_cleaning() -> pd.DataFrame:
    """
    Run complete data cleaning pipeline.
    """
    logger.info('Starting RoadSense data cleaning pipeline.')

    cleaned_df = clean_data(
        RAW_DATA_FILE
    )

    export_cleaned_data(
        cleaned_df
    )
    
    logger.info('RoadSense data cleaning pipeline completed successfully.')

    return cleaned_df



if __name__ == "__main__":
    cleaned_df = run_data_cleaning()
    
    print(
        cleaned_df.head()
        )

    cleaned_df.info()
