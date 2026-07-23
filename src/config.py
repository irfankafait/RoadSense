from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

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
SQL_DIR = PROJECT_ROOT / 'sql'


# Create folders if missing

for folder in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    EXTERNAL_DATA_DIR,
    DOCS_DIR,
    LOG_DIR,
    SQL_DIR
    
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
    'raw_accidents.csv'
)



CLEANED_DATA_FILE = (
    PROCESSED_DATA_DIR /
    'cleaned_accidents.csv'
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
    PROJECT_ROOT / 'logs/logger.py',
    PROJECT_ROOT / 'sql/002_create_tables.sql',
    PROJECT_ROOT / 'sql/003_seed_lookup_tables.sql',
    PROJECT_ROOT / 'sql/004_create_indexes.sql',
    PROJECT_ROOT / 'sql/005_create_views.sql',
    PROJECT_ROOT / 'src/etl.py'
]

for file in files:
    file.touch(exist_ok=True)


# ==========================================================
# Database Configuration
# ==========================================================

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


# ==========================================================
# Insert Data in Batch
# ==========================================================


BATCH_SIZE = 1000

