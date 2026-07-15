# ==========================================================
# Log Folder
# ==========================================================

import logging
from config import LOG_DIR



LOG_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = LOG_DIR / 'roadsense.log'

# Create the Logger with the name RoadSence
logger = logging.getLogger('RoadSence')

# Set the Log Level
logger.setLevel(logging.INFO)

# Create a File Handler
file_handler = logging.FileHandler(LOG_FILE)

# Create a Console Handler
console_handler = logging.StreamHandler()

# Create a Formatter
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s'
)

# Give the Formatter to the File Handler
file_handler.setFormatter(formatter)

# Give the Formatter to the Console Handler
console_handler.setFormatter(formatter)

# Connect the Handlers to the Logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.propagate = False