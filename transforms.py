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