import logging
import numpy as np
import pandas as pd
from config import (
    MAGNITUDE_MIN, MAGNITUDE_MAX,
    DEPTH_MIN_KM, DEPTH_MAX_KM,
    LAT_RANGE, LON_RANGE,
    IQR_MULTIPLIER,
)

logger = logging.getLogger(__name__)

# Schema Normalisation
COLUMN_RENAME_MAP = {
    "mag":        "magnitude",
    "magnitude":  "magnitude",   # already correct
    "lat":        "latitude",
    "latitude":   "latitude",
    "lon":        "longitude",
    "longitude":  "longitude",
    "depth":      "depth_km",
    "time":       "event_time",
    "updated":    "updated_time",
    "place":      "place",
    "type":       "event_type",
    "magtype":        "mag_type",
    "magnitude_type":  "mag_type",
    "magType":    "mag_type",
    "status":     "status",
    "id":         "raw_id",
}

def normalise_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Rename raw columns to the pipeline's internal naming convention."""
    df = df.rename(columns={k: v for k, v in COLUMN_RENAME_MAP.items()
                             if k in df.columns})
    logger.info(f"[schema]     {len(df):,} rows after column rename.")
    return df