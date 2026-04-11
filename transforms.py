import logging
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)
SCALER_PATH = "scaler.pkl"