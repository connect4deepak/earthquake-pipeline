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

# Apply Min-Max scaling and append *_scaled columns
def scale_numeric(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    scaler = _load_or_fit_scaler(df)
    scaled_values = scaler.transform(df[SCALE_COLS].fillna(0))
    scaled_df = pd.DataFrame(
        scaled_values,
        columns=SCALE_COLS,
        index=df.index,
    )

    for raw_col, out_col in SCALE_OUTPUT.items():
        df[out_col] = scaled_df[raw_col].round(6)

    logger.info(
        f"[transforms] Min-Max scaling applied to: {SCALE_COLS}."
    )
    return df

# Categorical Encoding 
TOP_N_MAGTYPES = 8  

def encode_categorical(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # mag_type one-hot encoding 
    if "mag_type" in df.columns:
        top_types = (
            df["mag_type"].value_counts().nlargest(TOP_N_MAGTYPES).index.tolist()
        )
        df["mag_type_clean"] = df["mag_type"].where(
            df["mag_type"].isin(top_types), other="other"
        )

        dummies = pd.get_dummies(
            df["mag_type_clean"],
            prefix="magtype",
            dtype=np.int8,
        )
        df = pd.concat([df, dummies], axis=1)
        df.drop(columns=["mag_type_clean"], inplace=True)
        logger.info(
            f"[transforms] mag_type one-hot encoded: {list(dummies.columns)}"
        )