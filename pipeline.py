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

# Pipeline Stages 
def generate_report(
    raw_df: pd.DataFrame,
    processed_df: pd.DataFrame,
    elapsed: float,
) -> None:
    """Print a concise summary report after the pipeline completes."""
    # Compute cleaning stats
    rows_in   = len(raw_df)
    rows_out  = len(processed_df)
    dropped   = rows_in - rows_out
    pct_kept  = rows_out / rows_in * 100 if rows_in else 0
    print()
    print("=" * 60)
    print("  PIPELINE RUN SUMMARY")
    print("=" * 60)
    print(f"  Completed at   : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"  Elapsed time   : {elapsed:.2f} s")
    print(f"  Pipeline ver.  : {PIPELINE_VERSION}")
    print()
    print(f"  Input rows     : {rows_in:,}")
    print(f"  Output rows    : {rows_out:,}  ({pct_kept:.1f}% retained)")
    print(f"  Dropped rows   : {dropped:,}")
    print()