from pathlib import Path

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ==========================================================
# Data Folders
# ==========================================================

DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
EXTERNAL_DATA_DIR = DATA_DIR / 'external'
LOG_DIR = PROJECT_ROOT / 'logs'

# ==========================================================
# Application Folders
# ==========================================================

DOCS_DIR = PROJECT_ROOT / 'docs'


# Create folders if missing

for folder in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
    DOCS_DIR,
    LOG_DIR
    
]:
    
    folder.mkdir(
        parents=True,
        exist_ok=True
    )

# ==========================================================
# Data Files
# ==========================================================

RAW_DATA_FILE = (
    RAW_DATA_DIR /
    'roadsense_accident_records_raw_v1.csv'
)



CLEANED_DATA_FILE = (
    PROCESSED_DATA_DIR /
    'roadsense_cleaned_records_v1.csv'
)

SUMMARY_METRICS_FILE = (
    PROCESSED_DATA_DIR / 
    'roadsense_summary_metrics_v1.csv'
)

HOTSPOT_RANKING_FILE = (
    PROCESSED_DATA_DIR /
    'roadsense_hotspot_ranking_v1.csv'
)

files = [
    PROJECT_ROOT / 'logs/logger.py'
]

for file in files:
    file.touch(exist_ok=True)
