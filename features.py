import logging
import numpy as np
import pandas as pd
from config import REFERENCE_LAT, REFERENCE_LON, REFERENCE_LABEL

logger = logging.getLogger(__name__)

# Time Features 
def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    t = df["event_time"].dt

    df["year"]        = t.year.astype("Int16")
    df["month"]       = t.month.astype("Int8")       
    df["day_of_week"] = t.dayofweek.astype("Int8")  
    df["hour"]        = t.hour.astype("Int8")      
    df["is_weekend"]  = df["day_of_week"].isin([5, 6])
    # Cyclic encoding for hour and month
    df["hour_sin"]  = np.sin(2 * np.pi * df["hour"]  / 24)
    df["hour_cos"]  = np.cos(2 * np.pi * df["hour"]  / 24)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    logger.info("[features]   Time features added (year, month, dow, hour, cyclic).")
    return df

# Magnitude Category 
# Richter / moment-magnitude labels used by USGS:
#   < 2.0   micro    – not felt by people
#   2–3.9   minor    – felt slightly by some
#   4–4.9   light    – felt by most, minor damage
#   5–5.9   moderate – slight damage to buildings
#   6–6.9   strong   – destructive in populated areas
#   7–7.9   major    – serious damage over large areas
#   ≥ 8     great    – total destruction, tsunamis possible

_MAG_BINS   = [-np.inf, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, np.inf]
_MAG_LABELS = ["micro", "minor", "light", "moderate", "strong", "major", "great"]

def add_magnitude_category(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["mag_category"] = pd.cut(
        df["magnitude"],
        bins=_MAG_BINS,
        labels=_MAG_LABELS,
        right=False,
    ).astype(str)
    counts = df["mag_category"].value_counts().to_dict()
    logger.info(f"[features]   mag_category distribution: {counts}")
    return df
