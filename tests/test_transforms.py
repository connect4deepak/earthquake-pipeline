import sys
import os
import unittest
import pickle
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import transforms as _transforms_mod

SCALER_PATH = os.path.join(os.path.dirname(__file__), 'test_scaler.pkl')
_transforms_mod.SCALER_PATH = SCALER_PATH 

def _remove_scaler():
    if os.path.exists(SCALER_PATH):
        os.remove(SCALER_PATH)

from transforms import scale_numeric, encode_categorical, select_final_columns, run_transforms, FINAL_COLUMNS

def make_df(n=20, **overrides):
    np.random.seed(0)
    base = {
        "raw_id":              list(range(1, n + 1)),
        "magnitude":           np.random.uniform(0.5, 5.0, n).tolist(),
        "latitude":            np.random.uniform(-60, 60, n).tolist(),
        "longitude":           np.random.uniform(-180, 180, n).tolist(),
        "depth_km":            np.random.uniform(0, 100, n).tolist(),
        "event_time":          [pd.Timestamp("2025-01-01", tz="UTC")] * n,
        "place":               ["Test"] * n,
        "mag_type":            (["ml"] * (n // 2)) + (["md"] * (n - n // 2)),
        "event_type":          ["earthquake"] * n,
        "status":              ["reviewed"] * n,
        "year":                [2025] * n,
        "month":               [3] * n,
        "day_of_week":         [1] * n,
        "hour":                [12] * n,
        "is_weekend":          [False] * n,
        "hour_sin":            [0.0] * n,
        "hour_cos":            [1.0] * n,
        "month_sin":           [0.5] * n,
        "month_cos":           [0.866] * n,
        "mag_category":        ["minor"] * n,
        "depth_category":      ["shallow"] * n,
        "distance_from_ref_km": np.random.uniform(1000, 15000, n).tolist(),
        "is_outlier":          [False] * n,
    }
    base.update(overrides)
    return pd.DataFrame(base)

# select_final_columns
class TestSelectFinalColumns(unittest.TestCase):
    def setUp(self):
        df = make_df(n=5)
        df["junk_col_a"] = 99
        df["junk_col_b"] = "noise"
        self.out = select_final_columns(df)

    def test_junk_columns_dropped(self):
        self.assertNotIn("junk_col_a", self.out.columns)
        self.assertNotIn("junk_col_b", self.out.columns)
