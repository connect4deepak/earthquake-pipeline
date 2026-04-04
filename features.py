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
