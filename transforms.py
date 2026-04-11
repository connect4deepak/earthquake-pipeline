import logging
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)
SCALER_PATH = "scaler.pkl"

# Numeric Scaling 
SCALE_COLS = ["magnitude", "depth_km", "latitude", "longitude"]
SCALE_OUTPUT = {
    "magnitude":  "magnitude_scaled",
    "depth_km":   "depth_scaled",
    "latitude":   "latitude_scaled",
    "longitude":  "longitude_scaled",
}

def _load_or_fit_scaler(df: pd.DataFrame) -> MinMaxScaler:
    if os.path.exists(SCALER_PATH):
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
        logger.info(f"[transforms] Loaded existing scaler from '{SCALER_PATH}'.")
    else:
        scaler = MinMaxScaler()
        scaler.fit(df[SCALE_COLS].dropna())
        with open(SCALER_PATH, "wb") as f:
            pickle.dump(scaler, f)
        logger.info(f"[transforms] Fitted new MinMaxScaler and saved to '{SCALER_PATH}'.")
    return scaler