import argparse
import logging
import sys
import time
from datetime import datetime, timezone

import pandas as pd

from db import (
    create_processed_table,
    load_raw_earthquakes,
    load_new_earthquakes,
    get_last_processed_id,
    save_processed,
)
from cleaning import run_cleaning
from features import run_feature_engineering
from transforms import run_transforms

# Logging setup 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log"),
    ],
)
logger = logging.getLogger(__name__)
PIPELINE_VERSION = "1.0.0"