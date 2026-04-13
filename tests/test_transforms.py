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
