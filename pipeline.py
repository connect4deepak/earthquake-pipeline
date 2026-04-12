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

    if not processed_df.empty:
        print(f"  Date range     : {processed_df['event_time'].min()} → "
              f"{processed_df['event_time'].max()}")
        print(f"  Magnitude      : {processed_df['magnitude'].min():.1f} – "
              f"{processed_df['magnitude'].max():.1f}  "
              f"(mean {processed_df['magnitude'].mean():.2f})")
        print(f"  Depth (km)     : {processed_df['depth_km'].min():.1f} – "
              f"{processed_df['depth_km'].max():.1f}  "
              f"(mean {processed_df['depth_km'].mean():.2f})")
        print()

        if "mag_category" in processed_df.columns:
            print("  Mag category breakdown:")
            cats = processed_df["mag_category"].value_counts().sort_index()
            for cat, cnt in cats.items():
                bar = "█" * min(int(cnt / max(cats) * 30), 30)
                print(f"    {cat:<12} {cnt:>6,}  {bar}")
        print()

        if "depth_category" in processed_df.columns:
            print("  Depth category breakdown:")
            for cat, cnt in processed_df["depth_category"].value_counts().items():
                print(f"    {cat:<14} {cnt:>6,}")

    print("=" * 60)
    print()    

# Main Entry Point 
def run_pipeline(incremental: bool = False) -> pd.DataFrame:
    """
    Execute the full pipeline.
    Parameters
    ----------
    incremental : bool
        If True, only process rows not yet in the processed table.
    Returns
    -------
    pd.DataFrame
        The final processed DataFrame (also saved to PostgreSQL).
    """
    start = time.time()
    logger.info("╔══════════════════════════════════════════════════════════╗")
    logger.info("║     EARTHQUAKE DATA PREPROCESSING PIPELINE               ║")
    logger.info(f"║     Mode: {'INCREMENTAL' if incremental else 'FULL':10}  Version: {PIPELINE_VERSION:10}              ║")
    logger.info("╚══════════════════════════════════════════════════════════╝")
